# -*- coding: utf-8 -*-
import re, util, text, time

SentenceEnds = [".", "!", "?", "…"]
SubsentenceEnds = [",", ";", ":"]
MarksQuotation = '"“”'

def sentence_loaded(Prg, Source, LineNum):
    if Source in Prg["DocumentObjectsLoaded"]:
        return Prg["DocumentObjectsLoaded"][Source]["Sentences"][LineNum]
    return f"DocumentsObjectsLoaded: {Source} is not loaded"

# Tested
_PatternNotAbc = re.compile(r'[^a-zA-Z]')
def remove_non_alpha_chars(Text, TextNew="", CharsKeepThem=""):

    # in other, none English languate other chars can be letters, too.
    # the traditional a-z method doesn't match with them
    #    return replace_regexp(Text, _PatternNotAbc, TextNew)

    Cleaned = []
    for Char in Text:
        # cliché - é is not in common Eng chars, but isalpha keep it
        if Char.isalpha() or Char in CharsKeepThem:
            Cleaned.append(Char)
        else:
            Cleaned.append(TextNew)
    return "".join(Cleaned)


# Tested with abbreviations,
# FromToPairsExample = [("Mr.", "Mr")]
def replace(Txt, FromToPairs):
    for Old, New in FromToPairs:
        Txt = Txt.replace(Old, New)
    return Txt

_PatternWhitespaces = re.compile(r'\s+')
# Tested
def replace_whitespaces_to_one_space(Text):
    return replace_regexp(Text, _PatternWhitespaces, " ")

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
    return replace(Txt, ReplaceAbbreviations)

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


def result_obj(Prg, FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, SentenceFillInResult=False):
    if SentenceFillInResult: # in html server the sentence is important in result
        Sentence = sentence_loaded(Prg, FileSourceBaseName, LineNumInSentenceFile)
    else:
        Sentence = "-"
    Obj = {"FileSourceBaseName": FileSourceBaseName,
           "LineNumInSentenceFile": LineNumInSentenceFile,
           "SubSentenceNum": SubSentenceNum,
           "Sentence": Sentence
            }
    return Obj

def word_highlight(Words, Text, HighlightBefore=">>", HighlightAfter="<<"):
    for Word in Words:
        Pattern = fr"\b({Word})\b"
        TextNew = fr"{HighlightBefore}\1{HighlightAfter}"
        Text = replace_regexp(Text, Pattern, TextNew, IgnoreCase=True)
    return Text