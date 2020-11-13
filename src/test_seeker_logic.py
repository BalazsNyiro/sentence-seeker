# -*- coding: utf-8 -*-
import unittest, util_test, copy, util, seeker
import seeker_logic, text
import os.path
import document

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

    def test_operator_exec(self):
        if self._test_exec("test_operator_exec"):

            # These are subsentence coordinates BUT NOT WITH ORIGINAL LINENUMBERS
            # the first coordinate is the sentence number, the last two digits represent
            # the subsentence coord.
            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200}, '(birds AND is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds AND is)', 2)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND',
                       ({0, 101, 200, 400}, 'is'), 'AND', ({200}, 'strong')]
            Explains = [('birds', 4), ('is', 4), ('strong', 1)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({200}, '((birds AND is) AND strong)')])
            self.assertEqual(Explains, [('birds', 4),
                                        ('is', 4),
                                        ('strong', 1),
                                        ('(birds AND is)', 2),
                                        ('((birds AND is) AND strong)', 1)]
                             )

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200}, '(birds AND is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds AND is)', 2)])

            Tokens = [({0, 200}, '(birds AND is)'), 'AND', ({200}, 'strong')]
            Explains = [('birds', 4), ('is', 4), ('strong', 1)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({200}, '((birds AND is) AND strong)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('strong', 1), ('((birds AND is) AND strong)', 1)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND',
                       ({0, 101, 200, 400}, 'is'), 'AND', ({0, 202}, 'are')]
            Explains = [('birds', 4), ('is', 4), ('are', 2)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0}, '((birds AND is) AND are)')])
            self.assertEqual(Explains, [('birds', 4),
                                        ('is', 4),
                                        ('are', 2),
                                        ('(birds AND is)', 2),
                                        ('((birds AND is) AND are)', 1)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'OR',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 100, 101, 200, 400, 500}, '(birds OR is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6)])

            Tokens = [({200}, 'strong'), 'OR', ({0, 202}, 'are')]
            Explains = [('strong', 1), ('are', 2)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200, 202}, '(strong OR are)')])
            self.assertEqual(Explains, [('strong', 1), ('are', 2), ('(strong OR are)', 3)])

            Tokens = [({200, 0, 202}, '(strong OR are)'), 'OR', (set(), '(empty_group)')]
            Explains = [('strong', 1), ('are', 2)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200, 202}, '((strong OR are) OR (empty_group))')])
            self.assertEqual(Explains, [('strong', 1), ('are', 2), ('((strong OR are) OR (empty_group))', 3)])

            Tokens = [({200, 0, 202}, '(strong OR are)'), 'AND', (set(), '(empty_group)')]
            Explains = [('strong', 1), ('are', 2)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [(set(), '((strong OR are) AND (empty_group))')])
            self.assertEqual(Explains, [('strong', 1), ('are', 2), ('((strong OR are) AND (empty_group))', 0)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'OR',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 100, 101, 200, 400, 500}, '(birds OR is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6)])

            Tokens = [({0, 202}, 'are'), 'OR', ({0}, 'singing')]
            Explains = [('birds', 4), ('are', 2), ('singing', 1)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 202}, '(are OR singing)')])
            self.assertEqual(Explains, [('birds', 4), ('are', 2), ('singing', 1), ('(are OR singing)', 2)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND', ({0, 202}, '(are OR singing)'),
                       'AND', ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('are', 2), ('singing', 1), ('is', 4)]
            Tokens, Explains = seeker_logic.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0}, '((birds AND (are OR singing)) AND is)')])
            self.assertEqual(Explains, [('birds', 4),
                                        ('are', 2),
                                        ('singing', 1),
                                        ('is', 4),
                                        ('(birds AND (are OR singing))', 1),
                                        ('((birds AND (are OR singing)) AND is)', 1)])

    def test_is_operator(self):
        if self._test_exec("test_is_operator"):

            self.assertFalse(seeker_logic.is_operator("Mother"))
            self.assertFalse(seeker_logic.is_operator("and"))
            self.assertFalse(seeker_logic.is_operator("Or"))

            # not operator, not string
            self.assertFalse(seeker_logic.is_operator(["big", "AND", "car"]))

            self.assertTrue(seeker_logic.is_operator("("))
            self.assertTrue(seeker_logic.is_operator(")"))
            self.assertTrue(seeker_logic.is_operator("AND"))
            self.assertTrue(seeker_logic.is_operator("OR"))

    def test_is_str_but_not_operator(self):
        if self._test_exec("test_is_str_but_not_operator"):

            self.assertTrue(seeker_logic.is_str_but_not_operator("Mother"))
            self.assertTrue(seeker_logic.is_str_but_not_operator("and"))
            self.assertTrue(seeker_logic.is_str_but_not_operator("Or"))

            # not operator, not string
            self.assertFalse(seeker_logic.is_str_but_not_operator(["big", "AND", "car"]))

            self.assertFalse(seeker_logic.is_str_but_not_operator("("))
            self.assertFalse(seeker_logic.is_str_but_not_operator(")"))
            self.assertFalse(seeker_logic.is_str_but_not_operator("AND"))
            self.assertFalse(seeker_logic.is_str_but_not_operator("OR"))


    def test_result_selectors(self):
        if self._test_exec("test_result_selectors"):
            Obj1 = text.result_obj("FileSourceBaseName1", 11, 1,
                                   "Sentence first part, and the other very long subsentence with interesting words because the main sentence has to be very long.",
                                   "Sentence first part", True)
            Obj2 = text.result_obj("FileSourceBaseName2", 11, 2,
                                   "Sentence first section, second part.",
                                   "second part.", True)

            Obj3 = text.result_obj("FileSourceBaseName1", 11, 1,
                                   "Sentence first part, when subsentence length is equal with Obj1 but the main sentence is shorter.",
                                   "Sentence first part", True)

        WordsMaybeDetected = ["part"]
        ResultsSelectedOrig = [Obj1, Obj2]
        ResultsSelected = seeker_logic.resultSelectors(ResultsSelectedOrig, WordsMaybeDetected)
        self.assertEqual(ResultsSelected, [Obj2, Obj1])

        ResultsSelectedOrig = [Obj1, Obj2, Obj3]
        ResultsSelected = seeker_logic.resultSelectors(ResultsSelectedOrig, WordsMaybeDetected)

        self.assertEqual(ResultsSelected, [Obj2, Obj3, Obj1])

    def test_words_wanted_from_tokens(self):
        if self._test_exec("test_words_wanted_from_tokens"):
            Tokens = ["(", "apple", "AND", "orange", ")"]
            Words = seeker_logic.words_wanted_from_tokens(Tokens)
            self.assertEqual(Words, ["apple", "orange"])

    def test_word_group_collect(self):
        if self._test_exec("test_word_group_collect"):
            Words = ["apple", "orange", "grape"]
            Group = seeker_logic.word_group_collect(Words)
            self.assertEqual(Group, ["(", "apple", "OR", "orange", "OR", "grape", ")"])

    def test_token_split(self):
        if self._test_exec("test_token_split"):
            Query = "like 1945"
            Wanted = ["like", "AND", "1945"]
            self.assertEqual(seeker_logic.token_split(Query), Wanted)

            Query = "(apple   house,mouse)"
            Wanted = ["(", "apple", "AND", "house", "AND", "mouse", ")"]
            self.assertEqual(seeker_logic.token_split(Query), Wanted)

            Query = "(every OR special) AND (events OR (bird OR audience))"
            TokensDetected = seeker_logic.token_split(Query)
            TokensWanted = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            self.assertEqual(TokensDetected, TokensWanted)

            Query = "birds (are OR  singing) AND (is)"
            TokensDetected = seeker_logic.token_split(Query)
            TokensWanted = ["birds", "AND", "(", "are", "OR", "singing", ")", "AND", "(", "is", ")"]
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
            document.doc_objects_delete__file_abspath(Prg, FilePathBird)
            util.file_write(Prg, Fname=FilePathBird, Content=self.TxtBird)
            # print("\n#### FILE WRITE:'", ResultWrite)

            seeker.be_ready_to_seeking(Prg, Verbose=False,  LoadOnlyThese=[self.FileBaseNameBirdWithoutExt])
            ######################################################################

            def token_interpreter_wrapper(Prg, Query):
                Tokens = seeker_logic.token_split(Query)
                TokenGroups = seeker_logic.token_group_finder(Tokens)
                DocIndex = Prg["DocumentObjectsLoaded"]["test_document_bird"]["WordPosition"]

                Explains = []
                ResultDict, ResultName = seeker_logic.token_interpreter(TokenGroups, DocIndex, Explains)
                return ResultDict, Explains

            if True:
                Query = "are"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 202}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('are', 2)]) # One Explain: ('Token', NumOfIndexElemsInDocIndex)

                Query = "birds"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 100, 200, 500}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4)])

                Query = "is"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 101, 200, 400}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('is', 4)])

                Query = "strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('strong', 1)])

                Query = "birds is"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 200}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds AND is)', 2)])

                Query = "birds  is,strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('strong', 1), ('(birds AND is)', 2), ('((birds AND is) AND strong)', 1)])

                Query = "(birds  is),strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds AND is)', 2), ('strong', 1), ('((birds AND is) AND strong)', 1)])

                Query = "(birds  is,are),(strong)"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = set()
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('are', 2), ('(birds AND is)', 2), ('((birds AND is) AND are)', 1), ('strong', 1), ('(((birds AND is) AND are) AND strong)', 0)])

                ##### OR ######
                Query = "birds   OR  is"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 100, 101, 200, 400, 500}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6)])

                Query = "(((strong OR are)))"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 200, 202}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('strong', 1), ('are', 2), ('(strong OR are)', 3)])

                Query = "(((strong OR are))) OR ()"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 200, 202}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('strong', 1), ('are', 2), ('(strong OR are)', 3), ('((strong OR are) OR (empty_group))', 3)])

                Query = "(((strong OR are))) AND ()"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = set()
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('strong', 1), ('are', 2), ('(strong OR are)', 3), ('((strong OR are) AND (empty_group))', 0)])

                #########  COMPLEX QUERY ###########
                Query = "(birds   OR  is) AND strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {200}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6), ('strong', 1), ('((birds OR is) AND strong)', 1)])

                Query = "(birds   OR  is) AND (strong OR are)"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 200}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6), ('strong', 1), ('are', 2), ('(strong OR are)', 3), ('((birds OR is) AND (strong OR are))', 2)])

            Query = "birds (are OR  singing) AND (is)"
            Result, Explains = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {0}
            self.assertEqual(Result, ResultWanted)
            self.assertEqual(Explains, [('birds', 4), ('are', 2), ('singing', 1), ('(are OR singing)', 2), ('is', 4), ('(birds AND (are OR singing))', 1), ('((birds AND (are OR singing)) AND is)', 1)])

            ################ restore original state #####################################
            document.doc_objects_delete__file_abspath(Prg, FilePathBird)
            self.Prg = PrgOrig


def run_all_tests(Prg):
    SeekerLogicTests.Prg = Prg
    # I can't use self.Prg when I define class variable so I set FilePath from here
    SeekerLogicTests.FileNameBird = "test_document_bird.txt"
    SeekerLogicTests.FileBaseNameBirdWithoutExt = "test_document_bird"
    SeekerLogicTests.FilePathBird = os.path.join(Prg["DirDocuments"], SeekerLogicTests.FileNameBird)
    unittest.main(module="test_seeker_logic", verbosity=2, exit=False)

