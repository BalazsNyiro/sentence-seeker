# -*- coding: utf-8 -*-
import text, json, shutil, util
import sys

from ui_color import *

try:
    import tty
    import termios
    TtyTermiosModulesAreAvailable = True
except ImportError:
    print("tty or termios is not available")
    TtyTermiosModulesAreAvailable = False

try:
    import msvcrt # on Windows
    MsvCrtModuleAvailable = True
except ImportError:
    MsvCrtModuleAvailable = False

########################################################################################################################
class WordObj():
    def __str__(self):
        return self.Txt

    def __init__(self, Txt, WordsDetected=set(), ColorBasic=None, ColorAfter=None, ColorDetected=None):
        self.Txt = Txt
        self.ColorBefore = ColorBasic
        self.ColorAfter = ColorAfter
        self.ColorDetected = ColorDetected

        self.Detected = False

        # the case-insensivity is important because words can start with upper/lower case
        # chars, too

        # if util.word_only_abc_chars(Txt).lower() in WordsDetected or Txt in WordsDetected:
        TxtLow = Txt.lower()
        if TxtLow in WordsDetected:
            # if it's exactly in detected: special signs, for help documentation, = sign for example
            self.Detected = True

        else:

            # TODO: refactor it to a separated fun and create tests
            # seek: (elephant AND horse)
            # one result: ...  for neither horse nor mule can bear to listen to an elephant’s voice
            # here the elephant wasn't highlighted
            # and (elephant not, too
            # so solve this problem: what happens if this is a word plus some extra char.  example: elephant!
            for WordDetected in WordsDetected:
                if len(WordDetected) > len(TxtLow):
                    continue # don't check if Detected can't be the part of Txt

                if TxtLow.startswith(WordDetected):
                    # elephant's -> elephant is matching
                    NextCharAfterWordDetected = TxtLow[len(WordDetected)]
                    if not util.abc_char(NextCharAfterWordDetected):
                        self.Detected = True
                        break

                elif TxtLow.endswith(WordDetected):
                    # non-elephant  in this case '-' is the prev char
                    PrevCharBeforeWordDetected = TxtLow[-1-len(WordDetected)]
                    if not util.abc_char(PrevCharBeforeWordDetected):
                        self.Detected = True
                        break

                # non-elephant!  here the elephant is surrounded by non-alpha chars
                elif WordDetected in TxtLow:
                    Fragments = TxtLow.split(WordDetected)
                    CharPos = -1 # check the first, then the last char, then first again, then last. -1, 0, -1, 0
                    SurroundedWithNonAbc = True
                    for Elem in Fragments:
                        if util.abc_char(Elem[CharPos]):
                            SurroundedWithNonAbc = False
                            break
                        if CharPos == -1: CharPos =  0
                        else:             CharPos = -1
                    if SurroundedWithNonAbc:
                        self.Detected = True
                        break

        self.Len = len(Txt)

    def render(self, ColorSentence):
        Out = []

        if self.Detected and self.ColorDetected:
            Out.append(self.ColorDetected)

        elif self.ColorBefore:
            Out.append(self.ColorBefore)

        if self.Txt:
            Out.append(self.Txt)

        if self.ColorAfter:
            Out.append(self.ColorAfter)
        else:
            if ColorSentence:
                Out.append(ColorSentence)
        # print(Out)
        return "".join(Out)

class SentenceObj():
    def render_console(self, WidthMax, AlignRight=None):

        def row_len(Row):
            SpaceNum = len(Row) - 1 if Row else 0
            CharNum = 0
            for W in Row:
                CharNum += W.Len
            return SpaceNum + CharNum

        if self.RowNumDisplayed is not None:
            if AlignRight is None:
                HumanResultNum = str(self.RowNumDisplayed + 1)
            else:
                HumanResultNum = f"{self.RowNumDisplayed + 1: <{AlignRight}}"

            Rows = [[WordObj(HumanResultNum, ColorBasic=self.ColorResultNum, ColorAfter=self.ColorBasic)]]
        else:
            Rows = [[]]

        for Word in self.Words:
            RowLast = Rows[-1]

            SpaceNeed = Word.Len
            if row_len(RowLast):
                SpaceNeed += 1

            if row_len(RowLast) + SpaceNeed <= WidthMax:
                RowLast.append(Word)
            else:
                Rows.append([Word])

        #######################################
        RowsRendered = []

        for Row in Rows:
            Rendered = []
            for Word in Row:
                W = Word.render(self.ColorBasic)
                if not RowsRendered and self.ColorBasic:
                    W += self.ColorBasic
                Rendered.append(W)
            RowsRendered.append(" ".join(Rendered))

        if self.ColorAfter:
            RowsRendered[-1] += self.ColorAfter

        if self.Prg:
            HumanResultNumLen = len(str(HumanResultNum))
            Indent = " " * (HumanResultNumLen+1)  # indentation instead of row numbers, plus ONE space
            if self.Prg["SettingsSaved"]["Ui"]["DisplaySourceUrlBelowSentences"]:
                if self.Url: # the help lines for example don't have source/Url
                    ColorUrl = color(self.Prg["SettingsSaved"]["Ui"]["Console"]["ColorSentenceUrl"])
                    RowsRendered.append(Indent + ColorUrl + self.Url + color_reset())
            if self.Prg["SettingsSaved"]["Ui"]["DisplaySourceFileNameBelowSentences"]:
                if self.Source:
                    ColorSource = color(self.Prg["SettingsSaved"]["Ui"]["Console"]["ColorSentenceSource"])
                    RowsRendered.append(Indent + ColorSource + self.Source + color_reset())

        #######################################
        # print(RowsRendered)
        return RowsRendered

    def add_word(self, Txt, ColorBasic=None, ColorAfter=None, ColorDetected=None):
        Txt = Txt.strip()
        if not Txt: return # be sure, insert only real words, not empty strings or whitespaces

        W = WordObj(Txt,
                    WordsDetected=self.WordsDetected,
                    ColorBasic=ColorBasic,
                    ColorAfter=ColorAfter,
                    ColorDetected=ColorDetected)
        self.Words.append(W)

    # "more word in one big string"
    def add_big_string(self, BigString):
        if BigString.strip():
            for WordTxt in BigString.split(" "):
                self.add_word(WordTxt, ColorDetected=self.ColorDetected)

    def __init__(self, Sentence=None,
                 ColorBasic=None, ColorAfter=None,
                 ColorDetected=None, ColorResultNum=None,
                 RowNumDisplayed=None, WordsDetected=set(),
                 Url=None, Source=None, Prg=dict()):
        self.Prg = Prg
        self.ColorBasic = ColorBasic
        self.ColorAfter = ColorAfter
        self.ColorDetected = ColorDetected
        self.ColorResultNum = ColorResultNum
        self.RowNumDisplayed = RowNumDisplayed
        self.Words = []
        self.WordsDetected = WordsDetected
        self.Url = Url
        self.Source = Source

        self.add_big_string(Sentence)

def sentence_get_from_result_oop(Prg, Result,
                                 ReturnType="separated_subsentences",
                                 ColorBefore=None,
                                 ColorAfter=None,
                                 ColorDetected=None,
                                 ColorResultNum=None,
                                 RowNumDisplayed=None,
                                 WordsDetected=set()):

    Url, Txt, Source = sentence_text_from_obj(Prg, Result, ReturnType=ReturnType)

    if util.is_dict(Txt):
        Sentence = SentenceObj(ColorBasic=ColorBefore,
                               ColorAfter=ColorAfter,
                               ColorDetected=ColorDetected,
                               ColorResultNum=ColorResultNum,
                               RowNumDisplayed=RowNumDisplayed,
                               WordsDetected=WordsDetected,
                               Url=Url, Source=Source, Prg=Prg)
        Sentence.add_big_string(Txt["subsentences_before"])
        Sentence.add_big_string(Txt["subsentence_result"])
        Sentence.add_big_string(Txt["subsentences_after"])
        return Sentence
    else:
        return SentenceObj(Txt,
                           ColorBasic=ColorBefore,
                           ColorAfter=ColorAfter,
                           ColorDetected=ColorDetected,
                           ColorResultNum=ColorResultNum,
                           RowNumDisplayed=RowNumDisplayed,
                           WordsDetected=WordsDetected,
                           Url=Url, Source=Source, Prg=Prg)

def sentence_text_from_obj(Prg, SentenceObj, ReturnType="separated_subsentences"):
    Source = SentenceObj.FileSourceBaseName

    # if sentence obj knows the sentence, use that, for example in help info
    if SentenceObj.Sentence != "-":
        Sentence = SentenceObj.Sentence
    else:
        LineNum = SentenceObj.LineNumInSentenceFile
        _Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum, Strip=True)

    Url = ""
    if Source in Prg["DocumentsSourceWebpages"]:
        Url = Prg["DocumentsSourceWebpages"][Source]["url"]

    if ReturnType == "separated_subsentences":

        # theoretically more than one subsentence can be found in a sentence
        ResultSubSentenceNumMin = SentenceObj.SubSentenceNumMin
        ResultSubSentenceNumMax = SentenceObj.SubSentenceNumMin

        SubSentencesBefore = []
        SubSentencesResult = []
        SubSentencesAfter = []

        _, SubSentences = text.subsentences(Prg, Sentence, KeepSubsentenceEnd=True)
        for SubSenNum, SubSentence in enumerate(SubSentences):
            if SubSenNum < ResultSubSentenceNumMin:   SubSentencesBefore.append(SubSentence)
            elif SubSenNum > ResultSubSentenceNumMax: SubSentencesAfter.append(SubSentence)
            else:                                     SubSentencesResult.append(SubSentence)

        Sentence = {"subsentences_before": " ".join(SubSentencesBefore),
                    "subsentence_result" : " ".join(SubSentencesResult),
                    "subsentences_after" : " ".join(SubSentencesAfter)}

    return Url, Sentence, Source

########################################################################################################################

def theme_actual(Prg):
    ThemeActual = Prg["UiThemes"]["ThemeNameActual"]
    Theme = Prg["UiThemes"][ThemeActual]
    return Theme

def ui_json_answer(Prg,
                   TokenProcessExplainSumma,
                   WordsDetected,
                   SentenceObjects,
                   NewLine="\n"):

    MaximizedSentences = SentenceObjects[:Prg["SettingsSaved"]["Ui"]["LimitDisplayedSentences"]]
    SentencesToJson = [Sen.to_json() for Sen in MaximizedSentences]

    Txt = token_explain_summa_to_text(TokenProcessExplainSumma, NewLine=NewLine) + 2*NewLine
    Reply = {"results": SentencesToJson,
             "token_process_explain": Txt,  # below list() is nececcary because
             "words_detected": sorted(list(WordsDetected))} # Words set can't be converted to json
    Reply = json.dumps(Reply).encode('UTF-8')
    return Reply

def token_explain_summa_to_text(TokenProcessExplainSumma, NewLine="\n", ExplainLimit=64):
    TokenExplainText = []
    if TokenProcessExplainSumma: # show warning if there is something in ExplainSumma
        TokenExplainText.append("Sentence duplications are removed so displayed result num can be different from Explained!")

    if len(TokenProcessExplainSumma) > ExplainLimit:
        return "Too complex Token explaining"

    for Token, ResultNum in TokenProcessExplainSumma.items():
        TokenExplainText.append(f"{Token}: {ResultNum}")

    return NewLine.join(TokenExplainText)

def title(Prg):
    return f"sentence-seeker Documents dir: {Prg['DirDocuments']}"

def title_refresh(Prg):
    if Prg["UiRootObj"]: # if gui is active
        if Prg["SettingsSaved"]["Ui"]["DisplayPersonalInfo"]:
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

        # if there is nothing before the word, than the length is the num of chars:
        WordLenDisplayed = len(WordNotColored)
        if Row: # It's not the first word, space is necessary before
            WordLenDisplayed += 1

        ForcedNewRowAfterWordInsert = False
        if "\n" in WordColored:
            WordColored = WordColored.replace("\n", "")
            WordNotColored = WordNotColored.replace("\n", "")
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
            if Row:
                Rows.append(" ".join(Row)) # close the prev row
            Rows.append(WordColored)          # and insert the too long new one
            Row = []
            RowWidth = 0

        if WordCantBeInsertedBecauseRowIsFull:
            if Row:
                Rows.append(" ".join(Row))
            Row = [WordColored]
            RowWidth = WordLenDisplayed

        if ForcedNewRowAfterWordInsert:
            if Row:
                Rows.append(" ".join(Row)) # close the prev row
            Row = []
            RowWidth = 0

    if Row:
        Rows.append(" ".join(Row))

    return Rows

# maybe in the future this module would be a better solution,
# https://pypi.org/project/readchar/
# but I don't want external installs

# in basic case user press key+Enter
# please solve that he has to press only one button
#  READ: https://stackoverflow.com/questions/510357/how-to-read-a-single-character-from-the-user
def keypress_detect_linux():
    Fd = sys.stdin.fileno()

    OldSettings = termios.tcgetattr(Fd)
    Char = ""
    try:
        tty.setraw(sys.stdin.fileno())
        Char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(Fd, termios.TCSADRAIN, OldSettings)
    return Char

def press_key_in_console(Msg, MsgEnd=""):
    # typically on Linux
    print(Msg, end=MsgEnd, flush=True)

    if TtyTermiosModulesAreAvailable:
        Reply = keypress_detect_linux() # in simple case it's one character
        ReplyOrig = Reply

        ###################### Linux ###########3##################
        if ord(Reply) == 27: # more than one char arrives, special keys

            Char2 = keypress_detect_linux()
            Char3 = keypress_detect_linux()
            print("Char2 >>", Char2, ord(Char2))
            print("Char3 >>", Char3, ord(Char3))

            ############# X11 keycodes, in Linux GUI ##################
            if Char2 == "[" and Char3 == "A": Reply = "KeyArrowUp"
            if Char2 == "[" and Char3 == "B": Reply = "KeyArrowDown"
            if Char2 == "[" and Char3 == "C": Reply = "KeyArrowRight"
            if Char2 == "[" and Char3 == "D": Reply = "KeyArrowLeft"
            if Char2 == "[" and Char3 == "H": Reply = "KeyHome"
            if Char2 == "[" and Char3 == "F": Reply = "KeyEnd"

            ##########  Linux virtual consoles: ctrl+alt+F1, different in last char  ########
            if Char2 == "[" and Char3 == "1": Reply = "KeyHome"
            if Char2 == "[" and Char3 == "4": Reply = "KeyEnd"

        # backspace: 127
        # enter: 13
        # escape: 27
        # home: 7
        # end:
        CharCodes = ",".join([str(ord(Char)) for Char in ReplyOrig])
        # print("Reply received: ", Reply, CharCodes)
        # sys.exit()

        if ord(ReplyOrig) == 127: Reply = "KeyBackSpace"

        print() # newline after message line (where we received user input at the end of the row
        return Reply

    if MsvCrtModuleAvailable: # on Windows
        Reply = msvcrt.getwch()
        # print("Char win os1", ord(Reply), Reply)
        if Reply == chr(8): Reply = "KeyBackSpace"

        if Reply == chr(224): # special keys, home/end, left, right
            Reply = msvcrt.getwch()
            # print("Char win os2", ord(Reply), Reply)
            if Reply == chr(71): Reply = "KeyHome"
            if Reply == chr(79): Reply = "KeyEnd"

            if Reply == chr(72): Reply = "KeyArrowUp"
            if Reply == chr(75): Reply = "KeyArrowLeft"
            if Reply == chr(77): Reply = "KeyArrowRight"
            if Reply == chr(80): Reply = "KeyArrowDown"

        print()
        return Reply

    # basic communication solution, type reply and press Enter
    UserReply = input(Msg).strip()
    return UserReply[0] # caller want only once char back

def clear_screen(ScreenHeight):
    print("\n"*ScreenHeight) # clear screen

def on_off(BooleVal): # convert True/False to On/Off to display config values
    if BooleVal:
        return "On"
    return "Off"