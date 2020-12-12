# -*- coding: utf-8 -*-
import unittest, eng, util_test, document

class EngTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []

    def test_word_wanted(self):
        if self._test_exec("test_word_wanted"):
            self.assertFalse(eng.selector_word_end("house", "ing"))
            self.assertTrue(eng.selector_word_end("reading", "ing"))

    def test_word_selecting_grouping(self):
        if self._test_exec("test_word_selecting_grouping"):
            PrgFake = {"DocumentObjectsLoaded": {
                "doc1": document.document_obj(WordPositionInLines={"read": [1, 2000],
                                                                   "reading": [3, 333]}),
                "doc2": document.document_obj(WordPositionInLines={"write": [4, 400000],
                                                                   "writing": [44, 4444],
                                                                   "any": [1, 2]})
                },
                "CacheWordGroups": dict()
            }
            Selector = eng.selector_word_include
            Received = eng.word_selecting(PrgFake, Selector, "ead")
            Wanted = set(["reading", "read"])
            self.assertEqual(Received, Wanted)

            Selector = eng.selector_word_start
            Received = eng.word_selecting(PrgFake, Selector, "r")
            Wanted = set(["reading", "read"])
            self.assertEqual(Received, Wanted)

            Selector = eng.selector_word_end
            Received = eng.word_selecting(PrgFake, Selector, "ing")
            Wanted = set(["reading", "writing"])
            self.assertEqual(Received, Wanted)

            def pattern_in_word(Word, StrSeek):
                return StrSeek in Word

            Selector = pattern_in_word
            Received = eng.word_selecting(PrgFake, Selector, "r")
            Wanted = set(["reading", "writing", "read", "write"])
            self.assertEqual(Received, Wanted)

            Wanted = set(["write"])
            Received = eng.groups_of_word_ending(PrgFake, "te")
            self.assertEqual(Received, Wanted)

            Wanted = set(["any"])
            Received = eng.groups_of_word_starting(PrgFake, "an")
            self.assertEqual(Received, Wanted)

            Wanted = set(["read", "reading", "write", "writing"])
            Received = eng.groups_of_word_include(PrgFake, "r")
            self.assertEqual(Received, Wanted)

            Wanted = set()
            Received = eng.groups_of_word_include(PrgFake, "unknown_pattern")
            self.assertEqual(Received, Wanted)

def run_all_tests(Prg):
    EngTests.Prg = Prg
    unittest.main(module="test_eng", verbosity=2, exit=False)

