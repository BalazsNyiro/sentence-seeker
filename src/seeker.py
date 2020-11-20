# -*- coding: utf-8 -*-
import document, util, os, text, ui_tkinter_boot_progress_bar, time

Version = "v03_index_in_subsentence"

def be_ready_to_seeking(Prg, Verbose=True, LoadOnlyThese=None):
    print("\n######### Be ready to seeking... #########")
    TimeStart = time.time()
    Prg["DocumentObjectsLoaded"] = \
        document.document_objects_collect_from_dir_documents(
            Prg, VersionSeeker=Version,
            FunSentenceCreate=file_sentence_create,
            FunIndexCreate=file_index_create,
            Verbose=Verbose,
            LoadOnlyThese=LoadOnlyThese
        )

    # not important for normal users, cost: 0.3, 0.4 sec
    # it's only an interesting stat
    #Prg["DocumentObjectsLoadedWordsCounterGlobal"] = text.words_count_in_all_document(Prg)

    util.time_spent("Time Be ready to seeking:", TimeStart)
    if Prg.get("MessagesForUser", []):
        print("\n\n Messages for user:")
        for Msg in Prg["MessagesForUser"]:
            print(f" - {Msg}")
        print("\n", flush=True)

    ui_tkinter_boot_progress_bar.progressbar_close(Prg)

# Tested
def file_sentence_create(Prg, FileSentencesAbsPath, Text="", FileTextAbsPath=""):
    if not os.path.isfile(FileSentencesAbsPath):
        if FileTextAbsPath: # for testing it's easier to get Text from param - and not create/del tmpfile
            _ReadSuccess, Text = util.file_read_all(Prg, Fname=FileTextAbsPath, CheckIsFile=False)
        Sentences = text.sentence_separator(Text)

        SentencesFiltered = []
        KnownSentences = set()

        ###### filter sentences with too much numbers ##################
        for Sentence in Sentences:

            ############## word with/without nums ratio filter ####################
            WordNumRatioLow = False
            WordsHasNum, WordsWithoutNum = util.count_words_with_num(Sentence)
            if WordsWithoutNum >= WordsHasNum * 3:
                WordNumRatioLow = True

            ################### avoid duplications in one text ####################
            if Sentence in KnownSentences:
                Repeated = True
            else:
                Repeated = False
                KnownSentences.add(Sentence)
            #######################################################################

            if WordNumRatioLow and not Repeated:
                SentencesFiltered.append(Sentence)
        ###### filter sentences with too much numbers ##################

        util.file_write_utf8_error_avoid(Prg, FileSentencesAbsPath, "\n".join(SentencesFiltered))

# Tested
def file_index_create(Prg, FileIndexAbsPath, FileSentencesAbsPath):
    if not os.path.isfile(FileIndexAbsPath):
        WordPositions = dict()

        _Success, TextAll = util.file_read_all(Prg, FileSentencesAbsPath, CheckIsFile=False)
        TextAll = TextAll.lower()
        TextAll = text.subsentences_use_only_one_separator(TextAll)

        # more than one minus: -- or --- signs: replace them
        TextAll = text.replace_regexp(TextAll, "[-][-]+", " ")

        Lines = TextAll.split("\n") # one sentence is in one line, it's guaranted
        SubSentenceMultiplyerMinusOne = Prg["SubSentenceMultiplayer"] - 1

        for LineNum, Line in enumerate(Lines):

            # if LineNum % 1000 == 0:
            #     Percent = int(LineNum / len(Lines)* 100)
            #     print(f"index create: {Percent} %", flush=True)

            LineNumMultiplied = LineNum * Prg["SubSentenceMultiplayer"]

            # we replaced all subsentence separators in ONE FUN CALL at the beginning
            _Satus, SubSentences = text.subsentences(Prg, Line, ReplaceSubsentenceEndsToOneSeparator=False)
            for SubSentenceNum, SubSentence in enumerate(SubSentences):
                if SubSentenceNum > SubSentenceMultiplyerMinusOne:
                    SubSentenceNum = SubSentenceMultiplyerMinusOne # the last num that we can represent
                WordPosition = LineNumMultiplied + SubSentenceNum
                indexing(WordPositions, SubSentence, WordPosition)

        Out = []
        for Word, LineNumsInts in WordPositions.items():
            LineNums = [str(Num) for Num in LineNumsInts]
            Out.append(f'"{Word}": [{",".join(LineNums)}]')
        Content="{\n"+"\n,".join(Out) + "\n}"

        util.file_write_with_check(Prg, Fname=FileIndexAbsPath, Content=Content)

def indexing(WordPositions, SubSentence, WordPosition):

    # IMPORTANT: I tried to refactor/reorganise this function,
    # with avoiding join() in remove_non_alpha_chars and local usage of it
    # instead of fun calling but this is the fastest implementation after
    # measuring

    SubSentence = text.remove_non_alpha_chars(SubSentence, " ", CharsKeepThem="-")

    for Word in SubSentence.split(): # split at space, tab, newline
        # TODO: words short form expand:
        # I've -> "I", "have" are two separated words,
        # wouldn't -> would is the real word

        # one word can be more than once in a subsentence. If we
        # detect it once, don't save it again
        if Word not in WordPositions:
            WordPositions[Word] = set()

        if WordPosition not in WordPositions[Word]: # save the word only once
            WordPositions[Word].add(WordPosition)
