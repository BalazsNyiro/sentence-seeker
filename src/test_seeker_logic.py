# -*- coding: utf-8 -*-
import unittest, util_test, copy, util, seeker
import seeker_logic
import os.path

class SeekerLogicTests(util_test.SentenceSeekerTest):
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

    def test_words_wanted_from_tokens(self):
        if self._test_exec("test_words_wanted_from_tokens"):
            Tokens = ["(", "apple", "AND", "orange", ")"]
            Words = seeker_logic.words_wanted_from_tokens(Tokens)
            self.assertEqual(Words, ["apple", "orange"])

    def test_token_split(self):
        if self._test_exec("test_token_split"):
            Query = "(apple   house,mouse)"
            Wanted = ["(", "apple", "AND", "house", "AND", "mouse", ")"]
            self.assertEqual(seeker_logic.token_split(Query), Wanted)

            Query = "(every OR special) AND (events OR (bird OR audience))"
            TokensDetected = seeker_logic.token_split(Query)
            TokensWanted = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            self.assertEqual(TokensDetected, TokensWanted)


    def test_token_split_and(self):
        if self._test_exec("test_token_split_and"):
            Query = "apple  house"
            Wanted = ["apple", "AND", "house"]

            TokensDetected = seeker_logic.token_split(Query)
            self.assertEqual(TokensDetected, Wanted)

    def test_token_group_finder(self):
        if self._test_exec("test_token_group_finder"):
            Tokens = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            TokenGroupsDetected = seeker_logic.token_group_finder(Tokens)
            TokenGroupsWanted = [['every', 'OR', 'special'], 'AND', ['events', 'OR', ['bird', 'OR', 'audience']]]
            self.assertEqual(TokenGroupsDetected, TokenGroupsWanted)

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

                Explains = []
                ResultDict, ResultName = seeker_logic.token_interpreter(TokenGroups, DocObj, Explains)
                print("\n\n.................")
                print(Query)
                print(Explains)
                return ResultDict

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


def run_all_tests(Prg):
    SeekerLogicTests.Prg = Prg
    # I can't use self.Prg when I define class variable so I set FilePath from here
    SeekerLogicTests.FilePathBird = os.path.join(Prg["DirDocuments"], "test_document_bird.txt")
    SeekerLogicTests.FileBaseNameBird = "test_document_bird.txt"
    unittest.main(module="test_seeker_logic", verbosity=2, exit=False)

