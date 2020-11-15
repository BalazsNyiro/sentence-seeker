# -*- coding: utf-8 -*-
import unittest, util_test, util_ui

class UtilTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_sentence_convert_to_rows(self):
        if self._test_exec("test_sentence_convert_to_rows"):
            SentencesColored = ["How many rows does it have if I use a really lengthened sentence like this one?"]
            SentencesNotColored = SentencesColored

            WantedRows = ["How many rows does\n"
                          "it have if I use a\n"
                          "really lengthened\n"
                          "sentence like this\n"
                          "one?"]
            ReceivedRows = util_ui.text_split_at_screensize(SentencesColored, SentencesNotColored, 20, 30)
            self.assertEqual(WantedRows, ReceivedRows)

            SentencesColored  = ["What\nif we have directly inserted\nnewline\nchars in the text?"]
            SentencesNotColored = SentencesColored
            WantedRows = ['What\nif we have\ndirectly\ninserted\nnewline\nchars in\nthe text?']
            ReceivedRows = util_ui.text_split_at_screensize(SentencesColored, SentencesNotColored, 10, 30)
            self.assertEqual(WantedRows, ReceivedRows)

def run_all_tests(Prg):
    UtilTests.Prg = Prg
    unittest.main(module="test_util_ui", verbosity=2, exit=False)
