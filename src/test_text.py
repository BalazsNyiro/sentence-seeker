# -*- coding: utf-8 -*-
import unittest, text, util_test

class TextTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    def test_remove_not_abc_chars(self):
        if self._test_exec("test_remove_not_abc_chars"):
            TextOrig = "[pine;a'pp_le\n!-cliché0123456789"
            TextNew = text.remove_non_alpha_chars(TextOrig, CharsKeepThem="-")
            self.assertEqual(TextNew, "pineapple-cliché0123456789")

            TextNew = text.remove_non_alpha_chars(TextOrig, "_", CharsKeepThem="-")
            self.assertEqual(TextNew, "_pine_a_pp_le__-cliché0123456789")

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

    def test_word_highlight(self):
        self.maxDiff = None
        if self._test_exec("test_word_highlight"):
            # Prg = self.Prg
            Text = "Apple has a lot of apple in his Tree garden"
            Words = ["apple", "tree"]
            Highlighted = text.word_highlight(Words, Text)

            TextWanted = ">>Apple<< has a lot of >>apple<< in his >>Tree<< garden"
            self.assertEqual(Highlighted, TextWanted)

    def test_sentence_separator(self): # replace_abbreviations uses text_replace()
        self.maxDiff = None
        if self._test_exec("test_sentence_separator"):
            Txt = 'Mr. and Mrs. Jones visited their friends... "Lisa and Pete lived in a big house, in Boston, did they?"  Yes, they did'
            Wanted = \
                ["Mr and Mrs Jones visited their friends...",
                 '"Lisa and Pete lived in a big house, in Boston, did they?"',
                 "Yes, they did"]
            Sentences = text.sentence_separator(Txt)
            self.assertEqual(Wanted, Sentences)


def run_all_tests(Prg):
    TextTests.Prg = Prg
    unittest.main(module="test_text", verbosity=2, exit=False)

