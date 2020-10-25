# -*- coding: utf-8 -*-
import document, util, os, text, ui_tkinter_boot_progress_bar

Version = "v03_index_in_subsentence"

def be_ready_to_seeking(Prg, Verbose=True, LoadOnlyThese=None):
    Prg["DocumentObjectsLoaded"] = \
        document.document_objects_collect_from_working_dir(
            Prg, VersionSeeker=Version,
            FunSentenceCreate=file_sentence_create,
            FunIndexCreate=file_index_create,
            Verbose=Verbose,
            LoadOnlyThese=LoadOnlyThese
        )
    Prg["DocumentObjectsLoadedWordsCounterGlobal"] = text.words_count_in_all_document(Prg)

    if Prg.get("MessagesForUser", []):
        print("\n\n Messages for user:")
        for Msg in Prg["MessagesForUser"]:
            print(f" - {Msg}")
        print("\n", flush=True)

    ui_tkinter_boot_progress_bar.progressbar_close(Prg)

# Tested
def file_sentence_create(Prg, FileSentencesAbsPath, Text="", FileTextAbsPath=""):
    Created = False
    if not os.path.isfile(FileSentencesAbsPath):
        if FileTextAbsPath: # for testing it's easier to get Text from param - and not create/del tmpfile
            _ReadSuccess, Text = util.file_read_all(Prg, Fname=FileTextAbsPath)

        Sentences = text.sentence_separator(Text)
        util.file_write_utf8_error_avoid(Prg, FileSentencesAbsPath, "\n".join(Sentences))
        Created = True

    return Created

# Tested
def file_index_create(Prg, FileIndexAbsPath, FileSentencesAbsPath):
    Created = False
    if not os.path.isfile(FileIndexAbsPath):
        Created = True
        WordPositions = dict()
        WordIndexOnlyLineNums = dict()

        _Success, TextAll = util.file_read_all(Prg, FileSentencesAbsPath)
        TextAll = TextAll.lower()
        TextAll = text.subsentences_use_only_one_separator(TextAll)

        # more than one minus: -- or --- signs: replace them
        TextAll = text.replace_regexp(TextAll, "[-][-]+", " ")

        Lines = TextAll.split("\n")
        for LineNum, Line in enumerate(Lines):

            if LineNum % 1000 == 0:
                Percent = int(LineNum / len(Lines)* 100)
                print(f"index create: {Percent} %", flush=True)

            # we replaced all subsentence separators in ONE FUN CALL at the beginning
            _Satus, SubSentences = text.subsentences(Prg, Line, ReplaceSubsentenceEndsToOneSeparator=False)
            for SubSentenceNum, SubSentence in enumerate(SubSentences):
                indexing(WordPositions, WordIndexOnlyLineNums, LineNum, SubSentence, SubSentenceNum)

        Out = []
        for Word, LineNumsInts in WordPositions.items():
            LineNums = [str(Num) for Num in LineNumsInts]
            Out.append(f'"{Word}": [{",".join(LineNums)}]')
        Content="{\n"+"\n,".join(Out) + "\n}"

        util.file_write_with_check(Prg, Fname=FileIndexAbsPath, Content=Content)

    return Created

def indexing(WordPositions, WordIndexOnlyLineNums, LineNum, SubSentence, SubSentenceNum):
    SubSentence = text.remove_non_alpha_chars(SubSentence, " ", CharsKeepThem="-")

    for Word in SubSentence.split(): # split at space, tab, newline
        # TODO: words short form expand:
        # I've -> "I", "have" are two separated words,
        # wouldn't -> would is the real word

        # the list/dict creation here is not a big performance problem
        # util.dict_key_insert_if_necessary(WordPositions, Word, list())
        # util.dict_key_insert_if_necessary(WordIndexOnlyLineNums, Word, dict())
        if Word not in WordPositions:
            WordPositions[Word] = list()
        if Word not in WordIndexOnlyLineNums:
            WordIndexOnlyLineNums[Word] = dict()

        if SubSentenceNum > 99:
            SubSentenceNum = 99
        WordPosition = LineNum*100+SubSentenceNum

        # one word can be more than once in a subsentence. If we
        # detect it once, don't save it again
        if WordPosition not in WordIndexOnlyLineNums[Word]: # save the word only once
            WordPositions[Word].append(WordPosition)
            WordIndexOnlyLineNums[Word][WordPosition] = True