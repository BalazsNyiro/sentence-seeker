# -*- coding: utf-8 -*-
import unittest, util_test, copy, util, seeker
import text, result_selectors
import os.path
import document
import tokens

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
            Tokens = [({0,  100, 20001, 501214}, 'birds'), 'AND',
                       ({1, 101, 20002, 501215, 61234}, 'is')]
            Explains = [('birds', 4), ('is', 5)]
            Tokens2, Explains = tokens.operators_exec(Tokens, Explains, Scope="subsentence")
            self.assertEqual(Tokens2, [({0, 1, 20001, 20002, 100, 101, 501214, 501215}, '(birds AND is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 5), ('(birds AND is)', 8)])

            Tokens = [({0, 12300, 20001, 500}, 'birds'),
                      'AND',
                      ({1, 12301, 20002, 400}, 'is'),
                      'AND',
                      ({20003}, 'strong')]
            Explains = [('birds', 4), ('is', 4), ('strong', 1)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({20001, 20002, 20003}, '(birds AND (is AND strong))')])

            self.assertEqual(Explains, [('birds', 4),
                                        ('is', 4),
                                        ('strong', 1),
                                        ('(is AND strong)', 2),
                                        ('(birds AND (is AND strong))', 3)]
                             )

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 100, 101, 200}, '(birds AND is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds AND is)', 4)])

            Tokens = [({0, 200}, '(birds AND is)'), 'AND', ({200}, 'strong')]
            Explains = [('birds', 4), ('is', 4), ('strong', 1)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({200}, '((birds AND is) AND strong)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('strong', 1), ('((birds AND is) AND strong)', 1)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND',
                       ({0, 101, 200, 400}, 'is'), 'AND', ({0, 202}, 'are')]
            Explains = [('birds', 4), ('is', 4), ('are', 2)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 202, 200}, '(birds AND (is AND are))')])
            self.assertEqual(Explains, [('birds', 4),
                                        ('is', 4),
                                        ('are', 2),
                                        ('(is AND are)', 3),
                                        ('(birds AND (is AND are))', 3)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'OR',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 100, 101, 200, 400, 500}, '(birds OR is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6)])

            Tokens = [({200}, 'strong'), 'OR', ({0, 202}, 'are')]
            Explains = [('strong', 1), ('are', 2)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200, 202}, '(strong OR are)')])
            self.assertEqual(Explains, [('strong', 1), ('are', 2), ('(strong OR are)', 3)])

            Tokens = [({200, 0, 202}, '(strong OR are)'), 'OR', (set(), '(empty_group)')]
            Explains = [('strong', 1), ('are', 2)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200, 202}, '((strong OR are) OR (empty_group))')])
            self.assertEqual(Explains, [('strong', 1), ('are', 2), ('((strong OR are) OR (empty_group))', 3)])

            Tokens = [({200, 0, 202}, '(strong OR are)'), 'AND', (set(), '(empty_group)')]
            Explains = [('strong', 1), ('are', 2)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [(set(), '((strong OR are) AND (empty_group))')])
            self.assertEqual(Explains, [('strong', 1), ('are', 2), ('((strong OR are) AND (empty_group))', 0)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'OR',
                       ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('is', 4)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 100, 101, 200, 400, 500}, '(birds OR is)')])
            self.assertEqual(Explains, [('birds', 4), ('is', 4), ('(birds OR is)', 6)])

            Tokens = [({0, 202}, 'are'), 'OR', ({0}, 'singing')]
            Explains = [('birds', 4), ('are', 2), ('singing', 1)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 202}, '(are OR singing)')])
            self.assertEqual(Explains, [('birds', 4), ('are', 2), ('singing', 1), ('(are OR singing)', 2)])

            Tokens = [({0, 100, 200, 500}, 'birds'), 'AND', ({0, 202}, '(are OR singing)'),
                       'AND', ({0, 101, 200, 400}, 'is')]
            Explains = [('birds', 4), ('are', 2), ('singing', 1), ('is', 4)]
            Tokens, Explains = tokens.operators_exec(Tokens, Explains)
            self.assertEqual(Tokens, [({0, 200, 202}, '(birds AND ((are OR singing) AND is))')])
            self.assertEqual(Explains, [('birds', 4),
                                        ('are', 2),
                                        ('singing', 1),
                                        ('is', 4),
                                        ('((are OR singing) AND is)', 3),
                                        ('(birds AND ((are OR singing) AND is))', 3)])

    def test_is_operator(self):
        if self._test_exec("test_is_operator"):

            self.assertFalse(tokens.is_operator("Mother"))
            self.assertFalse(tokens.is_operator("and"))
            self.assertFalse(tokens.is_operator("Or"))

            # not operator, not string
            self.assertFalse(tokens.is_operator(["big", "AND", "car"]))

            self.assertTrue(tokens.is_operator("("))
            self.assertTrue(tokens.is_operator(")"))
            self.assertTrue(tokens.is_operator("AND"))
            self.assertTrue(tokens.is_operator("OR"))

    def test_is_str_but_not_operator(self):
        if self._test_exec("test_is_str_but_not_operator"):

            self.assertTrue(tokens.is_str_but_not_operator("Mother"))
            self.assertTrue(tokens.is_str_but_not_operator("and"))
            self.assertTrue(tokens.is_str_but_not_operator("Or"))

            # not operator, not string
            self.assertFalse(tokens.is_str_but_not_operator(["big", "AND", "car"]))

            self.assertFalse(tokens.is_str_but_not_operator("("))
            self.assertFalse(tokens.is_str_but_not_operator(")"))
            self.assertFalse(tokens.is_str_but_not_operator("AND"))
            self.assertFalse(tokens.is_str_but_not_operator("OR"))


    #def __init__(self, Prg, FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, WordNum, SentenceFillInResult):
    def test_result_selectors(self):
        if self._test_exec("test_result_selectors"):
            Prg = dict()
            Obj1 = text.sentence_obj_from_memory(Prg, "FileSourceBaseName1", 11, 1, 0, True,
                                   "Sentence first part, and the other very long subsentence with interesting words because the main sentence has to be very long.",
                                   "Sentence first part")
            Obj2 = text.sentence_obj_from_memory(Prg, "FileSourceBaseName2", 11, 2, 0, True,
                                   "Sentence first section, second part.",
                                   "second part.")

            Obj3 = text.sentence_obj_from_memory(Prg, "FileSourceBaseName1", 11, 1, 0, True,
                                   "Sentence first part, when subsentence length is equal with Obj1 but the main sentence is shorter.",
                                   "Sentence first part")

        WordsMaybeDetected = ["part"]
        self.maxDiff = None

        ResultsSelectedOrig = [Obj1, Obj2]
        Selected = result_selectors.short_sorter(dict(), ResultsSelectedOrig, WordsMaybeDetected)
        IdsSelectedSentences = [Sen.Id for Sen in Selected]
        self.assertEqual([Obj2.Id, Obj1.Id], IdsSelectedSentences)

        ResultsSelectedOrig = [Obj1, Obj2, Obj3]
        Selected = result_selectors.short_sorter(dict(), ResultsSelectedOrig, WordsMaybeDetected)
        IdsSelectedSentences = [Sen.Id for Sen in Selected]
        self.assertEqual([Obj2.Id, Obj3.Id, Obj1.Id], IdsSelectedSentences)

    def test_words_wanted_from_tokens(self):
        if self._test_exec("test_words_wanted_from_tokens"):
            Tokens = ["(", "apple", "AND", "orange", ")"]
            Words = tokens.words_wanted_collect(Tokens)
            self.assertEqual(Words, set(["apple", "orange"]))

    def test_word_group_collect(self):
        if self._test_exec("test_word_group_collect"):
            Words = ["apple", "orange", "grape"]
            Group = tokens.word_group_collect(Words)
            self.assertEqual(Group, ["(", "apple", "OR", "orange", "OR", "grape", ")"])

    def test_token_split(self):
        if self._test_exec("test_token_split"):
            Query = "like 1945"
            Wanted = ["like", "AND", "1945"]
            self.assertEqual(tokens.token_split__group_words_collect(Query), Wanted)

            Query = "(apple   house,mouse)"
            Wanted = ["(", "apple", "AND", "house", "AND", "mouse", ")"]
            self.assertEqual(tokens.token_split__group_words_collect(Query), Wanted)

            Query = "(every OR special) AND (events OR (bird OR audience))"
            TokensDetected = tokens.token_split__group_words_collect(Query)
            TokensWanted = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            self.assertEqual(TokensDetected, TokensWanted)

            Query = "birds (are OR  singing) AND (is)"
            TokensDetected = tokens.token_split__group_words_collect(Query)
            TokensWanted = ["birds", "AND", "(", "are", "OR", "singing", ")", "AND", "(", "is", ")"]
            self.assertEqual(TokensDetected, TokensWanted)

    def test_token_split_and(self):
        if self._test_exec("test_token_split_and"):
            Query = "apple  house"
            Wanted = ["apple", "AND", "house"]

            TokensDetected = tokens.token_split__group_words_collect(Query)
            self.assertEqual(TokensDetected, Wanted)

    def test_token_group_finder(self):
        if self._test_exec("test_token_group_finder"):
            Tokens = ["(", "every", "OR", "special", ")", "AND", "(", "events", "OR", "(", "bird", "OR", "audience", ")", ")"]
            TokenGroupsDetected = tokens.token_group_finder(Tokens)
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
                Tokens = tokens.token_split__group_words_collect(Query)
                TokenGroups = tokens.token_group_finder(Tokens)
                DocIndex = Prg["DocumentObjectsLoaded"]["test_document_bird"]["WordPosition"]

                Explains = []
                Result, ResultName = tokens.token_interpreter(TokenGroups, DocIndex, Explains)
                return Result, Explains

            if True:
                SubMulti = Prg["SubSentenceMultiplier"]
                WordMulti = Prg["WordPositionMultiplier"]
                PosCalc = util.sentence_subsentence_wordpos_calc
                # sentence_subsentence_wordpos_calc(SentenceNum, SubSentenceNum, Wordposition, SubSentenceMultiply, WordMultiply):

                Query = "are"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {1, PosCalc(2, 2, 1, SubMulti, WordMulti)}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('are', 2)]) # One Explain: ('Token', NumOfIndexElemsInDocIndex)

                Query = "birds"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 10003, 20002, 50007}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4)])

                Query = "is"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {40001, 20004, 40009, 9, 10102, 10107}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('is', 6)])

                Query = "strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {20005}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('strong', 1)])

                Query = "birds is"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 9, 20002, 20004} 
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('(birds AND is)', 4)])

                Query = "birds  is,strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {20002, 20004, 20005}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('strong', 1), ('(is AND strong)', 2), ('(birds AND (is AND strong))', 3)])

                Query = "(birds  is),strong"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {20002, 20004, 20005}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('(birds AND is)', 4), ('strong', 1), ('((birds AND is) AND strong)', 3)])

                Query = "(birds  is,are),(strong)"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = set()
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('are', 2), ('(is AND are)', 2), ('(birds AND (is AND are))', 3), ('strong', 1), ('((birds AND (is AND are)) AND strong)', 0)])

                ##### OR ######
                Query = "birds   OR  is"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 40001, 20002, 20004, 9, 40009, 10003, 10102, 50007, 10107}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('(birds OR is)', 10)])

                Query = "(((strong OR are)))"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {1, 20201, 20005} 
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('strong', 1), ('are', 2), ('(strong OR are)', 3)])

                Query = "(((strong OR are))) OR ()"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {1, 20005, 20201}
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
                ResultWanted = {20002, 20004, 20005}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('(birds OR is)', 10), ('strong', 1), ('((birds OR is) AND strong)', 3)])

                Query = "(birds   OR  is) AND (strong OR are)"
                Result, Explains = token_interpreter_wrapper(Prg, Query)
                ResultWanted = {0, 1, 20002, 20004, 20005, 9}
                self.assertEqual(Result, ResultWanted)
                self.assertEqual(Explains, [('birds', 4), ('is', 6), ('(birds OR is)', 10), ('strong', 1), ('are', 2), ('(strong OR are)', 3), ('((birds OR is) AND (strong OR are))', 6)])

            Query = "birds (are OR  singing) AND (is)"
            Result, Explains = token_interpreter_wrapper(Prg, Query)
            ResultWanted = {0, 1, 2, 9}
            self.assertEqual(Result, ResultWanted)
            self.assertEqual(Explains, [('birds', 4), ('are', 2), ('singing', 1), ('(are OR singing)', 3), ('is', 6), ('((are OR singing) AND is)', 3), ('(birds AND ((are OR singing) AND is))', 4)])

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

