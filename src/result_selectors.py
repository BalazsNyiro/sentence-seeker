# -*- coding: utf-8 -*-
import util

LimitGeneral = 200

# TODO: test it
def shorters_are_better(ResultGroup, Limit=LimitGeneral):
    Length__Results__Pairs = dict()
    ResultGroupFresh = []

    for Result in ResultGroup:
        Len = len(Result["Sentence"])
        util.dict_key_insert_if_necessary(Length__Results__Pairs, Len, list())
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

