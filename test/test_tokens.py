# -*- coding: utf-8 -*-
import unittest, util_test
import tokens
import time, copy, seeker
# For speed tests, slow queries:
# 'not seemed to be'

from tokens import TokenObj

class TokenTests(util_test.SentenceSeekerTest):

    def test_tokens_find_leaf_tests(self):
        if self._test_exec("test_tokens_find_leaf_tests"):
            PrgOrig = copy.deepcopy(self.Prg)
            seeker.be_ready_to_seeking(self.Prg, Verbose=False)

            ProgressBarConsole = None
            Index = self.Prg["DocumentObjectsLoaded"]["WilliamShakespeare__CompleteWorks__gutenberg_org_100-0"]["WordPosition"]

            if True:
                # =================================================
                Tokens = [TokenObj("apple", Index)]
                tokens.operator_exec(Tokens)

                ResultWanted = [2990004, 301610113, 334040104, 370530102, 409740202, 537520004, 538300204, 547420107, 612450404, 625760001]
                ResultsCollected = Tokens[0].get_results()
                self.assertEqual(ResultWanted, ResultsCollected)
                # =================================================

                Tokens = [TokenObj("apple", Index), TokenObj("AND"), TokenObj("like", Index)]
                tokens.operator_exec(Tokens)

                ResultWanted = [2990004, 301610113, 538300204]
                ResultsCollected = Tokens[0].get_results()
                self.assertEqual(ResultWanted, ResultsCollected)

                # =================================================
                Tokens = [[TokenObj("apple", Index), TokenObj("AND"), TokenObj("like", Index)], TokenObj("AND"), TokenObj("tart", Index)]
                tokens.operator_exec(Tokens)

                ResultWanted = [538300204]
                ResultsCollected = Tokens[0].get_results()
                self.assertEqual(ResultWanted, ResultsCollected)

                # =================================================
                Tokens = [TokenObj("apple", Index), TokenObj("OR"), TokenObj("walking", Index)]
                tokens.operator_exec(Tokens)

                ResultToken = Tokens[0]
                ResultWanted = [2990004, 35130002, 149160214, 156400100, 191290111, 217380205, 228130100, 281880705,
                                282310104, 301610113, 307490103, 334040104, 348860102, 350440004, 370530102, 409740202,
                                418520100, 441190103, 477380406, 506270402, 537520004, 538300204, 540120201, 547420107,
                                612450404, 625760001, 641530203]
                self.assertEqual(ResultWanted, ResultToken.get_results())

                TokenApple = ResultToken.Explain[0] # from Explain
                ResultWanted = [2990004, 301610113, 334040104, 370530102, 409740202, 537520004, 538300204, 547420107, 612450404, 625760001]
                self.assertEqual(ResultWanted, TokenApple.get_results())

                TokenWalking = ResultToken.Explain[2] # from Explain
                ResultWanted = [35130002, 149160214, 156400100, 191290111, 217380205, 228130100, 281880705, 282310104,
                                307490103, 348860102, 350440004, 418520100, 441190103, 477380406, 506270402, 540120201, 641530203]
                self.assertEqual(ResultWanted, TokenWalking.get_results())
                # =================================================




            # =================================================
            Tokens = [TokenObj("raining", Index), TokenObj("OR"), TokenObj("located", Index)]
            tokens.operator_exec(Tokens)

            ResultWanted = [30004, 30113, 336371700, 674870904, 676760505, 677640403, 681870016, 681910009, 681980004, 681980113]
            ResultsCollected = Tokens[0].get_results()
            # print(">>>>>>", ResultsCollected)
            self.assertEqual(ResultWanted, ResultsCollected)


            # =================================================
            Tokens = [[TokenObj("raining", Index), TokenObj("OR"), TokenObj("located", Index)], TokenObj("OR"), TokenObj("january", Index)]
            tokens.operator_exec(Tokens)

            ResultWanted = [30004, 30113, 40300, 336371700, 417250104, 664630008, 674870904, 676760505, 677640403, 681870016, 681910009, 681980004, 681980113]
            ResultsCollected = Tokens[0].get_results()
            # print(">>>>>> or 3 elem: ", ResultsCollected)
            self.assertEqual(ResultWanted, ResultsCollected)

            # =================================================
            Tokens = [[[TokenObj("reading", Index)]]] # triple embedded group
            tokens.operator_exec(Tokens)
            ResultWanted = [8660103, 17690203, 26300100, 39430401, 55290100, 55500100, 56390010, 103280003, 106060002, 127410100, 127420008, 150260100, 182990403, 254540006, 254900108, 259100100, 285090100, 292450210, 298080004, 318910103, 327310301, 339320100, 416960200, 422130102, 424280605, 427130103, 461060002, 598470004, 598500003, 616850006, 629060004, 635530007, 671880302, 681760001]
            ResultsCollected = Tokens[0].get_results()
            self.assertEqual(ResultWanted, ResultsCollected)
            ###################################

            self.Prg = PrgOrig

def run_all_tests(Prg):
    TokenTests.Prg = Prg
    unittest.main(module="test_tokens", verbosity=2, exit=False)

