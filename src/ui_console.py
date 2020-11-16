# -*- coding: utf-8 -*-
import seeker_logic, text, util_ui
import time

def seek_and_display(Prg, Wanted):
    TimeLogicStart = time.time()
    TokenProcessExplainSumma, WordsMaybeDetected, MatchNums__ResultInfo, ResultsTotalNum = seeker_logic.seek(Prg, Wanted)
    TimeLogicUsed = time.time() - TimeLogicStart

    sentence_result_all_display(Prg, MatchNums__ResultInfo, WordsMaybeDetected)
    # print(f"Results Total: {ResultsTotalNum}")
    # print("Time logic: ", TimeLogicUsed)

def user_interface_start(Prg, Ui, QueryAsCmdlineParam=""):
    if Prg["OsIsUnixBased"]: # On Linux and I hope on Mac, we can use history in console with readline module
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

def sentence_result_one(Prg, Result, WordsMaybeDetected, DisplayedCounter):
    ColorReset = color_reset(Prg)

    Url, Sentence, Source = util_ui.sentence_get_from_result(Prg, Result, ReturnType="separated_subsentences")

    if DisplayedCounter % 2 == 0:
        ColorRow = color(Prg, "Default") # the basic color of the row - it's switched line by line
    else:
        ColorRow = color(Prg, "Green")
    RowNum = f"{DisplayedCounter} "

    LineResultColored = ColorRow + RowNum +\
                        Sentence["subsentences_before"] + \
                        text.word_highlight(WordsMaybeDetected,
                                            Sentence["subsentence_result"],
                                            HighlightBefore=color(Prg, "Yellow"),
                                            HighlightAfter=ColorReset,
                                            ColorRow=ColorRow,
                                            ColorRowEnd=ColorReset) \
                        + Sentence["subsentences_after"] + \
                        ColorReset + \
                        "\n"

    LineResultNotColored = Sentence["subsentences_before"] + RowNum +\
                           Sentence["subsentence_result"] + \
                           Sentence["subsentences_after"] + \
                           "\n"

    if Prg["SettingsSaved"]["Ui"]["DisplaySourceFileNameBelowSentences"]:
        LineResultColored += f"{color(Prg, 'Bright Red')}{Source}{ColorReset}\n"
        LineResultNotColored += f"{Source}\n"

    if Prg["SettingsSaved"]["Ui"]["DisplaySourceUrlBelowSentences"]:
        LineResultColored += f"{color(Prg, 'Bright Red')}{Url}{ColorReset}\n"
        LineResultNotColored += f"{Url}\n"

    return LineResultColored, LineResultNotColored

def sentence_result_all_display(Prg, SentenceObjects, WordsMaybeDetected):
    ScreenWidth, ScreenHeight = util_ui.get_screen_size()
    SentencesColored = []
    SentencesNotColored = []

    for DisplayedCounter, SentenceObj in enumerate(SentenceObjects, start=1):
        LineResultColored, LineResultNotColored = sentence_result_one(Prg, SentenceObj, WordsMaybeDetected, DisplayedCounter)
        SentencesColored.append(LineResultColored)
        SentencesNotColored.append(LineResultNotColored)

    TextsPerScreen = util_ui.text_split_at_screensize(SentencesColored, SentencesNotColored, ScreenWidth, ScreenHeight-3)

    # TODO: loop all, based on keypress
    Id = 0
    IdLast = len(TextsPerScreen)-1
    Msg = "[p]rev [n]ext [q]uery again."

    # 13: Enter
    # 127: backspace
    NextChars = "n jBC"+chr(13) # B = arrowDown, C=arrowRight buttons, fun return with these chars if I press arrow buttons
    PrevChars = "pkAD" + chr(127) # A: arrowUp, D: arrowLeft
    if TextsPerScreen: # if you use special commands, :help for example, we don't have any results
        while True:
            print(TextsPerScreen[Id])
            UserReply = util_ui.press_key_in_console(Msg)
            if UserReply in PrevChars:
                if Id > 0:
                    Id -= 1
            if UserReply in NextChars:
                if Id < IdLast-1:
                    Id += 1
            if UserReply == "q":
                break

    #    if DisplayedCounter >= Prg["LimitDisplayedSampleSentences"]:
    #        break

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

    # If os == windows, return with empty string, because
    # we have to test colors in Windows terminal

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


