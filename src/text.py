# -*- coding: utf-8 -*-
import re, util, text, time

SentenceEnds = [".", "!", "?", "…"]
SubsentenceEnds = [",", ";", ":"]
MarksQuotation = '"“”'

# Tested
def sentence_from_memory(Prg, Source, LineNum, Strip=False):
    Msg = ""
    if Source not in Prg["DocumentObjectsLoaded"]:
        Msg = f"DocumentsObjectsLoaded: {Source} is not loaded"

    elif "Sentences" not in Prg["DocumentObjectsLoaded"][Source]:
        Msg = f"DocumentsObjectsLoaded: {Source} no Sentences"

    elif not util.is_list(Prg["DocumentObjectsLoaded"][Source]["Sentences"]):
        Sentences = Prg["DocumentObjectsLoaded"][Source]["Sentences"]
        Msg = f"DocumentsObjectsLoaded: incorrect type: Sentences = {str(Sentences)}"

    elif len(Prg["DocumentObjectsLoaded"][Source]["Sentences"])-1 < LineNum:
        Msg = f"DocumentsObjectsLoaded: {Source} unknown linenum: {LineNum}"

    if Msg:
        print(Msg)
        util.log(Prg, Msg)
        return False, Msg

    Line = Prg["DocumentObjectsLoaded"][Source]["Sentences"][LineNum]
    if Strip:
        return True, Line.strip()
    return True, Line

# Tested
_PatternNotAbc = re.compile(r'[^a-zA-Z]')
def remove_non_alpha_chars(Text, TextNew="", CharsKeepThem=""):

    # in other, none English languate other chars can be letters, too.
    # the traditional a-z method doesn't match with them
    #    return replace_regexp(Text, _PatternNotAbc, TextNew)

    Cleaned = []
    for Char in Text:
        # cliché - é is not in common Eng chars, but isalpha keep it
        if Char.isalpha() or Char.isdigit() or Char in CharsKeepThem:
            Cleaned.append(Char)
        else:
            Cleaned.append(TextNew)
    return "".join(Cleaned)

_PatternWhitespaces = re.compile(r'\s+')
# Tested
def replace_whitespaces_to_one_space(Text):
    return replace_regexp(Text, _PatternWhitespaces, " ")

# Tested
def replace_pairs(Txt, Replaces):
    for Old, New in Replaces:
        Txt = Txt.replace(Old, New)
    return Txt

# Tested
def replace_regexp(Text, Pattern, TextNew, IgnoreCase=False):
    if IgnoreCase:
        P = re.compile(Pattern, re.IGNORECASE)
    else:
        P = re.compile(Pattern)
    return P.sub(TextNew, Text)

# Tested
def html_tags_remove(Src, TextNew=""):
    Pattern = r'<.*?>'
    return replace_regexp(Src, Pattern, TextNew)

# Tested
def replace_abbreviations(Txt):
    ReplaceAbbreviations = [("Mr.", "Mr"),
                            ("Mrs.", "Mrs"),
                            ("Ms.", "Ms")]
    return replace_pairs(Txt, ReplaceAbbreviations)

# TODO: test it
def sentence_separator(Text):
    Text = replace_abbreviations(Text)
    Text = replace_whitespaces_to_one_space(Text)

    Sentences = []
    Sentence = []

    InSentence = False
    InQuotation = False

    TimeStart = time.time()
    LoopCounter = 0
    for Char in Text:

        LoopCounter += 1
        if time.time() - TimeStart > 1:
            if LoopCounter % 2000 == 0:
                print("t", end="", flush=True)

        ########## BEGINNING ##########
        if Char in MarksQuotation:
            if not InQuotation:
                InSentence = True
                InQuotation = True
                # "Adam wrote the letter"  in this situation the first " char belongs to the next sentence, not the previous one
            else:
                InQuotation = False
                # Quotation End can be in the middle of a sentence:
                # For some time past vessels had been met by "an enormous thing," a long

        if not InSentence:
            if Char.isupper(): # it works with special national chars, too. Example: É
                InSentence = True

        ########## --BEGINNING-- part finished ##########

        if InSentence: # DECISION:
            Sentence.append(Char)
        else: # not InSentence
            if not Sentences: # if it's the first Sentence, Sentences is empty
                Sentence.append(Char)
            else:
                Sentences[-1].append(Char)  # if we are over a sentence but the next didn't started then attach it into previous sentence

        ########## CLOSER ##########
        if InSentence and Char in SentenceEnds:
            InSentence = False
            Sentences.append(Sentence)
            Sentence = []
        ########## CLOSER ##########

    if Sentence: # if something stayed in collected chars and the sentence wasn't finished, saved it, too
        Sentences.append(Sentence)

    RetSentences = [("".join(SentenceChars)).strip() for SentenceChars in Sentences]
    # print("\n\nSentences: ", RetSentences)
    return RetSentences

#FIXME: TEST IT
def subsentences(Sentence):
    for SubSep in SubsentenceEnds:
        Sentence = Sentence.replace(SubSep, ";")
    return Sentence.split(";")

def linenum_subsentencenum_get(LineNum_SubSentenceNum):
    SubSentenceNum = LineNum_SubSentenceNum % 100

    if LineNum_SubSentenceNum < 100:  # I store 2 numbers info in one number and LineNum can be zero, too
        return 0, SubSentenceNum   # basically Line1 == 100, Line 23 == 2300  so the last 2 digits strore Subsentence Num
    # and if the num is smaller than 100 it means LineNum = 0

    return (LineNum_SubSentenceNum - SubSentenceNum) // 100, SubSentenceNum

# tested/used in test_seeker_logic.test_result_selectors
def result_obj(FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, Sentence, SubSentenceResult, SentenceFillInResult):
    return {"FileSourceBaseName": FileSourceBaseName,
            "LineNumInSentenceFile": LineNumInSentenceFile,
            "SubSentenceNum": SubSentenceNum,
            "Sentence": Sentence if SentenceFillInResult else "-",
            "SentenceLen": len(Sentence),
            "SubSentenceLen": len(SubSentenceResult)
           }

def result_obj_from_memory(Prg, FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, SentenceFillInResult=False):
    _Status, Sentence = sentence_from_memory(Prg, FileSourceBaseName, LineNumInSentenceFile)
    SubSentences = text.subsentences(Sentence)
    SubSentenceResult = SubSentences[SubSentenceNum]
    return result_obj(FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, Sentence, SubSentenceResult, SentenceFillInResult)

def word_highlight(Words, Text, HighlightBefore=">>", HighlightAfter="<<"):
    for Word in Words:
        Pattern = fr"\b({Word})\b"
        TextNew = fr"{HighlightBefore}\1{HighlightAfter}"
        Text = replace_regexp(Text, Pattern, TextNew, IgnoreCase=True)
    return Text

def word_wanted(Txt):
    for Char in Txt:
        # accept low letter chars and numbers
        if not (Char in util.ABC_Eng_Lower or Char.isdigit()):
            return False
    return True
