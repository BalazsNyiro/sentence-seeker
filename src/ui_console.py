# -*- coding: utf-8 -*-
import seeker_logic, text, util_ui
import time

def seek_and_display(Prg, Wanted):
    TimeLogicStart = time.time()
    TokenProcessExplainSumma, WordsMaybeDetected, MatchNums__ResultInfo, ResultsTotalNum = seeker_logic.seek(Prg, Wanted)
    TimeLogicUsed = time.time() - TimeLogicStart

    sentence_result_all_display(Prg, MatchNums__ResultInfo, WordsMaybeDetected)
    print(f"Results Total: {ResultsTotalNum}")
    print("Time logic: ", TimeLogicUsed)

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
            Wanted = input("\nwanted> ").strip()

            if not Wanted:
                print(color_reset(Prg))
                break
        seek_and_display(Prg, Wanted)
        # if we got the query from command line, give it back and exit
        if QueryAsCmdlineParam:
            break

#########################################

def user_welcome_message(Prg, UserInterface):
    if UserInterface == "console":
        print()
        print(Prg["Licenses"])
        print()
        print("interesting search: looks, like, bird")
        print("interesting search: elephant")
        print()
        print("Exit:  Enter only")
        print("Help:  :help + Enter")
        print(f"{color(Prg, 'Yellow')}Docs dir: {Prg['DirDocuments']}{color_reset(Prg)}")

def sentence_result_one(Prg, Result, WordsMaybeDetected, ResultNum):
    ColorDefault = color(Prg, "Default")
    ColorBefore = color(Prg, "Green") if ResultNum % 2 == 0 else ColorDefault
    ColorDetected = color(Prg, "Yellow")
    ColorResultNum = color(Prg, "Red")
    return util_ui.sentence_get_from_result_oop(Prg,
                                                Result,
                                                ReturnType="separated_subsentences",
                                                ColorBefore=ColorBefore,
                                                ColorAfter=ColorDefault,
                                                ColorDetected=ColorDetected,
                                                ColorResultNum=ColorResultNum,
                                                ResultNum=ResultNum,
                                                WordsMaybeDetected=WordsMaybeDetected)

def sentence_result_all_display(Prg, SentenceStruct, WordsMaybeDetected):
    CharEnter = chr(13)
    CharBackspace = chr(127)
    CharEscape = chr(27)

    NextChars = "n jBC"+ CharEnter # B = arrowDown, C=arrowRight buttons, fun return with these chars if I press arrow buttons
    PrevChars = "pkAD" + CharBackspace # A: arrowUp, D: arrowLeft
    QuitChars = "q" + CharEscape
    Msg = "[p]rev [n]ext [q]uery again."

    ScreenWidth, ScreenHeight = util_ui.get_screen_size()

    IdNow = 0
    PageNum = 0
    PageTopSentenceId = dict() # pagenum, sentenceId
    PageTopSentenceId[PageNum] = IdNow

    ResultsNum = len(SentenceStruct)
    NoResult = ResultsNum == 0

    Step = 0
    while True:
        FreeLines = ScreenHeight - 3

        # print("PageNum", PageNum)
        SomethingDisplayed = False

        IdNow = PageTopSentenceId[PageNum]
        print("")
        while FreeLines:
            LastResultDisplayed = (IdNow >= ResultsNum)
            if NoResult or LastResultDisplayed: break

            SentenceObject = sentence_result_one(Prg, SentenceStruct[IdNow], WordsMaybeDetected, IdNow)
            RowsRendered = SentenceObject.render_console(ScreenWidth)
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
            UserReply = util_ui.press_key_in_console(f"{Msg}   total: {ResultsNum}")

            if len(UserReply) == 1 and UserReply in QuitChars: break

            if UserReply in NextChars:
                Step = 1
                util_ui.clear_screen(ScreenHeight)

            if UserReply in PrevChars:
                Step = -1
                util_ui.clear_screen(ScreenHeight)

            if UserReply == "KeyHome":
                Step = -PageNum
                util_ui.clear_screen(ScreenHeight)

            if UserReply == "KeyEnd":
                Step = ResultsNum
                # theoretically it's wrong because lot of results can be on a page
                # but I guess one result will be smaller than one page so it's a good upper limit
                util_ui.clear_screen(ScreenHeight)

        if Step > 0:
            if PageNum+1 in PageTopSentenceId:
                NextIdInResults = PageTopSentenceId[PageNum + 1] < ResultsNum
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


# https://www.geeksforgeeks.org/formatted-text-linux-terminal-using-python/
# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
Colors = {
    'Black':        '30',        'Bright Black':   '90',
    'Red':          '31',        'Bright Red':     '91',
    'Green':        '32',        'Bright Green':   '92',
    'Yellow':       '33',        'Bright Yellow':  '93',
    'Blue':         '34',        'Bright Blue':    '94',
    'Cyan':         '36',        'Bright Magenta': '95',
    'White':        '37',        'Bright Cyan':    '96',
    'Default':      '39',        'Bright White':   '97',

    'Plain' :       '0',    # xfce4-term    gnome-term
    'Bold':         '1',    # +                +
    'Italic':       '3',    # -                +
    'Underline':    '4',
    'Blink':        '5',

    # swap foreground and bg colour
    'Reverse':        '7',        
    
    'CursorHide':    '?25l',
    'CursorShow':    '?25h'
}
def color_reset(Prg):
    return color(Prg, "Plain")+color(Prg, "Default")

CSI = '\033[' # echo -e "\x1b[93;41m"  # example  \x1b is \033 in python


__color_name_last_used=["Default"]
__style_last_used=["Plain"]
def color(Prg, ColorName, CnameBackground=""):

    if Prg["OsIsWindows"]: return ""
    # MAYBE: win terminal has color display option, detailed here:
    # https://stackoverflow.com/questions/2048509/how-to-echo-with-different-colors-in-the-windows-command-line
    
    # https://devblogs.microsoft.com/commandline/updating-the-windows-console-colors/



    ColorBackground=""
    global __color_name_last_used, __style_last_used

    # print('\033[38;5;188;48;5;22mAlma')
    try: # ha 256 szinu tablazatbol dolgozunk, ColorName egy szam:
        ColorFg = "38;5;" + str( int(ColorName) ) # ha ez sikerul, akkor csak szamot kaptunk - amit visszaalakitunk stringge
        if CnameBackground:
            ColorBackground = ";48;5;" + str(int(CnameBackground))
        ControlChars = ColorFg + ColorBackground +  "m" 
        # print(ControlChars)
        return     CSI + ControlChars # 38: foreground

    except: # ha ColorName szoveges, tehat a fenti tablazatbol kell kivalasztani vmit
        if CnameBackground:
            if CnameBackground not in Colors:
                print("Color name error, not in table: ", CnameBackground)
            CodeBg = Colors[CnameBackground]
            if len(CodeBg) == 2:
                CodeBg = str(int(CodeBg) + 10)
            ColorBackground = ";" + CodeBg
            
        if "Prev" in ColorName: # ColorPrev, StylePrev
            # the current color is in -1, so Previous id == -2
            if "ColorPrev" == ColorName: 
                ColorName = __color_name_last_used[-2]
                colorCode = Colors[ColorName]
                __color_name_last_used.append(ColorName)
            if "StylePrev" == ColorName: 
                ColorName = __style_last_used[-2]
                colorCode = Colors[ColorName]
                __style_last_used.append(ColorName)
        else:

            if ColorName not in Colors:
                print("Color name error, not in table: ", ColorName)

            colorCode = Colors[ColorName]

            Styles = [  'Plain',
                        'Bold',
                        'Italic',
                        'Underline',
                        'Blink',
                        'Reverse',
                        'CursorHide',
                        'CursorShow', ]

            MaxElem = 20 # limit of memory usage
            if ColorName in Styles: 
                __style_last_used.append(ColorName)
                __style_last_used = __style_last_used[-MaxElem:]

            else: 
                __color_name_last_used.append(ColorName)
                __color_name_last_used = __color_name_last_used[-MaxElem:]

        # it doesn't work: return '\\e[' + colorCode + 'm'    
        ColorControl = colorCode + ColorBackground + 'm'    
        # print("ColorControl: " + ColorControl)
        return CSI + ColorControl


