# -*- coding: utf-8 -*-
import seeker_logic, text, util_ui, os
import time, msg_errors

from ui_color import *

try:
    import psutil # not available
    PsutilAvailable = True
except:
    PsutilAvailable = False

def cmd_back_to_tty_console(Prg, Wanted):
    # this is a special command but really USEFUL
    # if you use sentence-seeker.py from virtual-console mode where
    # you can change between consoles with Alt+F1, ALT+F2, you can use
    # and editor in one terminal (I use vim) and sentence-seeker.py in
    # another virtual terminal.
    # when you type :back,  the program switch back into the given terminal without
    # any magic with ALT+Fn

    Cmd = Prg["ChangeVirtualConsoleCmd"]
    TerminalNum = "1"
    if " " in Wanted:
        TerminalNum = Wanted.split(" ")[2]
        # SECURITY: allow only these chars
        # Linux has only six virtual consoles
        if TerminalNum not in list('123456'):
            TerminalNum = "1"

    os.system(f"{Cmd} {TerminalNum}")
    #################################################

def seek_and_display(Prg, Wanted):
    # Wanted = ":info"
    ##################################################################
    if Wanted == "b":         # this one char conversion works only in console mode because
        Wanted = ":back"        # you can use back only in virtual console
    # 'b 1', 'b 2' switch to given virtual console is working, too
    elif len(Wanted) == 3 and Wanted[:2] == "b ":
        Wanted = ":back " + Wanted[2]
    if ":back" == Wanted[:5] and Prg["CommandBackToTtyConsoleAvailable"]:
        cmd_back_to_tty_console(Prg, Wanted)
        return
    ##################################################################

    TimeLogicStart = time.time()
    ResultsTotalNum = 0

    Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowOddOnly"] = True
    ReturnType = "complete_sentence" # in separated_subsentence case the non-alphabhet chars become separators.

    DisplaySeekResult = False

    ## THIS IS A GOOD EXAMPLE FOR A CONSOLE SPECIFIC COMMAND ###
    if Wanted == ":console_specific_command" or Wanted == ":console_specific_command" or Wanted == "console_specific_command":
        pass
        # MatchNums__ResultInfo = []
        # MatchNums__ResultInfo.append(text.sentence_builder_from_spec_command(Prg, "display something"))
        # MatchNums__ResultInfo.append(text.sentence_builder_from_spec_command(Prg, "second row"))
        # WordsDetected = {"highlighted", "important", "words"}
        # DisplaySeekResult = True
    else:
        TokenProcessExplainSumma, WordsDetected, MatchNums__ResultInfo, ResultsTotalNum, DisplaySeekResult, _TextFromCommandResult = seeker_logic.seek(Prg, Wanted)
        ExplainLimit = 24
        TokenExplain = util_ui.token_explain_summa_to_text(TokenProcessExplainSumma, ExplainLimit=ExplainLimit)

        SentencesExplain = []
        if TokenExplain:
            for Line in (TokenExplain+"\n").split("\n"):
                SentencesExplain.append(text.sentence_builder_from_spec_command(Prg, Line))
        SentencesExplain.extend(MatchNums__ResultInfo)
        MatchNums__ResultInfo = SentencesExplain

    # TimeLogicUsed = time.time() - TimeLogicStart
    if DisplaySeekResult:
        sentence_result_all_display(Prg, MatchNums__ResultInfo, WordsDetected, ReturnType=ReturnType, ResultsTotalNum=ResultsTotalNum)
    # print(f"Results Total: {ResultsTotalNum}")
    # print("Time logic: ", TimeLogicUsed)

def user_interface_start(Prg, Ui, QueryAsCmdlineParam=""):
    # On Linux and I hope on Mac, we can use history in console
    if Prg["OsIsUnixBased"]:
        import readline

    user_welcome_message(Prg, Ui)
    # neverending cycle :-)

    while True:
        if QueryAsCmdlineParam:
            Wanted = QueryAsCmdlineParam.strip()
        else:

            ColorWanted = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorWanted"])
            ColorUserInfo = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorUserInfo"])
            ColorBattery = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorBattery"])

            BatteryInfo = ""
            if Prg["SettingsSaved"]["Ui"]["Console"]["BatteryInfoShow"]:
                if PsutilAvailable:
                    Battery = psutil.sensors_battery()
                    Plugged = Battery.power_plugged
                    Percent = int(Battery.percent)

                    Plugged = " <-" if Plugged else ""
                    Plugged = ""

                    BatteryInfo = f"{ColorBattery}{Percent}%{Plugged} "
                else: # the user wants to display battey info but module is missing
                    print(msg_errors.ModuleMissingPsutil)

            Scope = Prg["SettingsSaved"]["Scope"]
            print(f"\n{BatteryInfo}{ColorWanted}scope {Scope} >>>{color_reset()}", end="")
            # if user uses backspace in console, the space stops it to go back to the '...wanted>>' part
            # of the line. Without input('display') param, the backspace has side effect on the line
            # and colorful part disappears
            # you can't insert color information into input("colored prompt") fun because terminal can't detect
            # correctly the end of the line if you enter color information into input()

            LocationPrev, EventNamePrev, EventValuePrev = Prg["UserInputHistory"].event_last()
            if LocationPrev == "ResultViewer" and EventNamePrev == "KeyQuit" and EventValuePrev == "b":
                Wanted = ":back"
                Location = "ui_console"
                Prg["UserInputHistory"].event_new(Location, "get_user_input", "back_exit_from_resultviewer")
            else:
                Wanted = input(" ").strip()

            if Wanted in Prg["SettingsSaved"]["Ui"]["CommandsExit"]:
                print(color_reset())
                break
        seek_and_display(Prg, Wanted)
        # if we got the query from command line, give it back and exit
        if QueryAsCmdlineParam:
            break

#########################################

def user_welcome_message(Prg, UserInterface):
    if UserInterface == "console":
        ColorInf = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorUserInfo"])
        ColorHigh = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorUserInfoHigh"])

        print()
        print(Prg["Licenses"])
        print()
        print(f"{ColorInf}example search: {ColorHigh}looks AND like AND bird")
        print(f"{ColorInf}example search: {ColorHigh}pronouns:personal AND have:all AND iverb:pp")
        print(f"{color('Default')}")
        print(f"{ColorInf}Exit: {ColorHigh}:exit :quit :q q ")
        print(f"{ColorInf}Help: {ColorHigh}:help :h h")

        AllowedOutput = Prg['DirDocuments']
        if not Prg["SettingsSaved"]["Ui"]["DisplayPersonalInfo"]:
            AllowedOutput = "(demo mode) probably homedir/.sentence-seeker/documents"
        print(f"{color('Yellow')}Documents dir: {AllowedOutput}{color_reset()}")


def sentence_result_one(Prg, Result, WordsDetected, RowNumDisplayed, ReturnType="separated_subsentences"):
    ColorDefault = color("Default")

    if Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowOddOnly"]:
        ColorBefore = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowOdd"])
    else:
        ColorBefore = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowEven"]) if RowNumDisplayed % 2 == 0 \
            else      color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowOdd"])

    ColorDetected = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorWordDetected"])
    ColorResultNum = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowNum"])
    return util_ui.sentence_get_from_result_oop(Prg,
                                                Result,
                                                ReturnType=ReturnType,
                                                ColorBefore=ColorBefore,
                                                ColorAfter=ColorDefault,
                                                ColorDetected=ColorDetected,
                                                ColorResultNum=ColorResultNum,
                                                RowNumDisplayed=RowNumDisplayed,
                                                WordsDetected=WordsDetected)

def sentence_result_all_display(Prg, SentenceStruct, WordsDetected, ReturnType="separated_subsentences", ResultsTotalNum=0):
    CharEnter = chr(13)
    CharEscape = chr(27) # it's a problem because some special key's code starts with 27, too

    NextKeys = {"n", " ", "j", CharEnter, "KeyArrowDown", "KeyArrowRight"} # B = arrowDown, C=arrowRight buttons, fun return with these chars if I press arrow buttons
    PrevKeys = {"p", "k", "KeyBackSpace", "KeyArrowUp", "KeyArrowLeft"}
    QuitKeys = {"q"}

    # the :back function can work from GUI->tty_console, too,
    # maybe IsOsLinux==True would be enough?
    if Prg["CommandBackToTtyConsoleAvailable"]:
        QuitKeys.add("b") # in tty console you can go back to a given console

    ScreenWidth, ScreenHeight = util_ui.get_screen_size()

    IdNow = 0
    PageNum = 0
    PageTopSentenceId = dict() # pagenum, sentenceId
    PageTopSentenceId[PageNum] = IdNow

    RowNumDisplayed = len(SentenceStruct)
    NoResult = RowNumDisplayed == 0

    Step = 0

    ColorInfo = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorUserInfo"])
    ColorHigh = color(Prg["SettingsSaved"]["Ui"]["Console"]["ColorUserInfoHigh"])

    Location = "ResultViewer" # the user is in Result Viewer now

    while True:
        FreeLines = ScreenHeight - 3

        # print("PageNum", PageNum)
        SomethingDisplayed = False

        IdNow = PageTopSentenceId[PageNum]
        print("")
        while FreeLines:
            LastResultDisplayed = (IdNow >= RowNumDisplayed)
            if NoResult or LastResultDisplayed: break

            SentenceObject = sentence_result_one(Prg, SentenceStruct[IdNow], WordsDetected, IdNow, ReturnType=ReturnType)
            RowsRendered = SentenceObject.render_console(ScreenWidth, AlignRight=2) #len(str(RowNumDisplayed)))
            RowsRenderedLen = len(RowsRendered)

            if RowsRenderedLen <= FreeLines:
                print("\n".join(RowsRendered))
                FreeLines -= RowsRenderedLen
                IdNow += 1
                SomethingDisplayed = True
            else:
                break

        if SomethingDisplayed:
            PageTopSentenceId[PageNum+1] = IdNow

        if Step == 0: # ask new instruction if no more steps
            def high(T) :
                return f"{ColorHigh}{T}{ColorInfo}"

            TextPrev  = f"{high('p')}rev"
            TextNext  = f"{high('n')}ext"
            TextQuery = f"{high('q')}uery"

            TextBack = ""
            if Prg["CommandBackToTtyConsoleAvailable"]:
                TextBack = f"{high('b')}ackTty"

            TextTotal = f"{ColorInfo}#{high(ResultsTotalNum)}"
            TextVim = f"{ColorInfo}vim: {high('j')}, {high('k')} {color('Default')}"
            UserInfo = f"{TextPrev} {TextNext} {TextQuery} {TextBack}  {TextTotal}    {TextVim}{color('Default')}"

            if RowNumDisplayed == 0: # return to new search if no result
                print(f"{ColorHigh}No result!{color('Default')}")
                break

            UserReply = util_ui.press_key_in_console(UserInfo)
            # print("user reply:", UserReply)
            if len(UserReply) == 1 and UserReply in QuitKeys:
                Prg["UserInputHistory"].event_new(Location, "KeyQuit", UserReply)
                break

            if UserReply in NextKeys:
                Step = 1
                util_ui.clear_screen(ScreenHeight)
                Prg["UserInputHistory"].event_new(Location, "KeyPageNext", UserReply)

            if UserReply in PrevKeys:
                Step = -1
                util_ui.clear_screen(ScreenHeight)
                Prg["UserInputHistory"].event_new(Location, "KeyPagePrev", UserReply)

            if UserReply == "KeyHome":
                Step = -PageNum
                util_ui.clear_screen(ScreenHeight)
                Prg["UserInputHistory"].event_new(Location, "KeyPageFirst", UserReply)

            if UserReply == "KeyEnd":
                Step = RowNumDisplayed
                # theoretically it's wrong because lot of results can be on a page
                # but I guess one result will be smaller than one page so it's a good upper limit
                util_ui.clear_screen(ScreenHeight)
                Prg["UserInputHistory"].event_new(Location, "KeyPageLast", UserReply)

        if Step > 0:
            if PageNum+1 in PageTopSentenceId:
                NextIdInResults = PageTopSentenceId[PageNum + 1] < RowNumDisplayed
                if NextIdInResults:
                    PageNum += 1
                else:
                    print("No more result")
                    Step = 0
            else:
                Step = 0

            if Step > 0: # guard condition, sooner or later Step -> 0
                Step -= 1

        if Step < 0: # go back to the head
            Step += 1
            if PageNum > 0:
                PageNum -= 1
            else:
                print("This is the first page!")
                Step = 0
        # print("Step:", Step)
