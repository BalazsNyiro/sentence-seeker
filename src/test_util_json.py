# -*- coding: utf-8 -*-
import unittest, util_test, os, util_json_obj, util

class UtilJsonTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_json_read_write_from_file(self):
        if self._test_exec("test_json_read_write_from_file"):
            Prg = self.Prg
            Fname = os.path.join(Prg["DirWork"], "test_json_obj.txt")
            util.file_del(Fname)

            ObjExample = {"keyword": "value", "number": 1}
            util_json_obj.obj_to_file(Fname, ObjExample)

            _Status, ObjFromFile = util_json_obj.obj_from_file(Fname)
            self.assertEqual(ObjFromFile, ObjExample)

            util.file_del(Fname)

def run_all_tests(Prg):
    UtilJsonTests.Prg = Prg
    unittest.main(module="test_util_json", verbosity=2, exit=False)

