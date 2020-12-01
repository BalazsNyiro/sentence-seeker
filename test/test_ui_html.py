# -*- coding: utf-8 -*-
import unittest, util_test, ui_html

class UiHtmlTest(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    # it works from documents_user_dir_simulator
    def test_ui_html(self):
        if self._test_exec("test_ui_html"):
            SeekResult = ui_html.one_search(self.Prg, "apple")
            # this is the result for html ui
            Wanted = b'{"results": [{"FileSourceBaseName": "apple_tree", "LineNumInSentenceFile": 0, "Sentence": "Way up high in the apple tree, Two little apples smiled at me. \\n", "SentenceLen": 64, "SubSentenceLen": 29, "SubSentenceNums": [0], "SubSentenceNumMin": 0, "SubSentenceNumMax": 0, "WordNums": [5]}], "token_process_explain": "apple: 1<br /><br />", "words_maybe_detected": ["apple"]}'
            self.assertEqual(SeekResult, Wanted)

def run_all_tests(Prg):
    UiHtmlTest.Prg = Prg
    unittest.main(module="test_ui_html", verbosity=2, exit=False)
