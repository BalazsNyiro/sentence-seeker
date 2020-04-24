# -*- coding: utf-8 -*-
import unittest, util_test, document, util, os

class DocumentTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_collect_docs_from_working_dir(self):
        if self._test_exec("test_collect_docs_from_working_dir"):
            Prg = self.Prg

            FileName = "test_file_document_example.txt"
            FilePath = os.path.join(Prg["DirDocuments"], FileName)
            util.file_del(FilePath)
            util.file_write(Prg, Fname=FilePath, Content="example text")
            DocumentsAvailable = document.collect_docs_from_working_dir(Prg)

            self.assertIn(FileName, DocumentsAvailable)
            util.file_del(FilePath)

def run_all_tests(Prg):
    DocumentTests.Prg = Prg
    unittest.main(module="test_document", verbosity=2, exit=False)

