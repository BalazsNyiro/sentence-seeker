# -*- coding: utf-8 -*-
import util, text

LimitGeneral = 400
################### USED modifiers  ###############################
# the parameter struct is fixed, here we don't use Prg but maybe in other modifiers yes.

def sortSentences(_Prg, ResultsOrig, _WordsMaybeDetected):
    # the sorting has to happen in groups to keep the first sorting's result
    Groups = [ResultsOrig]
    Groups = groups_sort(Groups, "SubSentenceLen")
    Groups = groups_sort(Groups, "SentenceLen")
    return util.list_flat_embedded_lists(Groups)

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

#################  utils for selectors ##############

def groups_sort(Groups, By):
    SortedGroups = []
    for Grp in Groups:                  # but sorting creates sub-groups from the original one
        Sorted = sentence_sort(Grp, By) # so the result will be more group
        SortedGroups.extend(Sorted)     # BUT ORIGINAL ORDER IS KEPT
    return SortedGroups

def sentence_sort(Sentences, By):
    New = []
    Groups = {}
    for Sentence in Sentences:
        Score = vars(Sentence)[By]
        util.dict_value_insert_into_key_group(Groups, Score, Sentence)

    for KeyScore in sorted(Groups.keys()):
        New.append(Groups[KeyScore])
    return New
