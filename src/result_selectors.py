# -*- coding: utf-8 -*-
import util, text

LimitGeneral = 400
################### USED modifiers  ###############################
def sortSentences(_Prg, ResultsOrig, _WordsMaybeDetected):

    def sort(Results, By):
        New = []
        Groups = {}
        for Result in Results:
            Score = Result[By]
            util.dict_value_insert_into_key_group(Groups, Score, Result)

        for KeyScore in sorted(Groups.keys()):
            New.extend(Groups[KeyScore])
        return New

    Sorted1 = sort(ResultsOrig, "SubSentenceLen")
    Sorted2 = sort(Sorted1, "SentenceLen")

    return Sorted2

def remove_sentences_with_too_much_numbers(Prg, ResultsOrig, _WordsMaybeDetected):
    # THIS IS ONE sentence that I want to filter, keyword: public:
    # =====================================================
    # 4 Schools, 113, 116, 117, 401, 422; adornment of, 103, 131; at Athens, 19,
    # 20, 21; _central_, 407, 408; in China, 13; claustral, 69, 75, 76, 116, 282,
    # 345; etymology of the word, 87; European type of, 131; infant, 457-465, 501-504;
    # in India, 6, 514; Jewish, 9; Latin, 119, 128, 130, 131, 144, 346; of the
    # Middle Age, 69, 77, 78; Palatine, 72; primary, 120, 128, 190, 234, 254-277, 365,
    # 383, 426, 477, 510, 520-525; public, 114, 128, 135, 415; real, 414; at Rome, 45,
    # 52; secular, 114, 130, 233, 254, 278, 297, 318, 338, 509, 522.

    # a typical result:
    # RESULT: {'FileSourceBaseName': 'en_wikipedia_org_wiki_Pythagoras',
    #          'LineNumInSentenceFile': 97,
    #          'SubSentenceNum': 1,
    #          'Sentence': '-',
    #          'SentenceLen': 60,
    #          'SubSentenceLen': 55}

    ResultNew = []

    for Result in ResultsOrig:
        _StatusFromMemory, Sentence = text.sentence_from_memory(Prg,
                                                                Result["FileSourceBaseName"],
                                                                Result["LineNumInSentenceFile"])
        WordsHasNum = 0
        WordsWithoutNum = 0
        for Word in Sentence.split(" "):
            HasNum = False
            for Char in Word:
                if Char.isdigit():
                    HasNum = True
                    break
            if HasNum:
                WordsHasNum += 1
            else:
                WordsWithoutNum += 1

        if WordsWithoutNum > WordsHasNum * 5:
            ResultNew.append(Result)

    return ResultNew
################### USED modifiers  ###############################



def text_source_mixing(ResultGroup, Limit=LimitGeneral):
    # TODO : source mixing
    return ResultGroup

# TODO: test it
def shorters_are_better(ResultGroup, Limit=LimitGeneral):
    Length__Results__Pairs = dict()
    ResultGroupFresh = []

    for Result in ResultGroup:
        Len = len(Result["Sentence"])

        if Len not in Length__Results__Pairs:
            Length__Results__Pairs[Len] = list()

        Length__Results__Pairs[Len].append(Result)

    Counter = 0
    KeysDescented = util.dict_key_sorted(Length__Results__Pairs, Reverse=False)
    for Key in KeysDescented:
        Results = Length__Results__Pairs[Key]
        for Result in Results:
            ResultGroupFresh.append(Result)
            Counter += 1
            if Counter >= Limit:      # a raw seek can give back more thousand results.
                return ResultGroupFresh   # stop loop if we have enough result

    return ResultGroupFresh

# TODO: test it
def duplication_removing(ResultGroup, Limit=LimitGeneral):
    ResultGroupFresh = []

    Text__Results__Pairs = dict()
    for Result in ResultGroup:
        TextRaw = Result["Sentence"].lower().replace(" ", "").replace("\t", "")
        Text__Results__Pairs[TextRaw] = Result

    for Counter, Result in enumerate(Text__Results__Pairs.values(), start=1):
        ResultGroupFresh.append(Result)
        if Counter >= Limit:
            break

    return ResultGroupFresh

