# -*- coding: utf-8 -*-
import document, util, stats, time, os, text
import sys

Version = "a_naive_01"

def seek(Prg, WordsWantedOneString):
    LinesSelected = []
    stats.save(Prg, "first seek =>")
    TimeStart = time.time()
    ###############################

    Result = dict()
    WordsWanted = text.words_wanted_clean(WordsWantedOneString)

    for FileBaseName, Doc in Prg["DocumentObjectsLoaded"].items():
        LineNums__WordsDetected = text.linenums__words_detected__collect(
            WordsWanted, Doc["Index"])

       # TODO: here sort the results based on
       # - length of sentence (shorter is better)
       # - the words distance (shorter is better)
       # - if it's possible keep the word order?

        if LineNums__WordsDetected:
            for MatchNum, ResultInfos in text.linenumbers_sorted_by_seek_result_length(LineNums__WordsDetected, FileBaseName).items():
                if MatchNum not in Result:
                    Result[MatchNum] = list()
                    # print("DEBUG:::::  ", ResultInfos)
                    Result[MatchNum].extend(ResultInfos)

    ###############################
    TimeEnd = time.time()
    print("\n".join(LinesSelected))
    print("Time USED:", TimeEnd - TimeStart)
    stats.save(Prg, "first seek <=")

    return WordsWanted, Result

def be_ready_to_seeking(Prg):
    Prg["DocumentObjectsLoaded"] = \
        document.document_objects_collect_from_working_dir(
            Prg, Version,
            FunSentenceCreate=file_sentence_create,
            FunIndexCreate=file_index_create
        )

# what is a sentence: https://simple.wikipedia.org/wiki/Sentence
# unfortunatelly I can't analyse the text based on the structure of the text,
# for example to check it after verbs.
#
# Tested

# Tested
def file_sentence_create(Prg, FileSentences, Text="", FilePathOrigText=""):
    if not os.path.isfile(FileSentences):
        if FilePathOrigText: # for testing it's easier to get Text from param - and not create/del tmpfile
            _ReadSuccess, Text = util.file_read_all(Prg, Fname=FilePathOrigText)

        Sentences = text.sentence_separator(Text)
        util.file_write_utf8_error_avoid(Prg, FileSentences, "\n".join(Sentences))

# Tested
def file_index_create(Prg, FileIndex, FileSentences):
    if not os.path.isfile(FileIndex):
        WordIndex = dict()

        # start LineNum from 1
        _Success, TextAll= util.file_read_all(Prg, FileSentences)
        for LineNum, Line in enumerate(TextAll.split("\n")):

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


