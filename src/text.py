# -*- coding: utf-8 -*-
import re, util

SentenceEnds = [".", "!", "?", "…"]
MarksQuotation = '"“”'

# Tested
_PatternNotAbc = re.compile(r'[^a-zA-Z]')
def remove_not_alpha_chars(Text, TextNew="", CharsKeepThem=""):

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

def sentence_separator(Text):
    Text = replace_abbreviations(Text)
    Text = replace_whitespaces_to_one_space(Text)

    Sentences = []
    Sentence = []

    InSentence = False
    InQuotation = False

    for Char in Text:

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

def result_object_building___insert_source____linenumbers_sorted_by_seek_result_length(LineNums__WordsDetected, Source):
    LineNumbersSorted = dict()
    for LineNum, WordsDetected in LineNums__WordsDetected.items():
        NumOfWordsDetected = len(WordsDetected)
        util.dict_key_insert_if_necessary(LineNumbersSorted, NumOfWordsDetected, list())
        Source__LineNum__Words = {"Source": Source,
                                  "LineNum": LineNum,
                                  "WordsDetected": WordsDetected}
        LineNumbersSorted[NumOfWordsDetected].append(Source__LineNum__Words)
    return LineNumbersSorted

def words_wanted_clean(WordsOneString):
    WordsCleaned = []
    WordsWanted = WordsOneString.replace(",", " ").split()
    for Word in WordsWanted:
        Word = Word.strip().lower()
        if Word and Word not in WordsCleaned:
            WordsCleaned.append(Word)
    return WordsCleaned

# Tested - Words can be separated with comma or space chars
# return
def linenums__words_detected__collect(WordsWanted, Index):
    LineNums__WordsDetected = dict()
    for WordWanted in WordsWanted:

        if WordWanted and WordWanted in Index:
            LineNumbersCurrentWord = Index[WordWanted]
            for LineNum in LineNumbersCurrentWord:
                if LineNum not in LineNums__WordsDetected:
                    LineNums__WordsDetected[LineNum] = []

                # WARNING: if the sentence has the word two times,
                # the current detection append it two times!
                # if the words can be found more than once in a sentence,
                # save it only once
                if WordWanted not in LineNums__WordsDetected[LineNum]:
                    LineNums__WordsDetected[LineNum].append(WordWanted)

    return LineNums__WordsDetected

def word_highlight(Words, Text, HighlightBefore=">>", HighlightAfter="<<"):
    for Word in Words:
        Pattern = fr"\b({Word})\b"
        TextNew = fr"{HighlightBefore}\1{HighlightAfter}"
        Text = replace_regexp(Text, Pattern, TextNew, IgnoreCase=True)
    return Text