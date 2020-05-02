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

def linenumbers_sorted_by_seek_result_length(LineNumbersAllWord):
    LineNumbersSorted = dict()
    for LineNum, Words in LineNumbersAllWord.items():
        NumOfWords = len(Words)
        util.dict_key_insert_if_necessary(LineNumbersSorted, NumOfWords, dict())
        LineNumbersSorted[NumOfWords][LineNum] = Words
    return LineNumbersSorted

# Tested - Words can be separated with comma or space chars
# return
def linenumbers_with_group_of_words(WordsWantedOneString, Index):
    LineNumbersAllWord = dict()

    WordsWantedCleaned = []

    WordsWanted = WordsWantedOneString.replace(",", " ").split()
    for WordWanted in WordsWanted:
        WordWanted = WordWanted.strip().lower()
        WordsWantedCleaned.append(WordWanted)

        if WordWanted and WordWanted in Index:
            LineNumbersCurrentWord = Index[WordWanted]

            for LineNum in LineNumbersCurrentWord:
                if LineNum not in LineNumbersAllWord:
                    LineNumbersAllWord[LineNum] = []
                LineNumbersAllWord[LineNum].append(WordWanted)

    return WordsWantedCleaned, LineNumbersAllWord

def word_highlight(Words, Text, HighlightBefore=">>", HighlightAfter="<<"):
    for Word in Words:
        Pattern = fr"\b({Word})\b"
        TextNew = fr"{HighlightBefore}\1{HighlightAfter}"
        Text = replace_regexp(Text, Pattern, TextNew, IgnoreCase=True)
    return Text