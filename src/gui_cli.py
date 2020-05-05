# -*- coding: utf-8 -*-
import method_a_naive_01, text
import util

def user_interface_start(Prg, Args):
    if Args.ui == "cli":
        user_welcome_message(Prg, Args.ui)
        # neverending cycle :-)
        while True:
            Wanted = input("wanted: ").strip()
            if not Wanted:
                print(color_reset(Prg))
                break
            WordsWanted, MatchNums__ResultInfo = method_a_naive_01.seek(Prg, Wanted.lower() )
            sentence_result_all_display(Prg, MatchNums__ResultInfo)
        #########################################

def user_welcome_message(Prg, UserInterface):
    if UserInterface == "cli":
        print("test word: elephant")
        print("Exit: press enter, with empty wanted word")
        print(f"{color(Prg, 'Yellow')}Docs dir: {Prg['DirDocuments']}{color_reset(Prg)}")

def sentence_result_one_display(Prg, Result):
    Source = Result["Source"]
    LineNum = Result["LineNum"]
    WordsDetected = Result["WordsDetected"]
    WordsDetectedNum = len(WordsDetected)
    # print(Result)

    Sentence = Prg["DocumentObjectsLoaded"][Source]["Sentences"][LineNum]
    Sentence = Sentence.strip() # remove possible newline at end
    LineResultColored = text.word_highlight(WordsDetected, Sentence, HighlightBefore=color(Prg, "Yellow"), HighlightAfter=color_reset(Prg))
    print(f"{color(Prg, 'Bright Green')}[{WordsDetectedNum}]{color_reset(Prg)} {LineResultColored}\n{color(Prg, 'Bright Red')}{Source}{color_reset(Prg)}\n")

def sentence_result_all_display(Prg, SentenceObjects, LimitDisplayed=6):
    for DisplayedCounter, SentenceObj in enumerate(SentenceObjects, start=1):
        sentence_result_one_display(Prg, SentenceObj)
        if DisplayedCounter >= LimitDisplayed:
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
# cname lehet csak szam, 0-255 kozotti. 
# lehet szoveg, akkor a fenti tablabol veszi a kodokat.
def color(Prg, ColorName, CnameBackground=""):

    if Prg["Os"] == "Windows": return ""
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


