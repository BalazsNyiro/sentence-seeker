# -*- coding: utf-8 -*-
import util, text

LimitGeneral = 400
################### USED modifiers  ###############################
# the parameter struct is fixed, here we don't use Prg but maybe in other modifiers yes.
def short_sorter(_Prg, SentencesObj, _WordsMaybeDetected):
    # the sorting has to happen in groups to keep the first sorting's result
    Groups = [SentencesObj]
    Groups = groups_sort(Groups, "SentenceLen")
    Groups = groups_sort(Groups, "SubSentenceLen")
    return util.list_flat_embedded_lists(Groups)

def uniq_filter(Prg, SentencesObj, _WordsMaybeDetected):
    Uniq = []

    Inserted = set()
    for SenObj in SentencesObj:
        _Status, Sentence = text.sentence_from_memory(Prg, SenObj.FileSourceBaseName, SenObj.LineNumInSentenceFile)
        TextRaw = Sentence.lower().replace(" ", "").replace("\t", "")
        if TextRaw not in Inserted:
            Inserted.add(TextRaw)
            Uniq.append(SenObj)

    return Uniq

################### USED modifiers  ###############################


def text_source_mixing(ResultGroup, Limit=LimitGeneral):
    # TODO : source mixing
    return ResultGroup


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
