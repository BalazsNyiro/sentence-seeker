# -*- coding: utf-8 -*-
import unittest, util_test, util, os

class UtilTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_file_create_if_necessary(self):
        if self._test_exec("test_file_write_append_del"):
            Prg = self.Prg
            Fname = os.path.join(Prg["DirWork"], "test_file_create_if_necessary.txt")
            util.file_del(Fname)
            Created = util.file_create_if_necessary(Prg, Fname, ContentDefault="cloud")
            self.assertTrue(Created)

            RetRead, ContentRead = util.file_read_all(Prg, Fname)
            self.assertEqual(ContentRead, "cloud")

            util.file_del(Fname)

    def test_file_write_append_del(self):
        if self._test_exec("test_file_write_append_del"):
            Prg = self.Prg

            Ret = util.file_write(Prg, Fname="")
            self.assertFalse(Ret)

            Content = "apple "
            Fname = os.path.join(Prg["DirWork"], "test_file_write.txt")
            RetWrite = util.file_write(Prg, Fname=Fname, Content=Content)
            RetAppend = util.file_append(Prg, Fname=Fname, Content="tree")
            self.assertTrue(RetWrite)
            self.assertTrue(RetAppend)
            RetRead, ContentRead = util.file_read_all(Prg, Fname)

            self.assertTrue(RetRead)
            self.assertEqual(ContentRead, "apple tree")

            FileState, FileGzipped = util.file_is_gzipped(Prg, Fname)
            self.assertEqual("file_exists", FileState)
            self.assertEqual("not_gzipped", FileGzipped)

            RetWriteGz = util.file_write(Prg, Fname=Fname, Content="gzipped", Gzipped=True)
            self.assertTrue(RetWriteGz)
            RetReadGz, ContentReadGz = util.file_read_all(Prg, Fname, Gzipped=True)
            self.assertTrue(RetReadGz)
            self.assertEqual(ContentReadGz, b"gzipped")

            FileState, FileGzipped = util.file_is_gzipped(Prg, Fname)
            self.assertEqual("file_exists", FileState)
            self.assertEqual("gzipped", FileGzipped)

            RetDel1 = util.file_del(Fname)
            RetDel2 = util.file_del(Fname)
            self.assertTrue(RetDel1)
            self.assertFalse(RetDel2)

            FileState, FileGzipped = util.file_is_gzipped(Prg, Fname)
            self.assertEqual("file_not_found", FileState)
            self.assertEqual("", FileGzipped)

    def test_dir_create_if_necessary(self):
        if self._test_exec("test_dir_create_if_necessary"):
            Prg = self.Prg
            Ret = util.dir_create_if_necessary(Prg, os.path.join(Prg["DirPrgRoot"], "src"))
            self.assertEqual(True, "not created: dir exists" in Ret)

            Ret = util.dir_create_if_necessary(Prg, os.path.join(Prg["DirPrgRoot"], ".gitignore"))
            self.assertEqual(True, "not created: it was a filename" in Ret)

            DirTryToMake = os.path.join(Prg["DirWork"], "TryToMakeThis")
            util.dir_delete_if_exist(Prg, DirTryToMake, Print=True)
            Ret = util.dir_create_if_necessary(Prg, DirTryToMake)
            self.assertEqual(True, "" in Ret)
            util.dir_delete_if_exist(Prg, DirTryToMake, Print=True)

def run_all_tests(Prg):
    UtilTests.Prg = Prg
    unittest.main(module="test_util", verbosity=2, exit=False)
