# -*- coding: utf-8 -*-
import unittest, util_test, util, os, time, document

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
            DocumentsAvailable = document.document_objects_collect_from_dir_documents(Prg)

            self.assertIn(util.filename_without_extension(FileName), DocumentsAvailable)
            util.file_del(FilePath)

    def test_docs_copy_samples_into_dir(self):
        if self._test_exec("test_collect_docs_from_working_dir"):
            Prg = self.Prg

            DirTestBaseName = "test_" + str(int(time.time()))
            DirTest = os.path.join(Prg["DirWork"], DirTestBaseName)
            util.dir_create_if_necessary(Prg, DirTest)

            document.docs_copy_samples_into_dir(Prg, DirTest)
            Files = util.files_abspath_collect_from_dir(DirTest)
            FileNamesInOneLine = " ".join(Files)
            Wanted = "DanielDefoe__LifeAdventuresRobinsonCrusoe__gutenberg_org_521-0.txt"
            self.assertIn(Wanted, FileNamesInOneLine)

            for FileAbsPath in Files:
                util.file_del(FileAbsPath)

            DelRes = util.dir_delete_if_exist(Prg, DirTest)
            self.assertEqual("deleted", DelRes)

def run_all_tests(Prg):
    DocumentTests.Prg = Prg
    unittest.main(module="test_document", verbosity=2, exit=False)

