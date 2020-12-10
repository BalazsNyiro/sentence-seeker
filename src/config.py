# -*- coding: utf-8 -*-
import os, platform, util, time, util_json_obj
from shlex import quote
from pathlib import Path
import socket
from sys import platform

from html.parser import HTMLParser

def prg_config_create(TestExecution=False, DirWorkFromUserHome="", DirPrgExecRoot="", Os="", PrintForDeveloper=False):

    if not Os: # "Linux", "Windows" "Darwin"

        # debugger dies at this call
        #Os = platform.system()
        if "linux" in platform:
            Os = "Linux"
        elif platform == "darwin":
            Os = "Darwin"
        elif platform == "win32":
            Os = "Windows"

    if not DirPrgExecRoot:
        PathConfigModule = os.path.realpath(__file__)
        DirSrc = os.path.dirname(PathConfigModule)
        DirPrgExecRoot = os.path.realpath(os.path.join(DirSrc, ".."))

    if not DirWorkFromUserHome:
        DirWorkFromUserHome = util_json_obj.config_get("DirWorkFromUserHome", DirPrgExecRoot)

    DirWorkAbsPath = os.path.join(util.dir_user_home(), DirWorkFromUserHome)

    if not os.path.isdir(DirWorkAbsPath):
        # debugger dies at Path(...) lines so I guard it with if
        Path(DirWorkAbsPath).mkdir(parents=True, exist_ok=True)

    DirLog = os.path.join(DirWorkAbsPath, "log")
    if not os.path.isdir(DirLog):
        # debugger dies at Path(...) lines so I guard it with if
        Path(DirLog).mkdir(parents=True, exist_ok=True)
    print(f"== sentente seeker work path: {DirWorkAbsPath}")

    Time = int(time.time())
    FileLog = f"log_{Time}"
    DirDocuments = os.path.join(DirWorkAbsPath, "documents")

    if TestExecution:
        DirDocuments = os.path.join(DirPrgExecRoot, "test_files", "documents_user_dir_simulator")

    if not os.path.isdir(DirDocuments):
        # debugger dies at Path(...) lines so I guard it with if
        Path(DirDocuments).mkdir(parents=True, exist_ok=True)

    # we can use Prg as class, too - but the new code doesn't acceptable for me
    # Prg.Os would be the result but it's ugly in IDEA
    # class Dict(dict):
    #     def join(self, KeyInPrg, OtherVal):
    #         return os.path.join(self[KeyInPrg], OtherVal)

    # Prg = Dict({"Key":1}) works, too

    DocumentsSourceWebpagesFileName = os.path.join(DirDocuments, "documents_source_webpages.json")

    DefaultDocDb = '{"docs":{}, "source_names":{"gutenberg": "Project Gutenberg", "wikipedia": "Wikipedia"}}'
    util.file_create_if_necessary({}, DocumentsSourceWebpagesFileName, ContentDefault=DefaultDocDb, LogCreate=False)
    _Status, JsonObjReply = util_json_obj.obj_from_file(DocumentsSourceWebpagesFileName)
    DocumentsSourceWebpages = JsonObjReply["docs"]

    Prg = {
            "SettingsSaved": {
                "Ui":{
                    "CommandsExit": [":q", ":quit", ":exit"],
                    "DisplaySourceFileNameBelowSentences": True,
                    "DisplaySourceUrlBelowSentences": True,
                    "DirDocDisplay": True,
                    "LimitDisplayedSentences": 100,
                    "Console": {"NewlineBetweenSentences": False,
                                "BatteryInfoShow": True,
                                "ColorBattery": "Red",
                                "ColorUserInfo": "Blue",
                                "ColorUserInfoHigh": "Cyan",

                                "ColorRowOddOnly": False, # if True, no switch color at Even rows
                                "ColorRowOdd": "Default",
                                "ColorRowEven": "Green",

                                "ColorRowNum": "Red",
                                "ColorWanted": "Cyan",
                                "ColorWordDetected": "Yellow",
                                }
                },
                "DefaultWikiTextPackageUsage": "Y"
            },
            "ChangeVirtualConsoleCmd": "chvt",
            "TooManyTokenLimit": 300, # don't explain above this level
            "Cache": dict(),
            "Os": Os,
            "OsIsLinux": Os == "Linux",
            "OsIsWindows": Os == "Windows",
            "OsIsDarwin": Os == "Darwin",
            "OsIsUnixBased": Os == "Darwin" or Os == "Linux",

            "DirPrgRoot": DirPrgExecRoot, # parent dir of program, where sentence-seeker.py exists
            "DirWork": DirWorkAbsPath,
            "DirDocuments": DirDocuments,
            "DirTextSamples": os.path.join(DirPrgExecRoot, "text_samples"),
            "DirTestFiles": os.path.join(DirPrgExecRoot, "test_files"),
            "DirLog": DirLog,

            "DocumentsSourceWebpagesFileName": DocumentsSourceWebpagesFileName,
            "DocumentsSourceWebpagesFileContent": util.file_read_all({}, DocumentsSourceWebpagesFileName)[1], # for html_ui
            "DocumentsSourceWebpages": DocumentsSourceWebpages,

            "DocumentObjectsLoaded": dict(),
            "DocumentObjectsLoadedWordsCounterGlobal": dict(),

            "SubSentenceMultiplier": 100,  # "10001ww"  the last 2 digits shows the num of subsentence, ww is word positions
            "WordPositionMultiplier": 100,

            "FileLog": os.path.join(DirLog, FileLog),
            "TestResults": [],
            "TestExecution": TestExecution,
            "PrintForDeveloper": PrintForDeveloper,
            "ConverterPdfToText": converter_pdf_to_text(Os),
            "ConverterHtmlToText": converter_html_to_txt,

            "Statistics": {
                "ColorsConsoleUsedForeGround": set(),
                "Memory":[]
            },
            "Ui": "tkinter",
            "UiRootObj": None,
            "UiWindowGeometry": "800x600",
            "UiThemes": {
                "ThemeNameActual": "SunSet",
                "SunSet": {
                    "QueryWordEntry": "Helvetica 22 bold",
                    # https://www.schemecolor.com/collection-of-beautiful-pastel-color-schemes.php
                    # coolors.co
                    "Highlights":[
                                   "yellow",
                                   "#6BF178", # light green
                                   "orange",
                                   "pink",
                                   "#90F1EF", # light blue "cyan",
                                   "#85DE77", # light green
                                   "#FF756D"

                        , 'khaki1'
                        , 'gold'
                        ,'pale green'
                        , 'sandy brown'
                        , 'spring green'
                        , 'lawn green'
                        , 'SteelBlue2'
                        , "red",

                                      'snow'
                                    , 'gainsboro'
                                    , 'antique white'
                                    , 'navajo white'
                                    , 'lemon chiffon'
                                    , 'mint cream'

                                    , 'lavender'
                                    , 'lavender blush'
                                    , 'misty rose'

                                    , 'deep sky blue'
                                    , 'light sky blue'
                                    , 'steel blue'
                                    , 'light steel blue'
                                    , 'light blue'
                                    , 'powder blue'
                                    , 'pale turquoise'
                                    , 'dark turquoise'
                                    , 'medium turquoise'
                                    , 'turquoise'
                                    , 'cyan'
                                    , 'light cyan'
                                    , 'medium aquamarine'
                                    , 'aquamarine'
                                    , 'dark sea green'
                                    , 'medium sea green'
                                    , 'medium spring green'
                                    , 'green yellow'
                                    , 'lime green'
                                    , 'yellow green'
                                    , 'dark khaki'
                                    , 'khaki'
                                    , 'pale goldenrod'
                                    , 'light goldenrod yellow'
                                    , 'light yellow'
                                    , 'yellow'
                                    , 'light goldenrod'
                                    , 'goldenrod'
                                    , 'rosy brown'
                                    , 'indian red'
                                    , 'dark salmon'
                                    , 'salmon'
                                    , 'light salmon'
                                    , 'orange'
                                    , 'dark orange'
                                    , 'coral'
                                    , 'light coral'
                                    , 'tomato'
                                    , 'orange red'
                                    , 'hot pink'
                                    , 'deep pink'
                                    , 'pink'
                                    , 'light pink'
                                    , 'pale violet red'
                                    , 'medium orchid'
                                    , 'thistle'
                                    , 'snow2'
                                    , 'snow3'
                                    , 'SlateBlue1'
                                    , 'SteelBlue3'
                                    , 'DeepSkyBlue2'
                                    , 'DeepSkyBlue3'
                                    , 'SkyBlue1'
                                    , 'SkyBlue2'
                                    , 'SkyBlue3'
                                    , 'LightSkyBlue1'
                                    , 'LightSkyBlue2'
                                    , 'LightSkyBlue3'
                                    , 'SlateGray1'
                                    , 'aquamarine2'
                                    , 'DarkSeaGreen1'
                                    , 'DarkSeaGreen2'
                                    , 'DarkSeaGreen3'
                                    , 'SeaGreen1'
                                    , 'SeaGreen2'
                                    , 'SeaGreen3'
                                    , 'PaleGreen1'
                                    , 'PaleGreen2'
                                    , 'PaleGreen3'
                                    , 'SpringGreen2'
                                    , 'SpringGreen3'
                                    , 'green2'
                                    , 'green3'
                                    , 'chartreuse2'
                                    , 'chartreuse3'
                                    , 'OliveDrab1'
                                    , 'OliveDrab2'
                                    , 'DarkOliveGreen1'
                                    , 'DarkOliveGreen2'
                                    , 'DarkOliveGreen3'
                                    , 'khaki2'
                                    , 'khaki3'
                                    , 'LightGoldenrod1'
                                    , 'LightGoldenrod2'
                                    , 'LightGoldenrod3'
                                    , 'LightYellow2'
                                    , 'LightYellow3'
                                    , 'yellow2'
                                    , 'yellow3'
                                    , 'gold2'
                                    , 'gold3'
                                    , 'goldenrod1'
                                    , 'goldenrod2'
                                    , 'goldenrod3'
                                    , 'DarkGoldenrod1'
                                    , 'DarkGoldenrod2'
                                    , 'RosyBrown1'
                                    , 'RosyBrown2'
                                    , 'IndianRed1'
                                    , 'IndianRed2'
                                    , 'sienna1'
                                    , 'sienna2'
                                    , 'sienna3'
                                    , 'burlywood1'
                                    , 'burlywood2'
                                    , 'burlywood3'
                                    , 'wheat1'
                                    , 'wheat2'
                                    , 'wheat3'
                                    , 'tan1'
                                    , 'tan2'
                                    , 'chocolate1'
                                    , 'chocolate2'
                                    , 'chocolate3'
                                    , 'firebrick1'
                                    , 'firebrick2'
                                    , 'firebrick3'
                                    , 'brown1'
                                    , 'brown2'
                                    , 'brown3'
                                    , 'salmon1'
                                    , 'salmon2'
                                    , 'salmon3'
                                    , 'LightSalmon2'
                                    , 'LightSalmon3'
                                    , 'orange2'
                                    , 'orange3'
                                    , 'DarkOrange1'
                                    , 'DarkOrange2'
                                    , 'DarkOrange3'
                                    , 'coral1'
                                    , 'coral2'
                                    , 'coral3'
                                    , 'tomato2'
                                    , 'tomato3'
                                    , 'OrangeRed2'
                                    , 'OrangeRed3'
                                    , 'red2'
                                    , 'red3'
                                    , 'DeepPink2'
                                    , 'DeepPink3'
                                    , 'HotPink1'
                                    , 'HotPink2'
                                    , 'HotPink3'
                                    , 'pink1'
                                    , 'pink2'
                                    , 'pink3'
                                    , 'LightPink1'
                                    , 'LightPink2'
                                    , 'LightPink3'
                                    , 'PaleVioletRed1'
                                    , 'PaleVioletRed2'
                                    , 'PaleVioletRed3'
                                    , 'maroon1'
                                    , 'maroon2'
                                    , 'maroon3'
                                    , 'VioletRed1'
                                    , 'VioletRed2'
                                    , 'VioletRed3'
                                    , 'magenta2'
                                    , 'magenta3'
                                    , 'orchid1'
                                    , 'orchid2'
                                    , 'orchid3'
                                    , 'plum1'
                                    , 'plum2'
                                    , 'plum3'
                                    , 'MediumOrchid1'
                                    , 'MediumOrchid2'

                    ],
                    "SentencesWidth": 70,
                    "SentencesHeight": 30,

                    "FontTitle": ("Tempus Sans ITC", 12, "bold"),
                    "FontSentenceResult": ("Tempus Sans ITC", 12, "bold"),
                    "FontSentenceNormal": ("Tempus Sans ITC", 12, "normal"),
                    "FontUrl": ("Tempus Sans ITC", 12, "bold"),
                    "FontSource": ('Tempus Sans ITC', 9, 'normal'),
                    "BgWords": "#FFE2BC",
                    "BgAreaSentences": "#FFE2BC",
                    "FgAreaSentences": "#101010",
                    "FgUrl": "#35D0BA", # "blue"
                    "FgSource": "#D92027",
                    "FgSentence": "#7C3C21",   # https://colorhunt.co/palette/183389   browns
                    "FgSubSentenceResult": "#092532"
                }
            },
            "ServerHost": "data.sentence-seeker.net" if socket.gethostname() == "vps" else "localhost",
            "ServerPort": 8000,
            "Licenses": """Licenses: Books from Gutenberg.org are in Public Domain.\nThe Wikipedia articles are typically under 'Creative Commons Attribution-ShareAlike License', please always check the original source page.""",
            "QueryExamples": {"bird_or_cat": "looks AND like AND (bird OR cat)"},
            "UsageInfo": util.file_read_all_simple(os.path.join(DirPrgExecRoot, "README.md"))
    }

    SettingsSaved = util_json_obj.config_get("SettingsSaved", DirWorkAbsPath, DefaultVal=dict())
    util.dict_update_recursive(Prg["SettingsSaved"], SettingsSaved)

    # Save the
    util_json_obj.config_set(Prg, "SettingsSaved")
    return Prg

# Naive html text extractor.
# unfortunatelly it saves css data tags, too
# TODO: save only <p>, <h>, <div>, <ul>, <li> elems instead of all
class DocHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.Level_P = 0
        self.Level_Span = 0

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        if tag == "p":
            self.Level_P += 1
        if tag == "span":
            self.Level_Span += 1

    def handle_endtag(self, tag):
        if tag == "p":
            self.Level_P -= 1
        if tag == "span":
            self.Level_Span -= 1

    def handle_data(self, data):
        # self.data.append(data)
        if self.Level_P > 0:
            self.data.append(data)

        if self.Level_Span > 0:
            self.data.append(data)

    def handle_comment(self, data):
        #print("Comment  :", data)
        pass

    def handle_entityref(self, name):
        # c = chr(name2codepoint[name])
        # print("Named ent:", c)
        pass

    def handle_charref(self, name):
        # if name.startswith('x'):
        #     c = chr(int(name[1:], 16))
        # else:
        #     c = chr(int(name))
        # print("Num ent  :", c)
        pass

    def handle_decl(self, data):
        # print("Decl     :", data)
        pass

def converter_html_to_txt(Prg, PathInput, PathOutput):
    parser = DocHTMLParser()
    RetStatus, Src = util.file_read_all(Prg, PathInput)
    if not RetStatus: # error with reading
        print("READING ERROR: ", PathInput)
        return False
    parser.feed(Src)  # file_write: return with success/failure of writing
    # print("WRITE: ", PathOutput)
    # print("DATA", parser.data)
    return util.file_write(Prg, Fname=PathOutput, Content=parser.data)

# Tested
def converter_pdf_to_text(Os):
    ConverterDetected = False

    def pdf_to_text_fun(_Prg, _PathInput, _PathOutput):
        return False

    # pdfminer.six inserts unwanted (cid:XXX) and binary chars
    # into output so if it's possible I use pdftotext, if both are available

    Location = ""
    for Line in util.shell("pip3 show pdfminer.six -f").split("\n"):
        if "Location" in Line:
            print(Line)
            Location = Line.split()[1]

        if ".pyc" not in Line and "pdf2txt.py" in Line:
            PathRelative = Line.strip()
            PathPdfMinerSix = os.path.join(Location, PathRelative)
            Interpreter = "python3" if "python3" in PathPdfMinerSix else "python2"

            print(f"pdf converter detected: {Interpreter}, {PathPdfMinerSix}")
            # python2 Path/pdf2txt.py   test.pdf --outfile test.txt
            def PdfToTextFun(_Prg, PathInput, PathOutput): # shlex.quote
                util.shell(f"{Interpreter} {PathPdfMinerSix} {quote(PathInput)} --outfile {quote(PathOutput)}")
                return True

            ConverterDetected = True

    if True:
        PathPdfToText = util.shell("which pdftotext").strip()
        if "linux" in Os.lower() and "/pdftotext" in PathPdfToText:
            print(f"pdf converter detected: {PathPdfToText}")

            def pdf_to_text_fun(_Prg, PathInput, PathOutput):
                util.shell(f"{PathPdfToText} -nopgbrk {quote(PathInput)} {quote(PathOutput)}")
                return True

            ConverterDetected = True

    if not ConverterDetected:
        print("\n== There are more available pdf to text converters ==\n\n"
                "Win/Linux/Mac pdf to text converter - pdfminer.six:  \n"
                "    pip3 install pdfminer.six \n"
                "    https://github.com/pdfminer/pdfminer.six\n"
                "\n"
                "Linux/Mac: you can install poppler-utils,\n"
                "    apt install poppler-utils    (on Ubuntu Linux)"
              )

    return pdf_to_text_fun




# color names:
# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

TKINTER_ALL_COLORNAMES = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']


