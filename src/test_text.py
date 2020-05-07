# -*- coding: utf-8 -*-
import unittest, text, util_test

class TextTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    def test_remove_not_abc_chars(self):
        if self._test_exec("test_remove_not_abc_chars"):
            TextOrig = "[pine;a'pp_le\n!-cliché"
            TextNew = text.remove_not_alpha_chars(TextOrig, CharsKeepThem="-")
            self.assertEqual(TextNew, "pineapple-cliché")

            TextNew = text.remove_not_alpha_chars(TextOrig, "_", CharsKeepThem="-")
            self.assertEqual(TextNew, "_pine_a_pp_le__-cliché")

    def test_text_replace(self): # replace_abbreviations uses text_replace()
        if self._test_exec("test_text_replace"):
            TextOrig = "Mr. and Mrs. Jones"
            TextNew = text.replace_abbreviations(TextOrig)
            self.assertEqual(TextNew, "Mr and Mrs Jones")


    # html_tags_remove() uses replace_regexp()
    def test_replace_regexp(self):
        if self._test_exec("test_replace_regexp"):
            TextOrig = '<a href="something">plain text</a>'
            TextCleaned = text.html_tags_remove(TextOrig)
            self.assertEqual(TextCleaned, "plain text")

            Pattern = "[ ]+(.*?p)"
            TextCleaned = text.replace_regexp("alma    repa", Pattern, r"_\1_")
            self.assertEqual(TextCleaned, "alma_rep_a")

            Text = "apple    \t\t\nmelon"
            self.assertEqual("apple melon", text.replace_whitespaces_to_one_space(Text))

def run_all_tests(Prg):
    TextTests.Prg = Prg
    unittest.main(module="test_text", verbosity=2, exit=False)

