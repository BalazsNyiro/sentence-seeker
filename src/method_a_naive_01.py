# -*- coding: utf-8 -*-
import document, util, stats, time, os, text

Version = "a_naive_01"

def seek(Prg, Wanted):
    LinesSelected = []
    stats.save(Prg, "first seek =>")
    TimeStart = time.time()
    ###############################
    CharCounter = 0
    for DocBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():
        Text = DocObj["Text"]
        print(DocBaseName, len(Text))
        CharCounter += len(Text)
        for Line in Text.split("\n"):
            if Wanted in Line:
                LinesSelected.append(Line)

    ###############################
    TimeEnd = time.time()
    print("\n".join(LinesSelected))
    print("Time USED:", TimeEnd - TimeStart, f"CharCounter: {CharCounter}, page: {CharCounter / 2000}")
    stats.save(Prg, "first seek <=")

def be_ready_to_seeking(Prg):
    for FileBaseName, DocumentObj in \
            document.document_objects_collect_from_working_dir(Prg).items():

        _ReadSuccess, TextOrig = util.file_read_all(Prg, Fname=DocumentObj["PathAbs"])

        _sentence_separate_from_orig_txt(Prg, FileBaseName, DocumentObj, TextOrig)

        _indexes_from_orig_txt(Prg, FileBaseName, DocumentObj)
        _docs_load_all_to_be_ready_to_seeking(Prg, FileBaseName, DocumentObj, TextOrig)


def _sentence_separate_from_orig_txt(Prg, FileBaseName, DocumentObj, TextOrig):
    DocumentObj["SentenceFile"] = DocumentObj["PathAbs"] + "_sentence_sep_" + Version
    if not os.path.isfile(DocumentObj["SentenceFile"]):

        Text = text.replace_abbreviations(TextOrig)
        Text = text.replace_spaces_to_one_space(Text)

        util.file_write(Prg, DocumentObj["SentenceFile"], TextCleaned)

def _indexes_from_orig_txt(Prg, FileBaseName, DocumentObj):
    pass

def _docs_load_all_to_be_ready_to_seeking(Prg, FileBaseName, DocumentObj, TextOrig):
    DocumentObj["Text"] = TextOrig
    Prg["DocumentObjectsLoaded"][FileBaseName] = DocumentObj

    util.print_dev(Prg, "loaded doc >>", FileBaseName)

