# -*- coding: utf-8 -*-
import document, util, stats, time, os, text
import result_selectors

Version = "v02_simple"

# # MatchNumMaxInSubsentences
# 2: [{'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 1,
#      'WordsDetectedInSentence': ['looks', 'like', 'this'],
#      'Sentence': 'One of these birds looks like a blackbird, the tree is brown and this one is stronger.'},
#     {'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 3,
#      'WordsDetectedInSentence': ['like', 'this'], 'Sentence': 'Have you ever seen a brown blackbird, like this one?'}],
# 1: [{'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 0,
#      'WordsDetectedInSentence': ['bird'], 'Sentence': 'Birds are singing on the Tree but that bird is watching.'},
#     {'FileSourceBaseName': 'test_group_maker_document.txt', 'LineNumInSentenceFile': 2,
#      'WordsDetectedInSentence': ['this'],
#      'Sentence': "The other birds' feather is strong, brown colored, they are hidden in this foliage."}]


# Tested
def match_in_subsentence__results(Prg, WordsWanted):
    Groups_MatchNums_ResultInfos = dict()
    ResultsTotalNum = 0

    for FileBaseName, Doc in Prg["DocumentObjectsLoaded"].items():

        # this is an implemented Select LineNums, words from DB...
        LineNums__WordsWanted = text.linenums__words__collect(WordsWanted, Doc["Index"])

        for MatchNumInSentence, Results in \
                text.match_num__result_obj(Prg, LineNums__WordsWanted, FileBaseName).items():

            for Result in Results:
                MatchNumMaxInSubsentences = text.match_num_max_in_subsentences(MatchNumInSentence, WordsWanted, Result["Sentence"])

                util.dict_key_insert_if_necessary(Groups_MatchNums_ResultInfos, MatchNumMaxInSubsentences, list())
                Groups_MatchNums_ResultInfos[MatchNumMaxInSubsentences].append(Result)
                ResultsTotalNum += 1

    MatchNums__Descending = util.dict_key_sorted(Groups_MatchNums_ResultInfos)

    return Groups_MatchNums_ResultInfos, MatchNums__Descending, ResultsTotalNum

def seek(Prg, WordsWantedOneString):
    stats.save(Prg, "first seek =>")
    TimeStart = time.time()

    ###############################
    WordsWanted = text.words_wanted_clean(WordsWantedOneString)
    GroupsSubsentenceBased_MatchNums_ResultInfos, MatchNums__Descending, ResultsTotalNum = match_in_subsentence__results(Prg, WordsWanted)

    ResultsSelected = []
    Selectors = [result_selectors.shorters_are_better,
                 result_selectors.duplication_removing]

    for MatchNum in MatchNums__Descending:

        # PLUGIN ATTACH POINT
        # - if it's possible keep the search word order?
        # - the words distance (shorter is better)

        ResultsGroup = GroupsSubsentenceBased_MatchNums_ResultInfos[MatchNum]
        for Selector in Selectors:
            ResultsGroup = Selector(ResultsGroup)
        ResultsSelected.extend(ResultsGroup)

    ###############################
    TimeEnd = time.time()
    print("Time USED:", TimeEnd - TimeStart)
    stats.save(Prg, "first seek <=")

    return WordsWanted, ResultsSelected, ResultsTotalNum

def results_sort_by_sentence_length(Prg, Results):
    ResultsSorted = []

    GroupsByLen = dict()
    for Result in Results:
        Sentence = text.sentence_loaded(Prg, Result["FileSourceBaseName"], Result["LineNumInSentenceFile"])
        SentenceLen = len(Sentence)
        util.dict_key_insert_if_necessary(GroupsByLen, SentenceLen, list())
        GroupsByLen[SentenceLen].append(Result)

    LenKeys = util.dict_key_sorted(GroupsByLen)
    for Key in LenKeys:
        # TODO: first where the words are in the same clause
        # TODO: where words are in same order?
        # TODO: avoid same sentences in different results
        # TODO: choose samples from different sources, not only from one
        ResultsSorted.extend(GroupsByLen[Key])

    return ResultsSorted

def be_ready_to_seeking(Prg, Verbose=True, LoadOnlyTheseFileBaseNames=None):
    Prg["DocumentObjectsLoaded"] = \
        document.document_objects_collect_from_working_dir(
            Prg, Version,
            FunSentenceCreate=file_sentence_create,
            FunIndexCreate=file_index_create,
            Verbose=Verbose,
            LoadOnlyTheseFileBaseNames=LoadOnlyTheseFileBaseNames
        )

# what is a sentence: https://simple.wikipedia.org/wiki/Sentence
# unfortunatelly I can't analyse the text based on the structure of the text,
# for example to check it after verbs.
#
# Tested

# Tested
def file_sentence_create(Prg, FileSentences, Text="", FilePathText=""):
    if not os.path.isfile(FileSentences):
        if FilePathText: # for testing it's easier to get Text from param - and not create/del tmpfile
            _ReadSuccess, Text = util.file_read_all(Prg, Fname=FilePathText)

        Sentences = text.sentence_separator(Text)
        util.file_write_utf8_error_avoid(Prg, FileSentences, "\n".join(Sentences))

# Tested
def file_index_create(Prg, FileIndex, FileSentences):
    if not os.path.isfile(FileIndex):
        WordIndex = dict()

        # start LineNum from 1
        for LineNum, Line in enumerate(util.file_read_lines(Prg, FileSentences)):

            # THIS word can be spoiled:
            # word;  for example, I need clean words so remove the not-abc chars

            # I replace with space because:
            # This rock-hard cake is absolutely impossible to eat.
            # We’re looking for a dog-friendly hotel.
            # ’ -   signs has to be replaced with word separator char

            Line = text.remove_not_alpha_chars(Line, " ", CharsKeepThem="-")

            for Word in Line.split():

                # TODO: words short form expand:
                # I've -> "I", "have" are two separated words,
                # wouldn't -> would is the real word

                Word = Word.strip().lower() # The == the, capitals are not important from the viewpoint of words
                if Word: # if it's not empty string
                    if Word not in WordIndex:
                        WordIndex[Word] = list()
                    WordIndex[Word].append(LineNum)

        Out = []
        for Word, LineNums in WordIndex.items():
            Out.append(f'"{Word}": {str(LineNums)}')
        Content="{\n"+"\n,".join(Out) + "\n}"
        util.file_write(Prg, Fname=FileIndex, Content=Content)


