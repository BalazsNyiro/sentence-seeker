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

# Tested
_PatternWordsWithBoundary = dict()
def word_count_in_text(Word, Text):
    if Word not in _PatternWordsWithBoundary:
        _PatternWordsWithBoundary[Word] = re.compile(fr'\b{Word}\b', re.IGNORECASE)
    Pattern = _PatternWordsWithBoundary[Word]
    return len(Pattern.findall(Text))

# Tested in: test_seek_linenumbers_with_group_of_words
def match_num_in_subsentence__result_obj(Prg, LineNum_SubSentenceNum__WordsDetected, FileSourceBaseName, MatchNumInSubsentences__Results):
    for LineNum_SubSentenceNum, WordsDetectedInSubsentence in LineNum_SubSentenceNum__WordsDetected.items():

        if LineNum_SubSentenceNum < 100: # I store 2 numbers info in one number and LineNum can be zero, too
            LineNum = 0                  # basically Line1 == 100, Line 23 == 2300  so the last 2 digits strore Subsentence Num
        else:                            # and if the num is smaller than 100 it means LineNum = 0
            SubsentenceNum = LineNum_SubSentenceNum % 100
            LineNum = (LineNum_SubSentenceNum - SubsentenceNum)//100

        NumOfDetected = len(WordsDetectedInSubsentence)

        Source__LineNum__Words = {"FileSourceBaseName": FileSourceBaseName,
                                  "LineNumInSentenceFile": LineNum,
                                  "WordsDetectedInSubsentence": WordsDetectedInSubsentence,
                                  "Sentence": text.sentence_loaded(Prg, FileSourceBaseName, LineNum)}

        if NumOfDetected not in MatchNumInSubsentences__Results:
            MatchNumInSubsentences__Results[NumOfDetected] = [Source__LineNum__Words]
        else:
            MatchNumInSubsentences__Results[NumOfDetected].append(Source__LineNum__Words)

# Tested - Words can be separated with comma or space chars
# It's a separated step from result_object_building
def linenum__subsentnum__words__collect(Prg, WordsWanted, Index):
    LineNum_SubsentenceNum__WordsDetected = dict()
    WordSetsFounded = Prg["WordSetsFounded"]

    for WordWanted in WordsWanted:
        for LineNum_SubSentenceNum in Index.get(WordWanted, []):

            ############ This is the pure logic - but here we always create new lists with words
            # if LineNum_SubSentenceNum not in LineNum_SubsentenceNum__WordsDetected:
            #     LineNum_SubsentenceNum__WordsDetected[LineNum_SubSentenceNum] = [WordWanted] # always create new lists
            #     continue

            # if WordWanted not in LineNum_SubsentenceNum__WordsDetected[LineNum_SubSentenceNum]:     # Save it only once if the words
            #     LineNum_SubsentenceNum__WordsDetected[LineNum_SubSentenceNum].append(WordWanted)    # is more than once in a sentence
            ####################################################################################


            ### Here I store the possible word set variations in a common global store,
            ### and same sets are created only ONCE instead of a lot of lists with same elems
            if LineNum_SubSentenceNum not in LineNum_SubsentenceNum__WordsDetected:
                WordSet = (WordWanted,)
                WordSetSaved = wordset_save_and_get_saved(WordSetsFounded, WordSet)
                LineNum_SubsentenceNum__WordsDetected[LineNum_SubSentenceNum] = WordSetSaved
                continue

            WordSetOld = LineNum_SubsentenceNum__WordsDetected[LineNum_SubSentenceNum]
            if WordWanted not in WordSetOld:
                WordSet = WordSetOld + (WordWanted,)
                WordSetSaved = wordset_save_and_get_saved(WordSetsFounded, WordSet)
                LineNum_SubsentenceNum__WordsDetected[LineNum_SubSentenceNum] = WordSetSaved

    return LineNum_SubsentenceNum__WordsDetected

# TODO: TEST IT
# two tuples with same values can have different id -
# I want to use tuple from stored wordsets
def wordset_save_and_get_saved(WordSetsFounded, WordSet):
    if WordSet not in WordSetsFounded:
        WordSetsFounded[WordSet] = WordSet # the key and the value are same. very rare but valid
        return WordSet
    else:
        return WordSetsFounded[WordSet]

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