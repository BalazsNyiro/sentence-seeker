# -*- coding: utf-8 -*-
import util, text

LimitGeneral = 400
################### USED modifiers  ###############################
# the parameter struct is fixed, here we don't use Prg but maybe in other modifiers yes.
def sort_by_relevance(Prg, Group, _WordsMaybeDetected):

    def grouping_hitnum(_Prg, GroupOrig, _Params):
        # if the obj has more highlighted words/hit, it's more important for the user.
        obj_grouping(GroupOrig, "HitNum", Reverse=True, OverwriteOrig=True)

    # NewVal = obj_grouping(Group, "HitNum", Reverse=True)
    reach_the_deepest_lists_and_modify(Prg, Group, grouping_hitnum, dict())


def sort_by_sentence_len(Prg, Group, _WordsMaybeDetected):

    def grouping_sentencelen(_Prg, GroupOrig, _Params):
        obj_grouping(GroupOrig, "SentenceLen", OverwriteOrig=True)

    def grouping_subsentencelen(_Prg, GroupOrig, _Params):
        obj_grouping(GroupOrig, "SubSentenceLen", OverwriteOrig=True)

    reach_the_deepest_lists_and_modify(Prg, Group, grouping_sentencelen, dict())
    reach_the_deepest_lists_and_modify(Prg, Group, grouping_subsentencelen, dict())

def remove_duplicated_sentences(Prg, Group, _WordsMaybeDetected):
    def removing_duplicates(_Prg, Sentences, KnownSentences):
        ToDelete = []

        for Id, SenObj in enumerate(Sentences):
            _Status, Sentence = text.sentence_from_memory(Prg, SenObj.FileSourceBaseName, SenObj.LineNumInSentenceFile)
            TextRaw = Sentence.lower().replace(" ", "").replace("\t", "").strip()
            if TextRaw in KnownSentences:
                ToDelete.append(Id)
            else:
                KnownSentences.add(TextRaw)

        for Id in reversed(ToDelete):
            Sentences.pop(Id)

    KnownSentences = set() # this set is common in all leaves
    reach_the_deepest_lists_and_modify(Prg, Group, removing_duplicates, KnownSentences)
    ###############################################################################

#################  utils for selectors ##############

# TESTED
def obj_grouping(Objects, By, Reverse=False, OverwriteOrig=True):
    New = []
    Groups = {}
    for Obj in Objects:
        Score = vars(Obj)[By]
        util.dict_value_insert_into_key_group(Groups, Score, Obj)

    for KeyScore in sorted(Groups.keys(), reverse=Reverse):
        New.append(Groups[KeyScore])

    if OverwriteOrig:
        Objects.clear()
        Objects.extend(New)
    else:
        return New

# TESTED
def reach_the_deepest_lists_and_modify(Prg, Group, Fun, Params):
    # if the obj has more highlighted words/hit, it's more important for the user.
    if util.is_list(Group) and Group:

        # if one member is list, all members are list
        GroupHasListsMembers = util.is_list(Group[0])

        if GroupHasListsMembers:
            for ListMember in Group:
                reach_the_deepest_lists_and_modify(Prg, ListMember, Fun, Params)
        else:
            # modify the original values in Group
            Fun(Prg, Group, Params)

