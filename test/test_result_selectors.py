# -*- coding: utf-8 -*-
import unittest, util_test, result_selectors


class sample_obj():
    Id = 0
    def __init__(self, Sentence):
        self.Id = sample_obj.Id
        sample_obj.Id += 1
        self.Sentence = Sentence
        self.SentenceLen = len(Sentence)
        self.CharQuestionCounter = Sentence.count("?")
        self.CharSpaceCounter = Sentence.count(" ")

def member_ids(Groups, GrpNum):
    return [Obj.Id for Obj in Groups[GrpNum]]

###########################################################################
class SelectorTests(util_test.SentenceSeekerTest):

    TestsExecutedOnly = []
    def test_reach_the_deepest_lists_and_modify(self):
        if self._test_exec("test_reach_the_deepest_lists_and_modify"):

            Complex = [ [[[8,9]], [[7],[6]]],           [3,4,5], [1,2]     ]
            Simple = [1,2,3]

            def modify(_Prg, Group, Params):
                for Id in range(0, len(Group)):
                    Group[Id] = Group[Id] + Params["plus"]

            Params = {"plus": 20}

            result_selectors.reach_the_deepest_lists_and_modify(dict(), Simple, modify, Params)
            self.assertEqual([21, 22, 23], Simple)

            result_selectors.reach_the_deepest_lists_and_modify(dict(), Complex, modify, Params)
            ComplexWanted = [ [[[28,29]], [[27],[26]]],           [23,24,25], [21,22]     ]
            self.assertEqual(ComplexWanted, Complex)

    def test_objects_sort(self):
        if self._test_exec("test_objects_sort"):

            S0 = sample_obj("This is a sentence.")
            S1 = sample_obj("Jules Verne is one of the biggest Sci-fi writer")
            S2 = sample_obj("How can we clear the oceans?")
            S3 = sample_obj("Is this a sentence?")  # same length and other char attributes
            S4 = sample_obj("How can whales live in the deep ocean?")
            S5 = sample_obj("What do you do next weekend?") # same length with S3

            Groups = [S0, S1, S2, S3, S4, S5]

            result_selectors.obj_grouping(Groups, "SentenceLen")
            self.assertEqual([0, 3], member_ids(Groups, 0))
            self.assertEqual([2, 5], member_ids(Groups, 1))
            self.assertEqual([4], member_ids(Groups, 2))
            self.assertEqual([1], member_ids(Groups, 3))

            Groups = [S0, S1, S2, S3, S4, S5]
            result_selectors.obj_grouping(Groups, "CharSpaceCounter", Reverse=True)
            self.assertEqual([1], member_ids(Groups, 0))     # 8 spaces
            self.assertEqual([4], member_ids(Groups, 1))     # 7 spaces
            self.assertEqual([2, 5], member_ids(Groups, 2))  # 5 spaces
            self.assertEqual([0, 3], member_ids(Groups, 3))  # 3 spaces

            Groups = [S0, S1, S2, S3, S4, S5]
            result_selectors.obj_grouping(Groups, "CharQuestionCounter", Reverse=True)
            self.assertEqual([2, 3, 4, 5], member_ids(Groups, 0))
            self.assertEqual([0, 1], member_ids(Groups, 1))


    def test_result_selectors(self):
        if self._test_exec("test_result_selectors"):
            self.assertEqual(1, 1)

    # def test_result_selectors(self):
    #     if self._test_exec("test_result_selectors"):
    #         Prg = dict()
    #         Obj1 = text.sentence_obj_from_memory(Prg, "FileSourceBaseName1", 11, 1, 0, True,
    #                                              "Sentence first part, and the other very long subsentence with interesting words because the main sentence has to be very long.",
    #                                              "Sentence first part")
    #         Obj2 = text.sentence_obj_from_memory(Prg, "FileSourceBaseName2", 11, 2, 0, True,
    #                                              "Sentence first section, second part.",
    #                                              "second part.")

    #         Obj3 = text.sentence_obj_from_memory(Prg, "FileSourceBaseName1", 11, 1, 0, True,
    #                                              "Sentence first part, when subsentence length is equal with Obj1 but the main sentence is shorter.",
    #                                              "Sentence first part")

    #     WordsDetected = ["part"]
    #     self.maxDiff = None

    #     ResultsSelectedOrig = [Obj1, Obj2]
    #     Selected = result_selectors.sort_by_sentence_len(dict(), ResultsSelectedOrig, WordsDetected)
    #     IdsSelectedSentences = [Sen.Id for Sen in Selected]
    #     self.assertEqual([Obj2.Id, Obj1.Id], IdsSelectedSentences)

    #     ResultsSelectedOrig = [Obj1, Obj2, Obj3]
    #     Selected = result_selectors.sort_by_sentence_len(dict(), ResultsSelectedOrig, WordsDetected)
    #     IdsSelectedSentences = [Sen.Id for Sen in Selected]
    #     self.assertEqual([Obj2.Id, Obj3.Id, Obj1.Id], IdsSelectedSentences)


def run_all_tests(Prg):
    SelectorTests.Prg = Prg
    unittest.main(module="test_result_selectors", verbosity=2, exit=False)
