# -*- coding: utf-8 -*-
import util

# TODO: test it
def shorters_are_better(ResultGroup, Limit = 200):
    Length__Results__Pairs = dict()
    ResultsFresh = []

    for Result in ResultGroup:
        Len = len(Result["Sentence"])
        util.dict_key_insert_if_necessary(Length__Results__Pairs, Len, list())
        Length__Results__Pairs[Len].append(Result)

    Counter = 0
    KeysDescented = util.dict_key_sorted(Length__Results__Pairs, Reverse=False)
    for Key in KeysDescented:
        Results = Length__Results__Pairs[Key]
        for Result in Results:
            ResultsFresh.append(Result)
            Counter += 1
            if Counter >= Limit:      # a raw seek can give back more thousand results.
                return ResultsFresh   # stop loop if we have enough result

    return ResultsFresh

