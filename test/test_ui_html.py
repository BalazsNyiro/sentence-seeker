# -*- coding: utf-8 -*-
import unittest, util_test, ui_html, copy, seeker

class UiHtmlTest(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    # it works from documents_user_dir_simulator
    def test_ui_html(self):
        if self._test_exec("test_ui_html"):
            PrgOrig = copy.deepcopy(self.Prg)
            seeker.be_ready_to_seeking(self.Prg, Verbose=False)

            SeekResult = ui_html.one_search(self.Prg, "apple like")
            # this is the result for html ui
            Wanted = b'{"results": [{"FileSourceBaseName": "WilliamShakespeare__CompleteWorks__gutenberg_org_100-0", "LineNumInSentenceFile": 53830, "Sentence": "What, up and down, carv\\u2019d like an apple tart? \\n", "SentenceLen": 47, "SubSentenceLen": 29, "SubSentenceNums": [2], "SubSentenceNumMin": 2, "SubSentenceNumMax": 2, "WordNums": [4], "HitNum": 1}, {"FileSourceBaseName": "WilliamShakespeare__CompleteWorks__gutenberg_org_100-0", "LineNumInSentenceFile": 299, "Sentence": "How like Eve\\u2019s apple doth thy beauty grow, If thy sweet virtue answer not thy show. 94 \\n", "SentenceLen": 88, "SubSentenceLen": 41, "SubSentenceNums": [0], "SubSentenceNumMin": 0, "SubSentenceNumMax": 0, "WordNums": [4], "HitNum": 1}, {"FileSourceBaseName": "WilliamShakespeare__CompleteWorks__gutenberg_org_100-0", "LineNumInSentenceFile": 30161, "Sentence": "Shalt see thy other daughter will use thee kindly, for though she\\u2019s as like this as a crab\\u2019s like an apple, yet I can tell what I can tell. \\n", "SentenceLen": 141, "SubSentenceLen": 56, "SubSentenceNums": [1], "SubSentenceNumMin": 1, "SubSentenceNumMax": 1, "WordNums": [13], "HitNum": 1}], "token_process_explain": "Same sentences can be counted more than once from different results!<br />(apple AND like): 3<br />apple: 11<br />like: 1930<br /><br />", "words_detected": ["apple", "like"]}'
            self.assertEqual(SeekResult, Wanted)


            self.Prg = PrgOrig

def run_all_tests(Prg):
    UiHtmlTest.Prg = Prg
    unittest.main(module="test_ui_html", verbosity=2, exit=False)
