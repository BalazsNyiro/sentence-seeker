# -*- coding: utf-8 -*-
import method_a_naive_01, text
import util

def user_interface_start(Prg, Args):
    if Args.gui == "cli":
        print("Exit: press enter, with empty wanted word")
        # neverending cycle :-)
        while True:
            Wanted = input("wanted: ").strip()
            if not Wanted:
                print(color_reset())
                break
            WordsWanted, MatchNums__ResultInfo = method_a_naive_01.seek(Prg, Wanted.lower() )
            result_all_display(Prg, MatchNums__ResultInfo)
        #########################################


def result_one_display(Prg, Result):
    Source = Result["Source"]
    LineNum = Result["LineNum"]
    WordsDetected = Result["WordsDetected"]
    WordsDetectedNum = len(WordsDetected)
    # print(Result)

    Sentence = Prg["DocumentObjectsLoaded"][Source]["Sentences"][LineNum]
    LineResultColored = text.word_highlight(WordsDetected, Sentence, HighlightBefore=color("Yellow"), HighlightAfter=color_reset())
    print(f"[{WordsDetectedNum}] {LineResultColored}")


def results_sort_by_sentence_length(Prg, Results):
    ResultsSorted = []

    GroupsByLen = dict()
    for Result in Results:
        Source = Result["Source"]
        LineNum = Result["LineNum"]
        Sentence = Prg["DocumentObjectsLoaded"][Source]["Sentences"][LineNum].strip()
        SentenceLen = len(Sentence)
        util.dict_key_insert_if_necessary(GroupsByLen, SentenceLen, list())
        GroupsByLen[SentenceLen].append(Result)

    LenKeys = list(GroupsByLen.keys())
    LenKeys.sort()
    for Key in LenKeys:
        # TODO: first where the words are in the same clause
        # TODO: where words are in same order?
        ResultsSorted.extend(GroupsByLen[Key])

    return ResultsSorted

def result_all_display(Prg, MatchNums__ResultsInfo, LimitDisplayed=6):
    MatchNums__Descending = list(MatchNums__ResultsInfo.keys())
    MatchNums__Descending.sort(reverse=True)

    DisplayedCounter = 0

    for MatchNum in MatchNums__Descending:
        print("\n===> MatchNum: ", MatchNum)
        Results = MatchNums__ResultsInfo[MatchNum]
        # print("#### Results ####", Results)
        # print("====", f"{color('Green')}{FileBaseName}{color_reset()}")

        for Result in results_sort_by_sentence_length(Prg, Results):
            DisplayedCounter += 1
            if DisplayedCounter <= LimitDisplayed:
                result_one_display(Prg, Result)
            else:
                return


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
def color_reset():
    return color("Plain")+color("Default")

CSI = '\033[' # echo -e "\x1b[93;41m"  # example  \x1b is \033 in python


__color_name_last_used=["Default"]
__style_last_used=["Plain"]
# cname lehet csak szam, 0-255 kozotti. 
# lehet szoveg, akkor a fenti tablabol veszi a kodokat.
def color(ColorName, CnameBackground=""):
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


