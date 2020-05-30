# -*- coding: utf-8 -*-
import re, util, text, time

SentenceEnds = [".", "!", "?", "…"]
SubsentenceEnds = [",", ";", ":"]
MarksQuotation = '"“”'

def sentence_loaded(Prg, Source, LineNum, Strip=True):
    if Source in Prg["DocumentObjectsLoaded"]:
        Sentence = Prg["DocumentObjectsLoaded"][Source]["Sentences"][LineNum]
        if Strip:
            return Sentence.strip()
        return Sentence
    else:
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

# Tested
_PatternWordsWithBoundary = dict()
def word_count_in_text(Word, Text):
    if Word not in _PatternWordsWithBoundary:
        _PatternWordsWithBoundary[Word] = re.compile(fr'\b{Word}\b', re.IGNORECASE)
    Pattern = _PatternWordsWithBoundary[Word]
    return len(Pattern.findall(Text))

# Tested in: test_seek_linenumbers_with_group_of_words
def match_num_in_subsentence__result_obj(Prg, LineNum__SubsentenceNum__WordsDetected, FileSourceBaseName):
    MatchNumInSubsentence__Results = dict()
    MatchNumMax = 0

    for LineNum in LineNum__SubsentenceNum__WordsDetected:
        for SubsentenceNum in LineNum__SubsentenceNum__WordsDetected[LineNum]:

            WordsDetectedInSubsentence = LineNum__SubsentenceNum__WordsDetected[LineNum][SubsentenceNum]
            NumOfDetected = len(WordsDetectedInSubsentence)

            util.dict_key_insert_if_necessary(MatchNumInSubsentence__Results, NumOfDetected, list())
            Source__LineNum__Words = {"FileSourceBaseName": FileSourceBaseName,
                                      "LineNumInSentenceFile": LineNum,
                                      "WordsDetectedInSubsentence": WordsDetectedInSubsentence,
                                      "Sentence": text.sentence_loaded(Prg, FileSourceBaseName, LineNum)
            }
            MatchNumInSubsentence__Results[NumOfDetected].append(Source__LineNum__Words)
            if NumOfDetected > MatchNumMax:
                MatchNumMax = NumOfDetected
    return MatchNumMax, MatchNumInSubsentence__Results

# Tested - Words can be separated with comma or space chars
# It's a separated step from result_object_building
def linenums__words__collect(WordsWanted, Index):
    LineNums__SubsentenceNum__Words = dict()
    for WordWanted in WordsWanted:

        for IndexObj in Index.get(WordWanted, []):

            LineNum = IndexObj["line"]
            SubSentenceNum = IndexObj["subsentence"]

            util.dict_key_insert_if_necessary(LineNums__SubsentenceNum__Words, LineNum, dict())
            util.dict_key_insert_if_necessary(LineNums__SubsentenceNum__Words[LineNum], SubSentenceNum, list())

            if WordWanted not in LineNums__SubsentenceNum__Words[LineNum][SubSentenceNum]:     # Save it only once if the words
                LineNums__SubsentenceNum__Words[LineNum][SubSentenceNum].append(WordWanted)    # is more than once in a sentence

    return LineNums__SubsentenceNum__Words

# Tested
def words_wanted_clean(WordsOneString):
    WordsCleaned = []
    WordsWanted = WordsOneString.replace(",", " ").split()
    for Word in WordsWanted:
        Word = Word.strip().lower()
        if Word and Word not in WordsCleaned:
            WordsCleaned.append(Word)
    return WordsCleaned

def word_highlight(Words, Text, HighlightBefore=">>", HighlightAfter="<<"):
    for Word in Words:
        Pattern = fr"\b({Word})\b"
        TextNew = fr"{HighlightBefore}\1{HighlightAfter}"
        Text = replace_regexp(Text, Pattern, TextNew, IgnoreCase=True)
    return Text