# -*- coding: utf-8 -*-
import unittest, text, util_test

class TextTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []


    def test_sentence_from_memory(self):
        if self._test_exec("test_sentence_from_memory"):
            Prg = {"DocumentObjectsLoaded": dict()}
            Source = "book"
            LineNum = 1

            Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum)
            self.assertFalse(Status)
            self.assertTrue("is not loaded" in Sentence)

            Prg = {"DocumentObjectsLoaded": {Source: dict()}}
            Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum)
            self.assertFalse(Status)
            self.assertTrue("no Sentences" in Sentence)

            Prg = {"DocumentObjectsLoaded": {Source: {"Sentences": "wrong type"}}}
            Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum)
            self.assertFalse(Status)
            self.assertTrue("incorrect type" in Sentence)

            Prg = {"DocumentObjectsLoaded": {Source: {"Sentences": []}}}
            Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum)
            self.assertFalse(Status)
            self.assertTrue("unknown linenum" in Sentence)

            Prg = {"DocumentObjectsLoaded": {Source: {"Sentences": ["", "  Second line.  "]}}}
            Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum)
            self.assertTrue(Status)
            self.assertEqual("  Second line.  ", Sentence)

            Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum, Strip=True)
            self.assertTrue(Status)
            self.assertEqual("Second line.", Sentence)

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

    def test_replaces(self):
        if self._test_exec("test_replaces"):
            Txt = "Small apples hide in the forest until animals eat them"

            Replaces = (
                ("Small", "Big"),
                ("animals", "people")
            )
            Replaced = text.replace_pairs(Txt, Replaces)
            self.assertEqual(Replaced, "Big apples hide in the forest until people eat them")

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

    def test_subsentences(self):
        if self._test_exec("test_subsentences"):
            Txt = 'I am angry; I have to know: Lisa and Pete lived in a big house, in Boston, did they?'
            Wanted = ['I am angry',
                      ' I have to know',
                      ' Lisa and Pete lived in a big house',
                      ' in Boston',
                      ' did they?']
            SubSentences = text.subsentences(Txt)
            self.assertEqual(Wanted, SubSentences)

def run_all_tests(Prg):
    TextTests.Prg = Prg
    unittest.main(module="test_text", verbosity=2, exit=False)

