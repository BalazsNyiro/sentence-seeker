# -*- coding: utf-8 -*-
import unittest, text, util_test

class TextTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []

    def test_word_wanted(self):
        if self._test_exec("test_word_wanted"):
            self.assertFalse(text.word_wanted("apple(carrot"))
            self.assertFalse(text.word_wanted("Apple"))
            self.assertFalse(text.word_wanted("apPle"))
            self.assertFalse(text.word_wanted("APPLE"))
            self.assertFalse(text.word_wanted("apple!"))
            self.assertTrue(text.word_wanted("small0eng1chars2and3numbers4only"))

    # return with a Status and an Object.
    # The Object haas a fix structure, Status can be True/False
    def test_result_obj_from_memory(self):
        if self._test_exec("test_result_obj_from_memory"):
            Prg = {}
            FileSourceBaseName = "Filename"
            LineNumInSentenceFile = 1
            SubSentenceNum = 2
            WordNum = 0

            Obj = text.sentence_obj_from_memory(Prg,
                                                FileSourceBaseName,
                                                LineNumInSentenceFile, SubSentenceNum, WordNum,
                                                SentenceFillInResult=False)
            ObjWanted = {'FileSourceBaseName': 'Filename',
                         'LineNumInSentenceFile': 1,
                         'Sentence': '-',
                         'SentenceLen': 33,
                         'SubSentenceLen': 1,
                         'SubSentenceNums': {2},
                         'SubSentenceNumMin': 2,
                         'SubSentenceNumMax': 2,
                         'WordNums': {0},
                         'HitNum': 1
                         }

            ObjRepresentedAsDict = Obj.represent_as_dict()
            self.assertEqual(ObjWanted, ObjRepresentedAsDict)

            Prg = {"DocumentObjectsLoaded":
                    {"Filename":
                      {"Sentences": ["Sentence0",
                                     "This is the second, best subsentence, in test files"]
                      }
                    }
                  }
            FileSourceBaseName = "Filename"
            LineNumInSentenceFile = 1
            SubSentenceNum = 2
            WordNum = 0

            Obj = text.sentence_obj_from_memory(Prg,
                                                FileSourceBaseName,
                                                LineNumInSentenceFile, SubSentenceNum, WordNum,
                                                SentenceFillInResult=False)
            ObjWanted = {'FileSourceBaseName': 'Filename',
                         'LineNumInSentenceFile': 1,
                         'Sentence': '-',
                         'SentenceLen': 51,
                         'SubSentenceLen': 14,
                         'SubSentenceNums': {2},
                         'SubSentenceNumMin': 2,
                         'SubSentenceNumMax': 2,
                         'WordNums': {0},
                         'HitNum': 1
                        }
            self.assertEqual(ObjWanted, Obj.represent_as_dict())

    def test_only_subsentence_num__and__wordnum(self):
        if self._test_exec("test_only_subsentence_num__and__wordnum"):
            SubSentenceNum, WordNum = text.only_subsentence_num__and__wordnum(0)
            self.assertEqual(SubSentenceNum, 0)
            self.assertEqual(WordNum, 0)

            SubSentenceNum, WordNum = text.only_subsentence_num__and__wordnum(9)
            self.assertEqual(SubSentenceNum, 0)
            self.assertEqual(WordNum, 9)

            SubSentenceNum, WordNum = text.only_subsentence_num__and__wordnum(99)
            self.assertEqual(SubSentenceNum, 0)
            self.assertEqual(WordNum, 99)

            SubSentenceNum, WordNum = text.only_subsentence_num__and__wordnum(876)
            self.assertEqual(SubSentenceNum, 8)
            self.assertEqual(WordNum, 76)

            SubSentenceNum, WordNum = text.only_subsentence_num__and__wordnum(1876)
            self.assertEqual(SubSentenceNum, 18)
            self.assertEqual(WordNum, 76)

    def test_linenum_subsentencenum_get(self):
        if self._test_exec("test_linenum_subsentencenum_get"):
            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(0)
            self.assertEqual(LineNum, 0)
            self.assertEqual(SubSentenceNum, 0)
            self.assertEqual(WordNum, 0)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(5)
            self.assertEqual(LineNum, 0)
            self.assertEqual(SubSentenceNum, 0)
            self.assertEqual(WordNum, 5)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(50)
            self.assertEqual(LineNum, 0)
            self.assertEqual(SubSentenceNum, 0)
            self.assertEqual(WordNum, 50)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(102)
            self.assertEqual(LineNum, 0)
            self.assertEqual(SubSentenceNum, 1)
            self.assertEqual(WordNum, 2)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(987)
            self.assertEqual(LineNum, 0)
            self.assertEqual(SubSentenceNum, 9)
            self.assertEqual(WordNum, 87)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(9985)
            self.assertEqual(LineNum, 0)
            self.assertEqual(SubSentenceNum, 99)
            self.assertEqual(WordNum, 85)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(23456)
            self.assertEqual(LineNum, 2)
            self.assertEqual(SubSentenceNum, 34)
            self.assertEqual(WordNum, 56)

            LineNum, SubSentenceNum, WordNum = text.linenum_subsentencenum_wordnum_get(1234567)
            self.assertEqual(LineNum, 123)
            self.assertEqual(SubSentenceNum, 45)
            self.assertEqual(WordNum, 67)

    def test_char_add_into_sentence(self): #
        if self._test_exec("test_char_add_into_sentence"):

            Sentences, Sentence, InSentence = [], [], True
            Char, CharLast = "A", False
            Sentences, Sentence, InSentence = text.char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast)
            self.assertEqual(Sentences, [])
            self.assertEqual(Sentence, ["A"])
            self.assertEqual(InSentence, True)

            Sentences, Sentence, InSentence = [list("prev sen")], [], False
            Char, CharLast = "t", False
            Sentences, Sentence, InSentence = text.char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast)
            self.assertEqual(Sentences, [list("prev sent")])
            self.assertEqual(Sentence, [])
            self.assertEqual(InSentence, False)

            Sentences, Sentence, InSentence = [], [], False
            Char, CharLast = "A", False
            Sentences, Sentence, InSentence = text.char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast)
            self.assertEqual(Sentences, [])
            self.assertEqual(Sentence, ["A"])
            self.assertEqual(InSentence, True)

            Sentences, Sentence, InSentence = [list("prev sen")], ["W","h","y"], True
            Char, CharLast = "?", False
            Sentences, Sentence, InSentence = text.char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast)
            self.assertEqual(Sentences, [list("prev sen"), list("Why?")])
            self.assertEqual(Sentence, [])
            self.assertEqual(InSentence, False)

            Sentences, Sentence, InSentence = [list("prev sen")], ["W","h"], True
            Char, CharLast = "y", False
            Sentences, Sentence, InSentence = text.char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast)
            self.assertEqual(Sentences, [list("prev sen")])
            self.assertEqual(Sentence, ["W","h","y"])
            self.assertEqual(InSentence, True)

            Sentences, Sentence, InSentence = [list("prev sen")], ["W","h"], True
            Char, CharLast = "y", True
            Sentences, Sentence, InSentence = text.char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast)
            self.assertEqual(Sentences, [list("prev sen"), list("Why")])
            self.assertEqual(Sentence, [])
            self.assertEqual(InSentence, False)


    def test_inquotation_detect(self):
        if self._test_exec("test_inquotation_detect"):
            InSentence, InQuotation = text.quotation_sentence_starts("a", InSentence=False, InQuotation=False)
            self.assertEqual((InSentence, InQuotation), (False, False))

            InSentence, InQuotation = text.quotation_sentence_starts("a", InSentence=True, InQuotation=False)
            self.assertEqual((InSentence, InQuotation), (True, False))

            InSentence, InQuotation = text.quotation_sentence_starts('"', InSentence=False, InQuotation=False)
            self.assertEqual((InSentence, InQuotation), (True, True))

            InSentence, InQuotation = text.quotation_sentence_starts('"', InSentence=True, InQuotation=False)
            self.assertEqual((InSentence, InQuotation), (True, True))

            InSentence, InQuotation = text.quotation_sentence_starts('"', InSentence=True, InQuotation=True)
            self.assertEqual((InSentence, InQuotation), (True, False))

            InSentence, InQuotation = text.quotation_sentence_starts('A', InSentence=False, InQuotation=False)
            self.assertEqual((InSentence, InQuotation), (True, False))

            InSentence, InQuotation = text.quotation_sentence_starts('A', InSentence=True, InQuotation=False)
            self.assertEqual((InSentence, InQuotation), (True, False))

            InSentence, InQuotation = text.quotation_sentence_starts('A', InSentence=True, InQuotation=True)
            self.assertEqual((InSentence, InQuotation), (True, True))

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

    def test_sentence_separator(self): # replace_abbreviations uses text_replace()
        self.maxDiff = None
        if self._test_exec("test_sentence_separator"):
            Txt = 'Mr. and Mrs. Jones visited their friends... "Lisa and Pete lived in a big house, in Boston, did they?"  Yes, they did'
            Wanted = \
                ["Mr and Mrs Jones visited their friends... ",
                 '"Lisa and Pete lived in a big house, in Boston, did they?" ',
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
            Status, SubSentences = text.subsentences(Sentence=Txt)
            self.assertEqual((True, Wanted), (Status, SubSentences))

            # 0 is special id, because 'if 0' == False, we have to use 'if id is not none' in code
            self.assertEqual((True, 'I am angry'), text.subsentences(None, Txt, 0))

            self.assertEqual((True, ' in Boston'), text.subsentences(None, Txt, 3))
            self.assertEqual((False, ["subsentence 33 id is missing"]), text.subsentences(None, Txt, 33))

            Txt = 'I am angry; I have to know: Lisa and Pete lived in a big house, in Boston, did they?'
            Wanted = ['I am angry;',
                      ' I have to know:',
                      ' Lisa and Pete lived in a big house,',
                      ' in Boston,',
                      ' did they?']
            Status, SubSentences = text.subsentences(Sentence=Txt, KeepSubsentenceEnd=True)
            self.assertEqual((True, Wanted), (Status, SubSentences))

def run_all_tests(Prg):
    TextTests.Prg = Prg
    unittest.main(module="test_text", verbosity=2, exit=False)

