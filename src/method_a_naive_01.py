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


# what is a sentence: https://simple.wikipedia.org/wiki/Sentence
# unfortunatelly I can't analyse the text based on the structure of the text,
# for example to check it after verbs.
#
# Sentence
def sentence_separator(Text):
    Text = text.replace_abbreviations(Text)
    Text = text.replace_whitespaces_to_one_space(Text)

    Sentences = []
    SentenceChars = []
    InSentence = False

    for Char in Text:

        ########## BEGINNING ##########
        if not InSentence:
            if Char in text.AbcEngUpper: InSentence = True

            if Char in text.MarksQuotation: InSentence = True
            # "Adam wrote the letter"  in this situation the first " char belongs to the next sentence, not the previous one

        ########## BEGINNING ##########

        if InSentence:
            SentenceChars.append(Char)

        if not InSentence:
            if not Sentences: # if it's the first Sentence, Sentences is empty
                SentenceChars.append(Char)
            else:
                Sentences[-1].append(Char)  # if we are over a sentence but the next didn't started then attach it into previous sentence

        ########## CLOSER ##########
        if InSentence and Char in text.SentenceEnds:
            InSentence = False
            Sentences.append(SentenceChars)
            SentenceChars = []
        ########## CLOSER ##########

    if SentenceChars: # if something stayed in collected chars and the sentence wasn't finished, saved it, too
        Sentences.append(SentenceChars)

    RetSentences = [("".join(SentenceChars)).strip() for SentenceChars in Sentences]
    print("Sentences: ", RetSentences)
    return RetSentences


def _sentence_separate_from_orig_txt(Prg, FileBaseName, DocumentObj, Text):
    DocumentObj["SentenceFile"] = DocumentObj["PathAbs"] + "_sentence_sep_" + Version
    if not os.path.isfile(DocumentObj["SentenceFile"]):
        Sentences = sentence_separator(Text)
        util.file_write(Prg, DocumentObj["SentenceFile"], "\n>>>".join(Sentences))

def _indexes_from_orig_txt(Prg, FileBaseName, DocumentObj):
    pass

def _docs_load_all_to_be_ready_to_seeking(Prg, FileBaseName, DocumentObj, TextOrig):
    DocumentObj["Text"] = TextOrig
    Prg["DocumentObjectsLoaded"][FileBaseName] = DocumentObj

    util.print_dev(Prg, "loaded doc >>", FileBaseName)

