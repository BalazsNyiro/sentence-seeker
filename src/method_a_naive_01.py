# -*- coding: utf-8 -*-
import document, util, stats, time

SentenceFinishers = ["…", "!", "?", ".", "..."]
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
    _sentence_separate_from_orig_txt(Prg)
    _indexes_from_orig_txt(Prg)
    _docs_load_all_to_be_ready_to_seeking(Prg)

def _sentence_separate_from_orig_txt(Prg):
    pass

def _indexes_from_orig_txt(Prg):
    pass

def _docs_load_all_to_be_ready_to_seeking(Prg):
    for FileBaseName, DocumentObj in \
            document.document_objects_collect_from_working_dir(Prg).items():

        _ReadSuccess, Text = util.file_read_all(Prg, Fname=DocumentObj["PathAbs"])
        DocumentObj["Text"] = Text
        Prg["DocumentObjectsLoaded"][FileBaseName] = DocumentObj

        util.print_dev(Prg, "loaded doc >>", FileBaseName)

