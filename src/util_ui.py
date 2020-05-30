# -*- coding: utf-8 -*-
import text
def sentence_get_from_result(Prg, Result):
    Source = Result["FileSourceBaseName"]
    LineNum = Result["LineNumInSentenceFile"]
    WordsDetectedInSubsentence = Result["WordsDetectedInSubsentence"]
    WordsDetectedNum = len(WordsDetectedInSubsentence)

    Sentence = text.sentence_loaded(Prg, Source, LineNum)
    Sentence = Sentence.strip() # remove possible newline at end

    Url = ""
    if Source in Prg["DocumentsDb"]:
        Url = Prg["DocumentsDb"][Source]["url"]

    return WordsDetectedInSubsentence, Url, Sentence, WordsDetectedNum, Source
