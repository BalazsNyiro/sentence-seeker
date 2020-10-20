# -*- coding: utf-8 -*-
import seeker_logic, text, util_ui

def seek_and_display(Prg, Wanted):
    TokenProcessExplainSumma, WordsMaybeDetected, MatchNums__ResultInfo, ResultsTotalNum = seeker_logic.seek(Prg, Wanted)
    print(util_ui.token_explain_summa_to_text(TokenProcessExplainSumma))
    sentence_result_all_display(Prg, MatchNums__ResultInfo, WordsMaybeDetected)
    print(f"Results Total: {ResultsTotalNum}")

def user_interface_start(Prg, Ui):
    user_welcome_message(Prg, Ui)
    # neverending cycle :-)
    while True:
        Wanted = input("wanted: ").strip()
        if not Wanted:
            print(color_reset(Prg))
            break
        seek_and_display(Prg, Wanted)
    #########################################

def user_welcome_message(Prg, UserInterface):
    if UserInterface == "console":
        print(Prg["Licenses"])
        print("interesting search: looks, like, bird")
        print("interesting search: elephant")

        print("Exit: press enter, with empty wanted word")
        print(f"{color(Prg, 'Yellow')}Docs dir: {Prg['DirDocuments']}{color_reset(Prg)}")

def sentence_result_one_display(Prg, Result, WordsMaybeDetected ):

    Url, Sentence, Source = util_ui.sentence_get_from_result(Prg, Result, ReturnType="separated_subsentences")

    LineResultColored = Sentence["subsentences_before"] + text.word_highlight(WordsMaybeDetected, Sentence["subsentence_result"], HighlightBefore=color(Prg, "Yellow"), HighlightAfter=color_reset(Prg)) + Sentence["subsentences_after"]
    print(f"{LineResultColored}\n{color(Prg, 'Bright Red')}{Source}{color_reset(Prg)}")
    print(f"{color(Prg, 'Bright Red')}{Url}{color_reset(Prg)}\n")

def sentence_result_all_display(Prg, SentenceObjects, WordsMaybeDetected):
    for DisplayedCounter, SentenceObj in enumerate(SentenceObjects, start=1):
        sentence_result_one_display(Prg, SentenceObj, WordsMaybeDetected)
        if DisplayedCounter >= Prg["LimitDisplayedSampleSentences"]:
            break

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

    if Prg["Os"] == "Windows": return ""
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


