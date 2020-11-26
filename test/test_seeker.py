# -*- coding: utf-8 -*-
import unittest, util_test, seeker, util, os, util_json_obj

class SeekerTests(util_test.SentenceSeekerTest):
    def test_file_create_sentences__create_index(self):
        self.maxDiff = None
        if self._test_exec("test_file_create_sentences__create_index"):
            Prg = self.Prg

            FileSentences = os.path.join(Prg["DirWork"], "test_file_create_sentences.txt")
            util.file_del(FileSentences)

            Sample = 'He is my friend. "This is \n the next - city, London -- here, in London, the sky is nice." Is this the third line, or a Book about London?'

            seeker.file_sentence_create(Prg, FileSentences, Sample)
            Wanted = ["He is my friend. \n", # detect London only once from this sentence:
                      '"This is the next - city, London -- here, in London, the sky is nice." \n',
                      "Is this the third line, or a Book about London?"]

            LinesFromFile = util.file_read_lines(Prg, FileSentences)
            self.assertEqual(Wanted, LinesFromFile)

            FileIndex = os.path.join(Prg["DirWork"], "test_file_create_index.txt")
            util.file_del(FileIndex)
            seeker.file_index_create(Prg, FileIndex, FileSentences)
            #seeker.file_index_create(Prg, "/tmp/index.txt", FileSentences)
            # print(util.file_read_all(Prg, FileIndex))

            _Status, WordPosition = util_json_obj.obj_from_file(FileIndex)
            self.assertEqual(set(WordPosition["london"]), set([101, 102, 201]))

            util.file_del(FileSentences)
            util.file_del(FileIndex)

def run_all_tests(Prg):
    SeekerTests.Prg = Prg

    unittest.main(module="test_seeker", verbosity=2, exit=False)

