# -*- coding: utf-8 -*-
import unittest, util_test
import tokens

class TokenTests(util_test.SentenceSeekerTest):

    def test_token_scope_modify(self):
        if self._test_exec("test_token_scope_modify"):

            SubSentenceMultiplier = 100
            WordMultiplier = 100

            Result = tokens.results_scope_modify({123456}, SubSentenceMultiplier, WordMultiplier, Scope="subsentence")
            Wanted = {1234}
            self.assertTrue(Result, Wanted)

            Result = tokens.results_scope_modify({123456}, SubSentenceMultiplier, WordMultiplier, Scope="sentence")
            Wanted = {12}
            self.assertTrue(Result, Wanted)

            Result = tokens.results_scope_modify({0, 20001, 100, 501214}, SubSentenceMultiplier, WordMultiplier, Scope="subsentence")
            Wanted = {0, 200, 1, 5012}
            self.assertTrue(Result, Wanted)

            Result = tokens.results_scope_modify({1, 20002, 101, 61234, 501215}, SubSentenceMultiplier, WordMultiplier, Scope="subsentence")
            Wanted = {0, 200, 1, 612, 5012}
            self.assertTrue(Result, Wanted)

    def test_select_in_scope(self):
        if self._test_exec("test_select_in_scope"):

            SubSentenceMulti = 100
            WordPositionMulti = 100
            Scope = "subsentence"

            # ResultsLeftScoped = {0, 1, 5012, 200}
            # ResultsRightScoped = {0, 1, 612, 200, 5012}
            ResultsLeft = {0, 20001, 100, 501214} 
            ResultsRight = {1, 20002, 101, 61234, 501215}
            ResultsScoped = {0, 1, 5012, 200} # after AND operator
            ValuesSelected = tokens.values_select_in_scope(ResultsScoped, ResultsLeft, ResultsRight, SubSentenceMulti, WordPositionMulti, Scope)

            ValuesWanted = {0, 1, 100, 101, 20001, 20002, 501214, 501215}
            self.assertEqual(ValuesSelected, ValuesWanted)

def run_all_tests(Prg):
    TokenTests.Prg = Prg
    unittest.main(module="test_tokens", verbosity=2, exit=False)

