# -*- coding: utf-8 -*-
import unittest, util_test, os, util_json_obj, util

class UtilJsonTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_doc_db_update_in_file_and_Prg(self):
        if self._test_exec("test_doc_db_update_in_file_and_Prg"):
            Prg = self.Prg

            PrgFake = {}
            PrgFake["DocumentsSourceWebpagesFileName"] = os.path.join(Prg["DirWork"], "test_doc_update.json")
            PrgFake["DocumentsSourceWebpagesFileContent"] = ""

            util.file_write_simple(PrgFake["DocumentsSourceWebpagesFileName"], '{"key":"val"}')

            DocObj = {"name": "doc_update_test"}
            util_json_obj.doc_source_webpages_update_in_file_and_Prg(PrgFake, "sample_filename_without_extension", DocObj)

            _Status, DocObjUpdatedFromFile = util_json_obj.obj_from_file(PrgFake["DocumentsSourceWebpagesFileName"])
            self.assertTrue("docs" in DocObjUpdatedFromFile)
            self.assertTrue("sample_filename_without_extension" in DocObjUpdatedFromFile["docs"])
            self.assertEqual(DocObjUpdatedFromFile["docs"]["sample_filename_without_extension"]["name"], "doc_update_test")

            self.assertEqual(PrgFake["DocumentsSourceWebpages"], DocObjUpdatedFromFile["docs"])
            self.assertEqual(PrgFake["DocumentsSourceWebpagesFileContent"],
                             util_json_obj.json_to_str(DocObjUpdatedFromFile)
            )

            util_json_obj.doc_source_webpages_update_in_file_and_Prg(PrgFake, BaseNameNoExtRemove="sample_filename_without_extension")
            _Status, DocObjUpdatedFromFile = util_json_obj.obj_from_file(PrgFake["DocumentsSourceWebpagesFileName"])
            self.assertFalse("sample_filename_without_extension" in DocObjUpdatedFromFile["docs"])


            util.file_del(PrgFake["DocumentsSourceWebpagesFileName"])

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

