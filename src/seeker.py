# -*- coding: utf-8 -*-
import document, util, stats, time, os, text
import result_selectors

Version = "v03_index_in_subsentence"

# Tested
def match_in_subsentence__results(Prg, WordsWanted):
    TimeStart = stats.time_save(Prg, "match_in_subsentence__results =>")
    MatchNumInSubsentences__Results = dict()
    ResultsTotalNum = 0

    TimeUsedCollectTotal = 0
    TimeUsedResultTotal = 0
    #######################################################################
    for FileBaseName, Doc in Prg["DocumentObjectsLoaded"].items():
        TimeUsedCollectStart = time.time()
        LineNum__SubsentenceNum__WordsDetected = text.linenum__subsentnum__words__collect(WordsWanted, Doc["Index"])
        TimeUsedCollectTotal += time.time() - TimeUsedCollectStart

        # one Line with any result => one result
        ResultsTotalNum += len(LineNum__SubsentenceNum__WordsDetected)

        TimeUsedResultStart = time.time()
        text.match_num_in_subsentence__result_obj(Prg, LineNum__SubsentenceNum__WordsDetected, FileBaseName, MatchNumInSubsentences__Results)
        TimeUsedResultTotal += time.time() - TimeUsedResultStart
    #######################################################################

    MatchNums__Descending = util.dict_key_sorted(MatchNumInSubsentences__Results)

    TimeEnd = stats.time_save(Prg, "match_in_subsentence__results <=")
    print("\n\n")
    print("Time USED collect: ", TimeUsedCollectTotal)
    print("Time USED  result: ", TimeUsedResultTotal)
    print("Time USED (match_in_subsentence__results ):", TimeEnd - TimeStart)
    print("\n\n")
    return MatchNumInSubsentences__Results, MatchNums__Descending, ResultsTotalNum

def seek(Prg, WordsWantedOneString):
    TimeStart = stats.time_save(Prg, "first seek =>")

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
    TimeEnd = stats.time_save(Prg, "first seek <=")
    print("Time USED (seek):", TimeEnd - TimeStart)
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
    Created = False
    if not os.path.isfile(FileSentences):
        if FilePathText: # for testing it's easier to get Text from param - and not create/del tmpfile
            _ReadSuccess, Text = util.file_read_all(Prg, Fname=FilePathText)

        Sentences = text.sentence_separator(Text)
        util.file_write_utf8_error_avoid(Prg, FileSentences, "\n".join(Sentences))
        Created = True

    return Created

# Tested
def file_index_create(Prg, FileIndex, FileSentences):
    Created = False
    if not os.path.isfile(FileIndex):
        Created = True
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

    return Created

def indexing(WordIndex, WordIndexOnlyLineNums,  LineNum, SubSentence, SubSentenceNum):
    SubSentence = text.remove_non_alpha_chars(SubSentence, " ", CharsKeepThem="-")

    for Word in SubSentence.split(): # split at space, tab, newline
        # TODO: words short form expand:
        # I've -> "I", "have" are two separated words,
        # wouldn't -> would is the real word
        util.dict_key_insert_if_necessary(WordIndex, Word, list())
        util.dict_key_insert_if_necessary(WordIndexOnlyLineNums, Word, dict())

        Index = f'"{LineNum}_{SubSentenceNum}"'
        if Index not in WordIndexOnlyLineNums[Word]: # save the word only once
            WordIndex[Word].append(Index)
            WordIndexOnlyLineNums[Word][Index] = True