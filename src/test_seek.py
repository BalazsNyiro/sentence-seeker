# -*- coding: utf-8 -*-
import unittest, text, util_test, seeker, util, os, util_json_obj, copy

class SeekTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    # for higher text collector functions I will build up a test text
    TxtBird = ("Birds are singing on the Tree but that bird is watching.\n"
               "One of these birds looks like a blackbird, the tree is brown and this one is stronger.\n"
               "The other birds' feather is strong, brown colored, they are hidden in this foliage.\n"
               "Have you ever seen a brown blackbird, like this one?\n")

    def test_group_maker(self):
        self.maxDiff = None
        if self._test_exec("test_group_maker"):
            Prg = self.Prg
            FilePathBird = self.FilePathBird

            ################# init ####################################
            PrgOrig = copy.deepcopy(Prg)
            util.file_del(FilePathBird)
            util.file_write(Prg, Fname=FilePathBird, Content=self.TxtBird)

            seeker.be_ready_to_seeking(Prg, Verbose=False,  LoadOnlyTheseFileBaseNames = [self.FileBaseNameBird])
            #####################################################

            WordsWanted = ["looks", "like", "bird", "this"]
            MatchNumsInSubsentences_ResultInfos, MatchNums__Descending, ResultsTotalNum = seeker.match_in_subsentence__results(Prg, WordsWanted)

            GroupsSubsentenceBasedWanted = { # be careful: the linenum here means the linenum in sentence file, not in the orig!
                # the first num:
                # MatchNumMaxInSubsentences
                2: [{'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 1, 'WordsDetectedInSubsentence': ('looks', 'like'), 'Sentence': 'One of these birds looks like a blackbird, the tree is brown and this one is stronger.\n'},

                    {'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 3, 'WordsDetectedInSubsentence': ('like', 'this'), 'Sentence': 'Have you ever seen a brown blackbird, like this one?'}],
                # FIXME: why we don't have \n at the end of this?

                1: [{'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 0, 'WordsDetectedInSubsentence': ('bird',), 'Sentence': 'Birds are singing on the Tree but that bird is watching.\n'},
                    {'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 1, 'WordsDetectedInSubsentence': ('this',), 'Sentence': 'One of these birds looks like a blackbird, the tree is brown and this one is stronger.\n'},
                    {'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 2, 'WordsDetectedInSubsentence': ('this',), 'Sentence': "The other birds' feather is strong, brown colored, they are hidden in this foliage.\n"}
                   ]
            }

            ################ restore original state #####################################
            util.file_del(FilePathBird)
            util.file_del(Prg["DocumentObjectsLoaded"][self.FileBaseNameBird]["FileIndex"])
            util.file_del(Prg["DocumentObjectsLoaded"][self.FileBaseNameBird]["FileSentences"])
            self.Prg = PrgOrig
            ################ restore original state #####################################

            # print("ResultsTotalNum:", ResultsTotalNum)

            # print("Assert, Matchnums descending...")
            # print("\nMatchNums__Descending", MatchNums__Descending)
            self.assertEqual(MatchNums__Descending, [2, 1])

            #print("Assert, MatchNumsInSubsentences_ResultInfos...")
            #util.display_groups_matchnum_resultinfo(MatchNumsInSubsentences_ResultInfos)
            # print("Group, wanted:")
            # util.display_groups_matchnum_resultinfo(GroupsSubsentenceBasedWanted)
            self.assertEqual(GroupsSubsentenceBasedWanted, MatchNumsInSubsentences_ResultInfos)


    def test_words_wanted_clean(self):
        self.maxDiff = None
        if self._test_exec("test_words_wanted_clean"):
            WordsWanted = "apple, tree"
            WordsWantedCleaned = text.words_wanted_clean(WordsWanted)
            self.assertEqual(WordsWantedCleaned, ["apple", "tree"])

    def test_word_count_in_text(self):
        self.maxDiff = None
        if self._test_exec("test_word_count_in_text"):
            Sentence = "There are appletrees in Apple's applegarden - the owner wanted to eat more apple"
            WordCount = text.word_count_in_text("apple", Sentence)
            self.assertEqual(WordCount, 2)

    def test_word_highlight(self):
        self.maxDiff = None
        if self._test_exec("test_word_highlight"):
            # Prg = self.Prg
            Text = "Apple has a lot of apple in his Tree garden"
            Words = ["apple", "tree"]
            Highlighted = text.word_highlight(Words, Text)

            TextWanted = ">>Apple<< has a lot of >>apple<< in his >>Tree<< garden"
            self.assertEqual(Highlighted, TextWanted)

    def test_seek_linenumbers_with_group_of_words(self):
        self.maxDiff = None
        if self._test_exec("test_seek_linenumbers_with_group_of_words"):
            Prg = self.Prg
            WordsWanted = "apple, tree"
            Index = { "apple": [400, 300 ],
                      "house": [100, 200 ],
                      "mouse": [300, 400 ],
                      "tree":  [  0, 400 ]
                      }
            WordsWanted = text.words_wanted_clean(WordsWanted)
            ResultLineNumbers__WordsDetected = text.linenum__subsentnum__words__collect(Prg, WordsWanted, Index)

            # print("\n>>>>>>",ResultLineNumbers__WordsDetected )

            # 400 means: Line 4, subsentence 0
            # 501 means: Line 5, subsentence 1
            #   2 means: Line 0, Subsentence 2 - line 0 can't be represented, if value < 100, it means LineNum == 0
            Correct = { 0:   ('tree',),
                        300: ('apple',),
                        400: ('apple', 'tree')
                      }
            self.assertEqual(ResultLineNumbers__WordsDetected, Correct)
            self.assertEqual(WordsWanted, ['apple', 'tree'])

            MatchNum__Source_Words = dict()
            text.match_num_in_subsentence__result_obj(Prg, ResultLineNumbers__WordsDetected, "test_seek_linenumbers_with_group_of_words", MatchNum__Source_Words)
            # print("\n>>>>>>", MatchNum__Source_Words)

            # lengt with one result has two elem: in line0, result is 'tree' word, in line 3 'apple' word.
            # length with 2 results has one elem: in line 2 both words is found
            Wanted__MatchNum__SourceAndDetectedWords = {
                 2: [{'FileSourceBaseName': 'test_seek_linenumbers_with_group_of_words', 'LineNumInSentenceFile': 4,
                      'WordsDetectedInSubsentence': ('apple', 'tree'),
                      'Sentence': 'DocumentsObjectsLoaded: test_seek_linenumbers_with_group_of_words is not loaded'}],
                 1: [{'FileSourceBaseName': 'test_seek_linenumbers_with_group_of_words', 'LineNumInSentenceFile': 3,
                      'WordsDetectedInSubsentence': ('apple',),
                      'Sentence': 'DocumentsObjectsLoaded: test_seek_linenumbers_with_group_of_words is not loaded'},
                     {'FileSourceBaseName': 'test_seek_linenumbers_with_group_of_words', 'LineNumInSentenceFile': 0,
                      'WordsDetectedInSubsentence': ('tree',),
                      'Sentence': 'DocumentsObjectsLoaded: test_seek_linenumbers_with_group_of_words is not loaded'}]
            }
            # util.display_groups_matchnum_resultinfo(MatchNum__Source_Words)
            # util.display_groups_matchnum_resultinfo(Wanted__MatchNum__SourceAndDetectedWords)
            self.assertEqual(MatchNum__Source_Words, Wanted__MatchNum__SourceAndDetectedWords)


    def test_sentence_separator__a_naive_01(self): # replace_abbreviations uses text_replace()
        self.maxDiff = None
        if self._test_exec("test_sentence_separator__a_naive_01"):
            Txt = 'Mr. and Mrs. Jones visited their friends... "Lisa and Pete lived in a big house, in Boston, did they?"  Yes, they did'
            Wanted = \
                ["Mr and Mrs Jones visited their friends...",
                 '"Lisa and Pete lived in a big house, in Boston, did they?"',
                 "Yes, they did"]
            Sentences = text.sentence_separator(Txt)
            self.assertEqual(Wanted, Sentences)

    def test_file_create_sentences__create_index(self):
        self.maxDiff = None
        if self._test_exec("test_file_create_sentences__create_index"):
            Prg = self.Prg

            FileSentences = os.path.join(Prg["DirWork"], "test_file_create_sentences.txt")
            util.file_del(FileSentences)

            Sample = 'He is my friend. "This is \n the next - city, London -- here, in London, the sky is nice." Is this the third line, or a Book about London?'

            seeker.file_sentence_create(Prg, FileSentences, Sample)
            Wanted = ["He is my friend.\n", # detect London only once from this sentence:
                      '"This is the next - city, London -- here, in London, the sky is nice."\n',
                      "Is this the third line, or a Book about London?"]

            LinesFromFile = util.file_read_lines(Prg, FileSentences)
            self.assertEqual(Wanted, LinesFromFile)

            FileIndex = os.path.join(Prg["DirWork"], "test_file_create_index.txt")
            util.file_del(FileIndex)
            seeker.file_index_create(Prg, FileIndex, FileSentences)
            #seeker.file_index_create(Prg, "/tmp/index.txt", FileSentences)
            # print(util.file_read_all(Prg, FileIndex))

            Index = util_json_obj.obj_from_file(FileIndex)
            self.assertEqual(Index["london"], [101, 102, 201])

            util.file_del(FileSentences)
            util.file_del(FileIndex)

def run_all_tests(Prg):
    SeekTests.Prg = Prg

    # I can't use self.Prg when I define class variable so I set FilePath from here
    SeekTests.FilePathBird = os.path.join(Prg["DirDocuments"], "test_group_maker_document.txt")
    SeekTests.FileBaseNameBird = "test_group_maker_document.txt"
    unittest.main(module="test_seek", verbosity=2, exit=False)

