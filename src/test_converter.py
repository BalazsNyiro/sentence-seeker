# -*- coding: utf-8 -*-
import unittest, util_test, util, os

class ConverterTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_fun_pdf_to_text_converter(self):
        if self._test_exec("test_fun_pdf_to_text_converter"):
            Prg = self.Prg
            FileTxt = os.path.join(Prg["DirWork"], "test_converted_from_pdf.txt")
            util.file_del(FileTxt)
            FilePdf = os.path.join(Prg["DirTestFiles"], "test_pdf_conversion.pdf")
            Prg["PdfToTextConvert"](FilePdf, FileTxt)
            FileLines = util.file_read_lines(Prg, FileTxt, Strip=True)
            self.assertEqual(FileLines[0], "This is new document.")
            util.file_del(FileTxt)

def run_all_tests(Prg):
    ConverterTests.Prg = Prg
    unittest.main(module="test_converter", verbosity=2, exit=False)
