# -*- coding: utf-8 -*-
import unittest, util_test, util, os

class PathTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_2(self):
        if self._test_exec("test_2"):
            util.log(self.Prg, "test 2")

    def test_dir_create_if_necessary(self):
        if self._test_exec("test_dir_create_if_necessary"):
            Ret = util.dir_create_if_necessary(self.Prg, "src")
            self.assertEqual(True, "not created: dir exists" in Ret)

            Ret = util.dir_create_if_necessary(self.Prg, ".gitignore")
            self.assertEqual(True, "not created: it was a filename" in Ret)

            DirTryToMake = os.path.join(self.Prg["DirWork"], "TryToMakeThis")
            util.dir_delete_if_exist(self.Prg, DirTryToMake, Print=True)
            Ret = util.dir_create_if_necessary(self.Prg, DirTryToMake)
            self.assertEqual(True, "" in Ret)
            util.dir_delete_if_exist(self.Prg, DirTryToMake, Print=True)

def run_all_tests(Prg):
    PathTests.Prg = Prg
    unittest.main(module="test_util", verbosity=2, exit=False)
