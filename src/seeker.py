# -*- coding: utf-8 -*-
import document, util, stats, time, os, text
import result_selectors

Version = "v03_index_in_subsentence"

# Tested
def match_in_subsentence__results(Prg, WordsWanted):
    Groups_MatchNums_ResultInfos = dict()
    ResultsTotalNum = 0

    for FileBaseName, Doc in Prg["DocumentObjectsLoaded"].items():

        # this is an implemented Select LineNums, words from DB...
        #  {0: ['tree'],
        #   4: ['apple', 'tree'],
        #   3: ['apple'] }
        LineNums__WordsDetected = text.linenums__words__collect(WordsWanted, Doc["Index"])

        # 1: [{'FileSourceBaseName': 'test_seek_linenumbers_with_group_of_words', 'LineNumInSentenceFile': 3, 'WordsDetectedInSentence': ['apple'], 'Sentence': 'DocumentsObjectsLoaded: test_seek_linenumbers_with_group_of_words is not loaded'},
        #     {'FileSourceBaseName': 'test_seek_linenumbers_with_group_of_words', 'LineNumInSentenceFile': 0, 'WordsDetectedInSentence': ['tree'],  'Sentence': 'DocumentsObjectsLoaded: test_seek_linenumbers_with_group_of_words is not loaded'}],
        # 2: [{'FileSourceBaseName': 'test_seek_linenumbers_with_group_of_words', 'LineNumInSentenceFile': 4, 'WordsDetectedInSentence': ['apple', 'tree'], 'Sentence': 'DocumentsObjectsLoaded: test_seek_linenumbers_with_group_of_words is not loaded'}]

        for MatchNumInSentence, Results in \
                text.match_num__result_obj(Prg, LineNums__WordsDetected, FileBaseName).items():

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
        WordIndexOnlyLineNums = dict()

        Lines = util.file_read_lines(Prg, FileSentences, Strip=False, Lower=True)

        for LineNum, Line in enumerate(Lines):

            if LineNum % 1000 == 0:
                Percent = int(LineNum / len(Lines)* 100)
                print(f"index create: {Percent} %")#, end="", flush=True)

            # THIS word can be spoiled:
            # word;  for example, I need clean words so remove the not-abc chars

            # I replace with space because:
            # This rock-hard cake is absolutely impossible to eat.
            # We’re looking for a dog-friendly hotel.
            # ’ -   signs has to be replaced with word separator char

            # more than one minus: -- or --- signs: replace them

            Line = text.replace_regexp(Line, "[-][-]+", " ")

            for SubSentenceNum, SubSentence in enumerate(text.subsentences(Line)):
                indexing(WordIndex, WordIndexOnlyLineNums, LineNum, SubSentence, SubSentenceNum)

        Out = []
        for Word, LineNums in WordIndex.items():
            Out.append(f'"{Word}": [{",".join(LineNums)}]')
        Content="{\n"+"\n,".join(Out) + "\n}"
        util.file_write(Prg, Fname=FileIndex, Content=Content)


def indexing(WordIndex, WordIndexOnlyLineNums,  LineNum, SubSentence, SubSentenceNum):
    SubSentence = text.remove_non_alpha_chars(SubSentence, " ", CharsKeepThem="-")


    for Word in SubSentence.split(): # split at space, tab, newline
        # TODO: words short form expand:
        # I've -> "I", "have" are two separated words,
        # wouldn't -> would is the real word
        util.dict_key_insert_if_necessary(WordIndex, Word, list())
        util.dict_key_insert_if_necessary(WordIndexOnlyLineNums, Word, dict())

        Index = "{" + f'"line": {LineNum}, "subsentence": {SubSentenceNum}' + "}"
        if LineNum not in WordIndexOnlyLineNums[Word]: # save the word only once
            WordIndex[Word].append(Index)
            WordIndexOnlyLineNums[Word][LineNum] = True