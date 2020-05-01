# -*- coding: utf-8 -*-
import document, util, stats, time, os, text, util_json_obj

Version = "a_naive_01"

def seek(Prg, Wanted):
    LinesSelected = []
    stats.save(Prg, "first seek =>")
    TimeStart = time.time()
    ###############################
    CharCounter = 0
    # TODO: use CharCounter
    Result = []
    for FileBaseName, Doc in Prg["DocumentObjectsLoaded"]:
        if Wanted in Doc["Index"]:
            LineNumbers = Doc["Index"][Wanted]
            print("result, linenumbers: ", FileBaseName, LineNumbers)
            Result.append((FileBaseName, LineNumbers))

    ###############################
    TimeEnd = time.time()
    print("\n".join(LinesSelected))
    print("Time USED:", TimeEnd - TimeStart, f"CharCounter: {CharCounter}, page: {CharCounter / 2000}")
    stats.save(Prg, "first seek <=")

def be_ready_to_seeking(Prg):
    Prg["DocumentObjectsLoaded"] = \
        document.document_objects_collect_from_working_dir(
            Prg, Version,
            FunSentenceCreate=file_sentence_create,
            FunIndexCreate=file_index_create
        ).items()

# what is a sentence: https://simple.wikipedia.org/wiki/Sentence
# unfortunatelly I can't analyse the text based on the structure of the text,
# for example to check it after verbs.
#
# Tested
def sentence_separator(Text):
    Text = text.replace_abbreviations(Text)
    Text = text.replace_whitespaces_to_one_space(Text)

    Sentences = []
    SentenceChars = []
    InSentence = False

    InQuotation = False

    for Char in Text:

        ########## BEGINNING ##########
        if Char in text.MarksQuotation:
            if not InQuotation:
                InSentence = True
                InQuotation = True
                # "Adam wrote the letter"  in this situation the first " char belongs to the next sentence, not the previous one
            else:
                InQuotation = False
                # Quotation End can be in the middle of a sentence:
                # For some time past vessels had been met by "an enormous thing," a long

        if not InSentence:
            if Char.isupper(): # it works with special national chars, too. Example: É
                InSentence = True

        ########## BEGINNING ##########

        if InSentence:
            SentenceChars.append(Char)

        if not InSentence:
            if not Sentences: # if it's the first Sentence, Sentences is empty
                SentenceChars.append(Char)
            else:
                Sentences[-1].append(Char)  # if we are over a sentence but the next didn't started then attach it into previous sentence

        ########## CLOSER ##########
        if InSentence and Char in text.SentenceEnds:
            InSentence = False
            Sentences.append(SentenceChars)
            SentenceChars = []
        ########## CLOSER ##########

    if SentenceChars: # if something stayed in collected chars and the sentence wasn't finished, saved it, too
        Sentences.append(SentenceChars)

    RetSentences = [("".join(SentenceChars)).strip() for SentenceChars in Sentences]
    print("\n\nSentences: ", RetSentences)
    return RetSentences

# Tested
def file_sentence_create(Prg, FileSentences, Text="", FilePathOrigText=""):
    if not os.path.isfile(FileSentences):
        if FilePathOrigText: # for testing it's easier to get Text from param - and not create/del tmpfile
            _ReadSuccess, Text = util.file_read_all(Prg, Fname=FilePathOrigText)

        Sentences = sentence_separator(Text)
        util.file_write(Prg, FileSentences, "\n".join(Sentences))

# Tested
def file_index_create(Prg, FileIndex, FileSentences):
    if not os.path.isfile(FileIndex):
        WordIndex = dict()

        # start LineNum from 1
        for LineNum, Line in enumerate(util.file_read_lines(FileSentences), 1):

            # THIS word can be spoiled:
            # word;  for example, I need clean words so remove the not-abc chars

            # I replace with space because:
            # This rock-hard cake is absolutely impossible to eat.
            # We’re looking for a dog-friendly hotel.
            # ’ -   signs has to be replaced with word separator char

            Line = text.remove_not_abc_chars(Line, " ", CharsKeepThem="-")

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


