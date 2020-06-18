# -*- coding: utf-8 -*-
import unittest, text, util_test, seeker, util, os, util_json_obj, copy

import seeker_logic
from document import document_obj

class SeekTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    # for higher text collector functions I will build up a test text
    TxtBird = ("Birds are singing on the Tree but that bird is watching.\n"
               "One of these birds looks like a blackbird, the tree is brown and this one is stronger.\n"
               "The other birds' feather is strong, brown colored, they are hidden in this foliage.\n"
               "Have you ever seen a brown blackbird, like this one?\n"
               "Nightingale is a special bird because it's song is\n"
               "enjoyable and kind for every bird watcher.\n"
               "Special nights visitors can hear the male birds' song.\n"
               "These special events help to known the history of this special bird species for special audience.\n"
               )

    def test_token_split(self):
        if self._test_exec("test_token_split"):
            Query = "(apple   house,mouse)"
            Wanted = ["(", "apple", "AND", "house", "AND", "mouse", ")"]
            self.assertEqual(seeker_logic.token_split(Query), Wanted)

    def test_token_split(self):
        if self._test_exec("test_token_split"):
            Query = "apple  house"
            Wanted = ["apple", "AND", "house"]

            TokensDetected = seeker_logic.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

    def test_token_interpreter(self):
        if self._test_exec("test_token_interpreter"):
            Prg = self.Prg
            FilePathBird = self.FilePathBird

            PrgOrig = copy.deepcopy(Prg)
            util.file_del(FilePathBird)
            util.file_write(Prg, Fname=FilePathBird, Content=self.TxtBird)

            seeker.be_ready_to_seeking(Prg, Verbose=False,  LoadOnlyTheseFileBaseNames = [self.FileBaseNameBird])
            ######################################################################

            def token_interpreter_wrapper(Prg, Query):
                Tokens = seeker_logic.token_split(Query)
                TokenGroups = seeker_logic.token_group_finder(Tokens)
                DocObj = Prg["DocumentObjectsLoaded"]["test_document_bird"]["Index"]

                TokenProcessExplainOneDoc = []
                return seeker_logic.token_interpreter(Prg, TokenGroups, DocObj, TokenProcessExplainOneDoc,  FirstRun=True)

            if True:
                Query = "are"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0: True, 202: True}
                self.assertEqual(Result, ResultWanted)

                Query = "birds"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0:True, 100:True, 200:True, 500:True}
                self.assertEqual(Result, ResultWanted)

                Query = "is"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0: True, 101: True, 200: True, 400: True}
                self.assertEqual(Result, ResultWanted)

                Query = "strong"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200: True}
                self.assertEqual(Result, ResultWanted)

                Query = "birds is"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0:True, 200:True}
                self.assertEqual(Result, ResultWanted)

                Query = "birds  is,strong"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200:True}
                self.assertEqual(Result, ResultWanted)

                Query = "(birds  is),strong"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200:True}
                self.assertEqual(Result, ResultWanted)

                Query = "(birds  is,are),(strong)"
                Result = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {}
                self.assertEqual(Result, ResultWanted)

            ##### OR ######
            Query = "birds   OR  is"
            Result = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {0: True, 100: True, 101: True, 200: True, 400: True, 500: True}
            self.assertEqual(Result, ResultWanted)

            Query = "(((strong OR are)))"
            Result = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {0: True, 200: True, 202: True}
            self.assertEqual(Result, ResultWanted)

            Query = "(((strong OR are))) OR ()"
            Result = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {0: True, 200: True, 202: True}
            self.assertEqual(Result, ResultWanted)

            Query = "(((strong OR are))) AND ()"
            Result = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {}
            self.assertEqual(Result, ResultWanted)

            #########  COMPLEX QUERY ###########
            Query = "(birds   OR  is) AND strong"
            Result = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {200: True}
            self.assertEqual(Result, ResultWanted)

            Query = "(birds   OR  is) AND (strong OR are)"
            Result = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {0: True, 200: True}
            self.assertEqual(Result, ResultWanted)

            ################ restore original state #####################################
            util.file_del(FilePathBird)
            FileNameWithoutExtension = util.filename_without_extension(self.FileBaseNameBird)
            util.file_del(Prg["DocumentObjectsLoaded"][FileNameWithoutExtension]["FileIndex"])
            util.file_del(Prg["DocumentObjectsLoaded"][FileNameWithoutExtension]["FileSentences"])
            self.Prg = PrgOrig

    def test_match_in_subsentence_logic(self):
        if self._test_exec("test_match_in_subsentence_logic"):
            Prg = self.Prg
            FilePathBird = self.FilePathBird

            PrgOrig = copy.deepcopy(Prg)
            util.file_del(FilePathBird)
            util.file_write(Prg, Fname=FilePathBird, Content=self.TxtBird)

            seeker.be_ready_to_seeking(Prg, Verbose=False,  LoadOnlyTheseFileBaseNames = [self.FileBaseNameBird])


            Query = "(every OR special) AND (events OR (bird OR audience))"
            TokensDetected = seeker_logic.token_split(Query)
            TokensWanted = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            self.assertEqual(TokensDetected, TokensWanted)

            TokenGroupsDetected = seeker_logic.token_group_finder(TokensDetected)
            TokenGroupsWanted = [['every', 'OR', 'special'], 'AND', ['events', 'OR', ['bird', 'OR', 'audience']]]
            self.assertEqual(TokenGroupsDetected, TokenGroupsWanted)

            seeker_logic.seek(Prg, Query)


            ################ restore original state #####################################
            util.file_del(FilePathBird)
            FileNameWithoutExtension = util.filename_without_extension(self.FileBaseNameBird)
            util.file_del(Prg["DocumentObjectsLoaded"][FileNameWithoutExtension]["FileIndex"])
            util.file_del(Prg["DocumentObjectsLoaded"][FileNameWithoutExtension]["FileSentences"])
            self.Prg = PrgOrig

    def test_word_highlight(self):
        self.maxDiff = None
        if self._test_exec("test_word_highlight"):
            # Prg = self.Prg
            Text = "Apple has a lot of apple in his Tree garden"
            Words = ["apple", "tree"]
            Highlighted = text.word_highlight(Words, Text)

            TextWanted = ">>Apple<< has a lot of >>apple<< in his >>Tree<< garden"
            self.assertEqual(Highlighted, TextWanted)

    def test_sentence_separator(self): # replace_abbreviations uses text_replace()
        self.maxDiff = None
        if self._test_exec("test_sentence_separator"):
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
    SeekTests.FilePathBird = os.path.join(Prg["DirDocuments"], "test_document_bird.txt")
    SeekTests.FileBaseNameBird = "test_document_bird.txt"
    unittest.main(module="test_seek", verbosity=2, exit=False)

