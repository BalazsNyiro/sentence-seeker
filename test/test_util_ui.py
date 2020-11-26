# -*- coding: utf-8 -*-
import unittest, util_test, util_ui

class UtilTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_sentence_convert_to_rows(self):
        if self._test_exec("test_sentence_convert_to_rows"):
            Sentence = "How many rows does it have if I use a really lengthened sentence like this one?"
            WantedRows = ["How many rows does",
                          "it have if I use a",
                          "really lengthened",
                          "sentence like this",
                          "one?"]

            SentenceObj = util_ui.SentenceObj(Sentence)
            RenderedRows = SentenceObj.render_console(20)
            self.assertEqual(WantedRows, RenderedRows)

def run_all_tests(Prg):
    UtilTests.Prg = Prg
    unittest.main(module="test_util_ui", verbosity=2, exit=False)
