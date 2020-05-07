# -*- coding: utf-8 -*-
import unittest, text, util_test, seeker, util, os, util_json_obj, copy

class SeekTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    # for higher text collector functions I will build up a test text
    TxtBird = ("Birds are singing on the Tree.\n"
               "One of these birds looks like a blackbird, the tree is brown.\n"
               "The other birds' feather is strong, brown colored, they are hidden in the foliage.\n"
               "Have you ever seen a brown blackbird, like this one?\n")

    def test_group_maker(self):
        if self._test_exec("test_group_maker"):
            Prg = self.Prg
            FilePathBird = self.FilePathBird

            ################# init ####################################
            PrgOrig = copy.deepcopy(Prg)
            util.file_del(FilePathBird)
            util.file_write(Prg, Fname=FilePathBird, Content=self.TxtBird)

            seeker.be_ready_to_seeking(Prg, Verbose=False)
            DocsSaved = Prg["DocumentObjectsLoaded"][self.FileBaseNameBird]
            Prg["DocumentObjectsLoaded"] = dict()        # clear everything

            # load back only the test obj
            Prg["DocumentObjectsLoaded"][self.FileBaseNameBird] = DocsSaved
            print("\nDocumentObjectsLoaded", Prg["DocumentObjectsLoaded"])
            #####################################################

            WordsWanted = ["looks", "like", "bird"]
            Groups_MatchNums_ResultInfos, MatchNums__Descending, ResultsTotalNum = seeker.group_maker(Prg, WordsWanted)
            print("\nGroups_MatchNums_ResultInfos", Groups_MatchNums_ResultInfos)

            # TODO: check Linenum handling in group_maker:  0-based, 1 based?
            # TODO: LineNumsInLine__WordsDetected = text.linenums__words_detected_in_line__collect(WordsWanted, Doc["Index"])
            # TODO: review this test

            # TODO: CHECK LINE RESULTS
            GroupsWanted = { # be careful: the linenum here means the linenum in sentence file, not in the orig!
                1: [{'Source': 'test_group_maker_document.txt', 'LineNum': 3, 'WordsDetected': ['like']}],
                2: [{'Source': 'test_group_maker_document.txt', 'LineNum': 1, 'WordsDetected': ['looks', 'like']}]
            }
            self.assertEqual(GroupsWanted, Groups_MatchNums_ResultInfos)
            # TODO: CHECK LINE RESULTS


            print("\nMatchNums__Descending", MatchNums__Descending)
            self.assertEqual(MatchNums__Descending, [2, 1])

            # self.assertEqual(GroupsDetected, GroupsWanted)
            print("ResultsTotalNum:", ResultsTotalNum)

            ################ restore original state #####################################
            self.Prg = PrgOrig
            util.file_del(FilePathBird)
            util.file_del(Prg["DocumentObjectsLoaded"][self.FileBaseNameBird]["FileIndex"])
            util.file_del(Prg["DocumentObjectsLoaded"][self.FileBaseNameBird]["FileSentences"])

    def test_match_num_max_in_subsentences(self):
        if self._test_exec("test_match_num_max_in_subsentences"):
            WordsWanted = ["what", "do", "like"] # do is two times in second subsentence
            MatchNumInSentences = 3              # but 'do'+'do'+'like' = 2 only because 'do' is repeated
            Sentence = "What is your favourite color, for example do you like black like I do?"
            MatchNumMaxSubsentences = text.match_num_max_in_subsentences(MatchNumInSentences, WordsWanted, Sentence)
            self.assertEqual(MatchNumMaxSubsentences, 2)

    def test_words_wanted_clean(self):
        if self._test_exec("test_words_wanted_clean"):
            WordsWanted = "apple, tree"
            WordsWantedCleaned = text.words_wanted_clean(WordsWanted)
            self.assertEqual(WordsWantedCleaned, ["apple", "tree"])

    def test_word_count_in_text(self):
        if self._test_exec("test_word_count_in_text"):
            Sentence = "There are appletrees in Apple's applegarden - the owner wanted to eat more apple"
            WordCount = text.word_count_in_text("apple", Sentence)
            self.assertEqual(WordCount, 2)

    def test_word_highlight(self):
        if self._test_exec("test_word_highlight"):
            # Prg = self.Prg
            Text = "Apple has a lot of apple in his Tree garden"
            Words = ["apple", "tree"]
            Highlighted = text.word_highlight(Words, Text)

            TextWanted = ">>Apple<< has a lot of >>apple<< in his >>Tree<< garden"
            self.assertEqual(Highlighted, TextWanted)

    def test_seek_linenumbers_with_group_of_words(self):
        if self._test_exec("test_seek_linenumbers_with_group_of_words"):
            # Prg = self.Prg
            WordsWanted = "apple, tree"
            Index = { "apple": [4, 3],
                      "house": [1, 2],
                      "mouse": [3, 4],
                      "tree":  [0, 4]
                      }
            WordsWanted = text.words_wanted_clean(WordsWanted)
            ResultLineNumbers__WordsDetected = text.linenums__words_detected_in_line__collect(WordsWanted, Index)

            # print("\n>>>>>>", LineNumbersAllWord)
            Correct = { 0: ['tree'],
                        4: ['apple', 'tree'],
                        3: ['apple']
                        }
            self.assertEqual(ResultLineNumbers__WordsDetected, Correct)
            self.assertEqual(WordsWanted, ['apple', 'tree'])

            MatchNum__SourceAndDetectedWords = text.result_obj_maker__words_detected_group_by_match_num(ResultLineNumbers__WordsDetected, "test")
            # print("\n>>>>>>", MatchNum__SourceAndDetectedWords)

            # lengt with one result has two elem: in line0, result is 'tree' word, in line 3 'apple' word.
            # length with 2 results has one elem: in line 2 both words is found
            Wanted__MatchNum__SourceAndDetectedWords = {
                1: [{'Source': 'test', 'LineNum': 3, 'WordsDetected': ['apple']},
                    {'Source': 'test', 'LineNum': 0, 'WordsDetected': ['tree']}],
                2: [{'Source': 'test', 'LineNum': 4, 'WordsDetected': ['apple', 'tree']}]
            }
            self.assertEqual(MatchNum__SourceAndDetectedWords, Wanted__MatchNum__SourceAndDetectedWords)


    def test_sentence_separator__a_naive_01(self): # replace_abbreviations uses text_replace()
        if self._test_exec("test_sentence_separator__a_naive_01"):
            Txt = 'Mr. and Mrs. Jones visited their friends... "Lisa and Pete lived in a big house, in Boston, did they?"  Yes, they did'
            Wanted = \
                ["Mr and Mrs Jones visited their friends...",
                 '"Lisa and Pete lived in a big house, in Boston, did they?"',
                 "Yes, they did"]
            Sentences = text.sentence_separator(Txt)
            self.assertEqual(Wanted, Sentences)

    def test_file_create_sentences__create_index(self):
        if self._test_exec("test_file_create_sentences__create_index"):
            Prg = self.Prg

            FileSentences = os.path.join(Prg["DirWork"], "test_file_create_sentences.txt")
            util.file_del(FileSentences)

            Sample = 'He is my friend. "This is \n the next - city, London." Is this the third line, or a Book about London?'

            seeker.file_sentence_create(Prg, FileSentences, Sample)
            Wanted = ["He is my friend.\n",
                      '"This is the next - city, London."\n',
                      "Is this the third line, or a Book about London?"]

            LinesFromFile = util.file_read_lines(Prg, FileSentences)
            self.assertEqual(Wanted, LinesFromFile)

            FileIndex = os.path.join(Prg["DirWork"], "test_file_create_index.txt")
            util.file_del(FileIndex)
            seeker.file_index_create(Prg, FileIndex, FileSentences)

            Index = util_json_obj.obj_from_file(FileIndex)
            self.assertEqual(Index["london"], [1, 2])

            util.file_del(FileSentences)
            util.file_del(FileIndex)

def run_all_tests(Prg):
    SeekTests.Prg = Prg

    # I can't use self.Prg when I define class variable so I set FilePath from here
    SeekTests.FilePathBird = os.path.join(Prg["DirDocuments"], "test_group_maker_document.txt")
    SeekTests.FileBaseNameBird = "test_group_maker_document.txt"
    unittest.main(module="test_seek", verbosity=2, exit=False)

