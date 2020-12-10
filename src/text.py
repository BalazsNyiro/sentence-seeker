# -*- coding: utf-8 -*-
import re, util

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
def subsentences(Prg=None, Sentence="", SubSentenceIdWanted=None, KeepSubsentenceEnd=False):
    SubSentences = []

    ################# collect subsentences by character ###################################
    SubSen = []
    def pack_subsen(SubSenChars):
        return "".join(SubSenChars)

    for Char in Sentence:
        Separator = Char in SubSentenceEnds
        if KeepSubsentenceEnd or not Separator:
            SubSen.append(Char)
        if Separator:
            SubSentences.append(pack_subsen(SubSen))
            SubSen = []
    if SubSen:
        SubSentences.append(pack_subsen(SubSen))
    ####################################################

    if SubSentenceIdWanted is not None: # it can be 0, too. and if 0 == False!
        if SubSentenceIdWanted < len(SubSentences):
            # return with one subsentence
            return True, SubSentences[SubSentenceIdWanted]
        else:
            Msg = f"subsentence {SubSentenceIdWanted} id is missing"
            util.log(Prg, Msg)
            return False, [Msg]
    return True, SubSentences # return with a list, with more than one subsentence


def only_subsentence_num__and__wordnum(Num, WordMultiplier = 100):
    # example: 902:   ( 902 - 2 ) / 100 = 9
    SubSentenceNum = (Num - (Num % WordMultiplier)) // WordMultiplier

    # 902 - 9*100
    WordNum = Num - SubSentenceNum * WordMultiplier
    return SubSentenceNum, WordNum

# Tested - default values are important for testcases
def linenum_subsentencenum_wordnum_get(Line_SubSentence_WordPos, SubSentenceMultiplier=100, WordMultiplier=100):

    # I store 3 numbers info in one number and LineNum can be zero, too
    # basically Line1 == 10000, Line 23 == 230000  so the rule: LineNumber, SubSentenceNum, WordNum

    # complex example: 12345 means: Line=1, Subsentence = 23, WordPos = 45
    LineNum = 0
    SubSentenceNum = 0
    WordNum = 0

    MultiSubWord = SubSentenceMultiplier * WordMultiplier

    if WordMultiplier > Line_SubSentence_WordPos >= 0:
        WordNum = Line_SubSentence_WordPos
    elif MultiSubWord > Line_SubSentence_WordPos >= WordMultiplier:
        SubSentenceNum, WordNum = only_subsentence_num__and__wordnum(Line_SubSentence_WordPos)
    else:
        # without //, a simple / results a float num: 10/2 = 5.0 and I need an integer as result
        LineNum = (Line_SubSentence_WordPos - (Line_SubSentence_WordPos % MultiSubWord)) // MultiSubWord
        SubSentence_WordPos = Line_SubSentence_WordPos - LineNum * MultiSubWord
        SubSentenceNum, WordNum = only_subsentence_num__and__wordnum(SubSentence_WordPos)

    return LineNum, SubSentenceNum, WordNum

# tested/used in test_seeker_logic.test_result_selectors
class sentence_obj_from_memory():
    Counter = -1

    def subsentence_num_add(self, SubSentenceNum):
        self.SubSentenceNums.add(SubSentenceNum)
        if SubSentenceNum < self.SubSentenceNumMin: self.SubSentenceNumMin = SubSentenceNum
        if SubSentenceNum > self.SubSentenceNumMax: self.SubSentenceNumMax = SubSentenceNum

    def word_num_add(self, WordNum):
        self.WordNums.add(WordNum)
        self.HitNum = len(self.WordNums)

    def represent_as_dict(self): # in tests it's easier to check matching with dicts
        return { 'FileSourceBaseName':             self.FileSourceBaseName,
                 'LineNumInSentenceFile':          self.LineNumInSentenceFile,
                 'Sentence':                       self.Sentence,
                 'SentenceLen':                    self.SentenceLen,
                 'SubSentenceLen':                 self.SubSentenceLen,
                 'SubSentenceNums':                self.SubSentenceNums,
                 'SubSentenceNumMin':              self.SubSentenceNumMin,
                 'SubSentenceNumMax':              self.SubSentenceNumMax,
                 'WordNums':                       self.WordNums,
                 'HitNum':                         self.HitNum
                 }

    def to_json(self): # in tests it's easier to check matching with dicts
        return { 'FileSourceBaseName':             self.FileSourceBaseName,
                 'LineNumInSentenceFile':          self.LineNumInSentenceFile,
                 'Sentence':                       self.Sentence,
                 'SentenceLen':                    self.SentenceLen,
                 'SubSentenceLen':                 self.SubSentenceLen,
                 'SubSentenceNums':                list(self.SubSentenceNums), # sets can't be converted to json
                 'SubSentenceNumMin':              self.SubSentenceNumMin,
                 'SubSentenceNumMax':              self.SubSentenceNumMax,
                 'WordNums':                       list(self.WordNums),
                 'HitNum':                         self.HitNum
                 }


    def __init__(self, Prg, FileSourceBaseName, LineNumInSentenceFile, SubSentenceNum, WordNum, SentenceFillInResult=False, SentenceFromOutside=None, SubSentenceFromTest=""):

        if SentenceFromOutside is not None:
            StatusSentenceFromMemory = True
            StatusSubSentences = True
            Sentence = SentenceFromOutside
            SubSentenceResult = SubSentenceFromTest
        else:
            StatusSentenceFromMemory, Sentence = sentence_from_memory(Prg, FileSourceBaseName, LineNumInSentenceFile)
            StatusSubSentences, SubSentenceResult = subsentences(Prg, Sentence, SubSentenceNum)

        sentence_obj_from_memory.Counter += 1
        self.Id = sentence_obj_from_memory.Counter # in tests it's easier to tell: the object where id = 0, 1...

        self.Status = {StatusSentenceFromMemory: StatusSentenceFromMemory,
                       StatusSubSentences: StatusSubSentences}
        self.FileSourceBaseName = FileSourceBaseName

        self.LineNumInSentenceFile = LineNumInSentenceFile
        self.SubSentenceNums = {SubSentenceNum}
        self.SubSentenceNumMin = SubSentenceNum
        self.SubSentenceNumMax = SubSentenceNum
        self.WordNums = {WordNum}
        self.HitNum = 1

        self.Sentence = Sentence if SentenceFillInResult else "-"
        self.SentenceLen = len(Sentence)
        self.SubSentenceLen = len(SubSentenceResult)

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

