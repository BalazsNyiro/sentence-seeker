# -*- coding: utf-8 -*-
import text, json, shutil
import sys

def sentence_get_from_result(Prg, Result, ReturnType="complete_sentence"):
    Source = Result["FileSourceBaseName"]
    LineNum = Result["LineNumInSentenceFile"]

    _Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum, Strip=True)

    Url = ""
    if Source in Prg["DocumentsSourceWebpages"]:
        Url = Prg["DocumentsSourceWebpages"][Source]["url"]

    if ReturnType == "separated_subsentences":
        SubSentenceNum = Result["SubSentenceNum"]
        _Status, SubSentenceResult = text.subsentences(Prg, Sentence, SubSentenceNum)

        # split at first match, more than one can be in subsentence
        SubSentencesBefore, SubSentencesAfter = Sentence.split(SubSentenceResult, 1)

        Sentence = {"subsentences_before": SubSentencesBefore,
                    "subsentence_result": SubSentenceResult,
                    "subsentences_after": SubSentencesAfter
                    }

    return Url, Sentence, Source

def theme_actual(Prg):
    ThemeActual = Prg["UiThemes"]["ThemeNameActual"]
    Theme = Prg["UiThemes"][ThemeActual]
    return Theme

def ui_json_answer(Prg,
                   TokenProcessExplainSumma,
                   WordsMaybeDetected,
                   MatchNums__ResultInfo,
                   NewLine="\n"):
    Txt = token_explain_summa_to_text(TokenProcessExplainSumma, NewLine=NewLine) + 2*NewLine
    Reply = {"results": MatchNums__ResultInfo[:Prg["LimitDisplayedSampleSentences"]],
             "token_process_explain": Txt,
             "words_maybe_detected": WordsMaybeDetected}
    Reply = json.dumps(Reply).encode('UTF-8')
    return Reply

def token_explain_summa_to_text(TokenProcessExplainSumma, NewLine="\n", ExplainLimit=64):
    TokenExplainText = []

    if len(TokenProcessExplainSumma) > ExplainLimit:
        return "Too complex Token explaining"

    for Exp in TokenProcessExplainSumma:
        Token, ResultNum = Exp
        TokenExplainText.append(f"{Token}: {ResultNum}")

    return NewLine.join(TokenExplainText)

def title(Prg):
    return f"sentence-seeker: {Prg['DirDocuments']}"

def title_refresh(Prg):
    if Prg["Settings"]["Ui"]["DisplayDirDocInGuiTitle"]:
        print("dir doc is displayed")
        Prg["UiRootObj"].title(title(Prg))
    else:
        print("dir doc is hidden")
        # dir is hidden, because of demo for example :-)
        Prg["UiRootObj"].title("sentence-seeker.net")

# https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
def get_screen_size():
    Width, Height = shutil.get_terminal_size((80, 20))
    return Width, Height


def sentence_convert_to_rows(SentenceColored, SentenceNotColored, WidthWanted):

    Rows = []
    Row = []
    RowWidth = 0

    # prevent\nonly\nnewline connected words
    SentenceColored = SentenceColored.replace("\n", "\n ")
    SentenceNotColored = SentenceNotColored.replace("\n", "\n ")

    WordsNotColored = SentenceNotColored.split(" ")
    for Id, WordColored in enumerate(SentenceColored.split(" ")):
        WordNotColored = WordsNotColored[Id]

        # the length of the words are not evident. they can be colored, for example.
        # The displayedLength is different from real one
        # +1 because there is a space between words

        # if Row is empty:
        WordLenDisplayed = len(WordNotColored)
        if Row: # if row has previous word, space is necessary before
            WordLenDisplayed += 1

        ForcedNewRowAfterWordInsert = False
        if "\n" in WordColored:
            WordColored = WordColored.strip()
            WordNotColored = WordNotColored.strip()
            ForcedNewRowAfterWordInsert = True
            WordLenDisplayed = len(WordNotColored) + 1 # set len again because of strip()

        TooLongWordCantBeFittedAnywhere = WordLenDisplayed > WidthWanted
        WordCanBeInserted = RowWidth + WordLenDisplayed <= WidthWanted

        WordCantBeInsertedBecauseRowIsFull = \
            (not WordCanBeInserted) and (not TooLongWordCantBeFittedAnywhere)

        if WordCanBeInserted:
            Row.append(WordColored)
            RowWidth += WordLenDisplayed

        # if you are unlucky and the word can't be fitted into the wanted width
        # then we have to insert it anyway
        if TooLongWordCantBeFittedAnywhere:
            Rows.append(" ".join(Row)) # close the prev row
            Rows.append(WordColored)          # and insert the too long new one
            Row = []
            RowWidth = 0

        if WordCantBeInsertedBecauseRowIsFull:
            Rows.append(" ".join(Row))
            Row = [WordColored]
            RowWidth = WordLenDisplayed

        if ForcedNewRowAfterWordInsert:
            Rows.append(" ".join(Row)) # close the prev row
            Row = []
            RowWidth = 0

    if Row:
        Rows.append(" ".join(Row))

    return Rows

# return with list of splitted texts: [TextScreen1, TextScreen2]
# one text block fits well on the screen
# the two sentences are similar but in
def text_split_at_screensize(SentencesColored, SentencesNotColored, WidthWanted, HeightWanted):
    TextBlocksScreenSized = []
    Rows = []

    for Id, SentenceColored in enumerate(SentencesColored):
        SentenceNotColored = SentencesNotColored[Id]

        SentenceRows = sentence_convert_to_rows(SentenceColored, SentenceNotColored, WidthWanted)
        if len(SentenceRows) + len(Rows) < HeightWanted:
            Rows.extend(SentenceRows)
        else:
            TextBlocksScreenSized.append("\n".join(Rows))
            Rows = []
            Rows.extend(SentenceRows)

    if Rows:
        TextBlocksScreenSized.append("\n".join(Rows))

    return TextBlocksScreenSized

# in basic case user press key+Enter
# please solve that he has to press only one button
def press_key_in_console(Prg):
    UserReply = input("[p]rev, [n]ext, [q]uery again> ").strip()
    return UserReply
