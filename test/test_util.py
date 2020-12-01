# -*- coding: utf-8 -*-
import unittest, util_test, util, os

class UtilTests(util_test.SentenceSeekerTest):
    TestsExecutedOnly = []
    #TestsExecutedOnly = [""]

    def test_sentence_subsentence_wordpos_calc(self):
        if self._test_exec("test_sentence_subsentence_wordpos_calc"):
            Wanted = 200304
            Result = util.sentence_subsentence_wordpos_calc(2, 3, 4, 1000, 100)
            self.assertEqual(Wanted, Result)

    def test_count_words_with_numbers(self):
        if self._test_exec("test_count_words_with_numbers"):
            Sentence = "apple, banana5, 1 Thesaurus bird"
            WordsHasNum, WordsWithoutNum = util.count_words_with_num(Sentence)
            self.assertEqual(WordsWithoutNum, 3)
            self.assertEqual(WordsHasNum, 2)

    def test_dict_value_insert_into_key_group(self):
        if self._test_exec("test_dict_value_insert_into_key_group"):
            Dict = {}
            util.dict_value_insert_into_key_group(Dict, "Group", 1)
            util.dict_value_insert_into_key_group(Dict, "Group", 2)
            self.assertEqual(Dict["Group"], [1, 2])

    def test_util_dict_key_sorted(self):
        if self._test_exec("test_util_dict_key_sorted"):
            Dict = {"Aphrodite": 0, "Zeus": 2, "Xena": 1,  "Athene": 3}

            SortedKeys = util.dict_key_sorted(Dict, Reverse=True)
            self.assertEqual(SortedKeys, ["Zeus", "Xena", "Athene", "Aphrodite"])

    def test_util_dict_key_insert_if_necessary(self):
        if self._test_exec("test_util_dict_key_insert_if_necessary"):
            Dict = {"Xena": 1, "Zeus": 2, "Athene": 3}
            Inserted = util.dict_key_insert_if_necessary(Dict, "Zeus", 99)
            self.assertFalse(Inserted)

            Inserted = util.dict_key_insert_if_necessary(Dict, "Hermes", 33)
            self.assertTrue(Inserted)
            self.assertTrue(Dict["Hermes"] == 33)

    def test_util_filename_extension__without_extension(self):
        if self._test_exec("test_filename_extension__without_extension"):
            Ext = util.filename_extension("file.py")
            self.assertEqual(Ext, ".py")

            Ext = util.filename_extension("noext")
            self.assertEqual(Ext, "")

            FnameOnly = util.filename_without_extension("file.py")
            self.assertEqual(FnameOnly, "file")

    def test_util_shell(self):
        if self._test_exec("test_shell"):
            Prg = self.Prg
            if self.Prg["OsIsUnixBased"]: # the tests with ls/grep don't work on Windows
                Result = util.shell(f"ls {Prg['DirPrgRoot']} | grep READ").strip()
                self.assertEqual(Result, "README.md")

    def test_util_dict_key_insert_if_necessary(self):
        if self._test_exec("test_dict_key_insert_if_necessary"):
            Dict = dict()
            Key = "numbers"
            Default = []
            util.dict_key_insert_if_necessary(Dict, Key, Default)
            self.assertEqual(Dict, {Key: Default})

    def test_util_files_collect_from_dir(self):
        if self._test_exec("test_files_collect_from_dir"):
            Prg = self.Prg
            Files = util.files_abspath_collect_from_dir(Prg["DirPrgRoot"])
            self.assertIn(os.path.join(Prg["DirPrgRoot"], "src", "util.py"), Files)

    def test_util_file_create_if_necessary__file_read(self):
        if self._test_exec("test_file_create_if_necessary"):
            Prg = self.Prg
            Fname = os.path.join(Prg["DirWork"], "test_file_create_if_necessary.txt")
            util.file_del(Fname)

            Content = "Cloud\nRain\nSun\r\nSnow   "
            Created = util.file_create_if_necessary(Prg, Fname, ContentDefault=Content)
            self.assertTrue(Created)

            RetRead, ContentReadAll = util.file_read_all(Prg, Fname)
            self.assertEqual(ContentReadAll, Content)

            ContentReadLines = util.file_read_lines(Prg, Fname, Lower=True)
            LinesWanted = ["cloud\n", "rain\n", "sun\r\n", "snow   "]
            self.assertEqual(LinesWanted, ContentReadLines)

            ContentReadLines = util.file_read_lines(Prg, Fname, Strip=True)
            LinesWanted = ["Cloud", "Rain", "Sun", "Snow"]
            self.assertEqual(LinesWanted, ContentReadLines)

            util.file_del(Fname)

    def test_util_file_read_lines(self):
        if self._test_exec("test_file_read_lines"):
            Prg = self.Prg
            Fname = os.path.join(Prg["DirWork"], "test_file_read_lines.txt")
            util.file_write(Prg, Fname=Fname, Content="cat\ndog\nelephant")
            Lines = util.file_read_lines(Prg, Fname, Strip=True)
            self.assertEqual(Lines, ["cat", "dog", "elephant"])
            util.file_del(Fname)

    def test_util_file_write_append_del(self):
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

            Sample = "Árvíztűrő tükörfúrógép"
            RetWriteGz = util.file_write(Prg, Fname=Fname, Content=Sample, Gzipped=True)
            self.assertTrue(RetWriteGz)
            RetReadGz, ContentReadGz = util.file_read_all(Prg, Fname, Gzipped=True)
            self.assertTrue(RetReadGz)
            self.assertEqual(ContentReadGz, Sample)

            FileState, FileGzipped = util.file_is_gzipped(Prg, Fname)
            self.assertEqual("file_exists", FileState)
            self.assertEqual("gzipped", FileGzipped)

            BinWanted = Sample.encode()
            util.file_write_utf8_error_avoid(Prg, Fname, Sample)
            BinFromFile = util.file_read_all_simple(Fname, "rb")
            # print("\n######### >>" + util.file_read_all(Prg, Fname)[1] + "<<")
            # print("\n######### >>", Sample.encode(), "<<")
            self.assertEqual(BinWanted, BinFromFile)


            FileWriteRet = util.file_write_with_check(Prg, Fname, Sample)
            TxtFromFile = util.file_read_all_simple(Fname)
            self.assertEqual(TxtFromFile, Sample)
            self.assertTrue(FileWriteRet)

            util.file_write_with_check(Prg, Fname, "") # clear the content of the file
            # writing is unsuccessful because writer fun doesn't do anything
            def empty_writer_fun(Prg, Fname, Sample): pass
            FileWriteRet = util.file_write_with_check(Prg, Fname, Sample, WriterFun=empty_writer_fun)
            self.assertFalse(FileWriteRet)

            RetDel1 = util.file_del(Fname)
            RetDel2 = util.file_del(Fname)
            self.assertTrue(RetDel1)
            self.assertFalse(RetDel2)

            FileState, FileGzipped = util.file_is_gzipped(Prg, Fname)
            self.assertEqual("file_not_found", FileState)
            self.assertEqual("", FileGzipped)

    def test_util_dir_create_if_necessary(self):
        if self._test_exec("test_dir_create_if_necessary"):
            Prg = self.Prg

            # dir exists, can't create
            Created = util.dir_create_if_necessary(Prg, os.path.join(Prg["DirPrgRoot"], "src"))
            self.assertFalse(Created)

            # file exists with the same name, can't create
            Created = util.dir_create_if_necessary(Prg, os.path.join(Prg["DirPrgRoot"], ".gitignore"))
            self.assertFalse(Created)

            # test dir created
            DirTryToMake = os.path.join(Prg["DirWork"], "TryToMakeThis")
            util.dir_delete_if_exist(Prg, DirTryToMake, Print=True)
            Created = util.dir_create_if_necessary(Prg, DirTryToMake)
            self.assertTrue(Created)
            util.dir_delete_if_exist(Prg, DirTryToMake, Print=True)

def run_all_tests(Prg):
    UtilTests.Prg = Prg
    unittest.main(module="test_util", verbosity=2, exit=False)
