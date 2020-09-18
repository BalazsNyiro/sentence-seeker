# -*- coding: utf-8 -*-
import document, util, os, text, ui_tkinter_boot_progress_bar

Version = "v03_index_in_subsentence"

def be_ready_to_seeking(Prg, Verbose=True, LoadOnlyThese=None):
    Prg["DocumentObjectsLoaded"] = \
        document.document_objects_collect_from_working_dir(
            Prg, Version,
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
                print(f"index create: {Percent} %", flush=True)

            # THIS word can be spoiled:
            # word;  for example, I need clean words so remove the not-abc chars

            # I replace with space because:
            # This rock-hard cake is absolutely impossible to eat.
            # We’re looking for a dog-friendly hotel.
            # ’ -   signs has to be replaced with word separator char

            # more than one minus: -- or --- signs: replace them

            Line = text.replace_regexp(Line, "[-][-]+", " ")

            _Satus, SubSentences = text.subsentences(Prg, Line)
            for SubSentenceNum, SubSentence in enumerate(SubSentences):
                indexing(WordIndex, WordIndexOnlyLineNums, LineNum, SubSentence, SubSentenceNum)

        Out = []
        for Word, LineNums in WordIndex.items():
            Out.append(f'"{Word}": [{",".join(LineNums)}]')
        Content="{\n"+"\n,".join(Out) + "\n}"

        util.file_write_with_check(Prg, Fname=FileIndex, Content=Content)

    return Created

def indexing(WordIndex, WordIndexOnlyLineNums,  LineNum, SubSentence, SubSentenceNum):
    SubSentence = text.remove_non_alpha_chars(SubSentence, " ", CharsKeepThem="-")

    for Word in SubSentence.split(): # split at space, tab, newline
        # TODO: words short form expand:
        # I've -> "I", "have" are two separated words,
        # wouldn't -> would is the real word
        util.dict_key_insert_if_necessary(WordIndex, Word, list())
        util.dict_key_insert_if_necessary(WordIndexOnlyLineNums, Word, dict())

        if SubSentenceNum > 99:
            SubSentenceNum = 99
        Index = f"{LineNum*100+SubSentenceNum}"
        if Index not in WordIndexOnlyLineNums[Word]: # save the word only once
            WordIndex[Word].append(Index)
            WordIndexOnlyLineNums[Word][Index] = True