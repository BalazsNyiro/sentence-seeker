# -*- coding: utf-8 -*-
import re, util, text

SentenceEnds = {".", "!", "?", "…"} # searching in sets is faster than simple lists
SubSentenceEnds = {",", ";", ":"}
MarksQuotation = set(list('"“”'))

# Tested
def sentence_from_memory(Prg, Source, LineNum, Strip=False):
    Msg = ""
    if "DocumentObjectsLoaded" not in Prg:
        Msg = f"DocumentsObjectsLoaded not in Prg"

    elif Source not in Prg["DocumentObjectsLoaded"]:
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


# compile pattern only once
_PatternsCompiledIgnoreCase = {}
_PatternsCompiled = {}
# Tested
def replace_regexp(Text, Pattern, TextNew, IgnoreCase=False):
    global _PatternsCompiled, _PatternsCompiledIgnoreCase
    if IgnoreCase:
        if Pattern not in _PatternsCompiledIgnoreCase:
            _PatternsCompiledIgnoreCase[Pattern] = re.compile(Pattern, re.IGNORECASE)
        P = _PatternsCompiledIgnoreCase[Pattern]
    else:
        if Pattern not in _PatternsCompiled:
            _PatternsCompiled[Pattern] = re.compile(Pattern)
        P = _PatternsCompiled[Pattern]
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








# TESTED
def quotation_sentence_starts(Char, InSentence=False, InQuotation=False):

    if Char in MarksQuotation:
        # if we are in quotation, it can be longer than one sentence -
        # so I change only InQuotation state here. because I don't know anything
        # about the sentences
        if InQuotation:           # we have just finished the quotation
            InQuotation = False   # Quotation End can be in the middle of a sentence:
                                  # For some time past vessels had been met by "an enormous thing," a long

        else: # not InQuotation:
            InSentence = True  # the quotation mark can stand before a normal sentence
            InQuotation = True
            # "Adam wrote the letter"  in this situation the first " char belongs to the next sentence, not the previous one

    if not InSentence:
        if Char.isupper():  # it works with special national chars, too. Example: É
            InSentence = True

    return InSentence, InQuotation

# Tested
def char_add_into_sentence(Sentences, Sentence, Char, InSentence, CharLast):
    if InSentence:
        Sentence.append(Char)
    else: # if not InSentence:
        if Sentences:
            Sentences[-1].append(Char)  # if we are over a sentence but the next didn't started then attach it into previous sentence
        else: #if not Sentences: # if it's the first Sentence, Sentences is empty
            Sentence.append(Char)
            InSentence = True

    if InSentence and Char in SentenceEnds: # I don't want to handle if in a sentence somebody has a
        InSentence = False                  # quotation with another full sentence
        Sentences.append(Sentence)          # because this solution doesn't depend on the correctly
        Sentence = []                       # closed quotation pairs

    if CharLast and Sentence:        # if something stayed in collected chars
        InSentence = False           # and the sentence wasn't finished, saved it, too
        Sentences.append(Sentence)
        Sentence = []

    return Sentences, Sentence, InSentence

def sentence_separator(Text):

    Sentences = [[]] # one empty first sentence to store the not sentence starter texts
    Sentence = []
    InSentence = False
    InQuotation = False

    Text = replace_abbreviations(Text)
    Text = replace_whitespaces_to_one_space(Text)

    ############################ the most naive implementation faster with circa 4 seconds (27->22 sec) ##############
    # for Char in Text + ".":  # add one sentence closer char to the end of the text
    #     Sentence.append(Char)
    #     if Char in SentenceEnds:            # this is rare condition
    #         Sentences.append(Sentence)      # because this solution doesn't depend on the correctly
    #         Sentence = []                   # closed quotation pairs
    # ############################ the most naive implementation faster with 4 seconds ##############

    for Char in Text+".":  # add one sentence closer char to the end of the text

        #########################################################################################################
        # inline to fasten the process: def quotation_sentence_starts(Char, InSentence=False, InQuotation=False):
        if Char in MarksQuotation:
            # if we are in quotation, it can be longer than one sentence -
            # so I change only InQuotation state here. because I don't know anything
            # about the sentences
            if InQuotation:  # we have just finished the quotation
                InQuotation = False  # Quotation End can be in the middle of a sentence:
                # For some time past vessels had been met by "an enormous thing," a long

            else:  # not InQuotation:
                InSentence = True  # the quotation mark can stand before a normal sentence
                InQuotation = True
                # "Adam wrote the letter"  in this situation the first " char belongs to the next sentence, not the previous one

        if not InSentence:
            if Char.isupper():  # it works with special national chars, too. Example: É
                InSentence = True

        ############ inline: fun char_add_into_sentence, avoid fun call, performance #######################################
        if InSentence:
            Sentence.append(Char)
        else: # if not InSentence:
            Sentences[-1].append(Char)  # if we are over a sentence but the next didn't started then attach it into previous sentence

        if Char in SentenceEnds:   # this is rare condition
            if InSentence:                      # I don't want to handle if in a sentence somebody has a
                InSentence = False              # quotation with another full sentence
                Sentences.append(Sentence)      # because this solution doesn't depend on the correctly
                Sentence = []                   # closed quotation pairs

    # first elem of Sentences can be empty at the case of normal Capital sentence starters
    SentenceStrings = ["".join(SentenceChars) for SentenceChars in Sentences if SentenceChars]
    SentenceStrings[-1] = SentenceStrings[-1][:-1] # remove last, fixed built . from the end of last sentence
    return SentenceStrings

def subsentences_use_only_one_separator(Txt):
    for SubSep in SubSentenceEnds:
        Txt = Txt.replace(SubSep, ";")
    return Txt

# Tested
def subsentences(Prg=None, Sentence="", SubSentenceIdWanted=None, ReplaceSubsentenceEndsToOneSeparator=True):
    if ReplaceSubsentenceEndsToOneSeparator:
        Sentence = subsentences_use_only_one_separator(Sentence)

    Subsentences = Sentence.split(";")
    if SubSentenceIdWanted is not None: # it can be 0, too. and if 0 == False!
        if SubSentenceIdWanted < len(Subsentences):
            # return with one subsentence
            return True, Subsentences[SubSentenceIdWanted]
        else:
            Msg = f"subsentence {SubSentenceIdWanted} id is missing"
            util.log(Prg, Msg)
            return False, [Msg]
    return True, Subsentences # return with a list, with more than one subsentence

# Tested
def linenum_subsentencenum_get(LineNum__SubSentenceNum, SubSentenceMultiplayer=100):
    SubSentenceNum = LineNum__SubSentenceNum % SubSentenceMultiplayer
    LineNum = 0

    # I store 2 numbers info in one number and LineNum can be zero, too
    # basically Line1 == 100, Line 23 == 2300  so the last 2 digits strore Subsentence Num
    # and if the num is smaller than 100 it means LineNum = 0
    if LineNum__SubSentenceNum >= SubSentenceMultiplayer:
        LineNum = (LineNum__SubSentenceNum - SubSentenceNum) // SubSentenceMultiplayer

    return LineNum, SubSentenceNum

# tested/used in test_seeker_logic.test_result_selectors
def result_obj(FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, Sentence, SubSentenceResult, SentenceFillInResult):
    return {"FileSourceBaseName": FileSourceBaseName,
            "LineNumInSentenceFile": LineNumInSentenceFile,
            "SubSentenceNum": SubSentenceNum,
            "Sentence": Sentence if SentenceFillInResult else "-",
            "SentenceLen": len(Sentence),
            "SubSentenceLen": len(SubSentenceResult)
           }
# Tested
def result_obj_from_memory(Prg, FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, SentenceFillInResult=False):
    StatusFromMemory, Sentence = sentence_from_memory(Prg, FileSourceBaseName, LineNumInSentenceFile)
    StatusSubSentences, SubSentenceResult = text.subsentences(Prg, Sentence, SubSentenceNum)

    return StatusFromMemory and StatusSubSentences, result_obj(FileSourceBaseName,
                                                               LineNumInSentenceFile,
                                                               SubSentenceNum,
                                                               Sentence,
                                                               SubSentenceResult,
                                                               SentenceFillInResult)

# Tested
def word_wanted(Txt):
    for Char in Txt:
        # accept low letter chars and numbers
        if not (Char in util.ABC_Eng_Lower or Char.isdigit()):
            return False
    return True

def words_count_in_all_document(Prg):
    WordsCounter = dict()
    for Doc in Prg["DocumentObjectsLoaded"].values():
        for Word, LineNums in Doc["WordPosition"].items():
            if Word not in WordsCounter:
                WordsCounter[Word] = 0
            WordsCounter[Word] += len(LineNums)
    return WordsCounter
