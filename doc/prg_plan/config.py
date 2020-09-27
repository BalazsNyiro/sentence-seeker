import util, util_json_obj
import os, platform
from pathlib import Path
from html.parser import HTMLParser
import socket


def PrgConfigCreate(Args, DirWorkFromUserHome="", DirPrgRoot="", Os="", PrintForDeveloper=False):

    if not DirPrgRoot:
        PathConfigModule = os.path.realpath(__file__)
        DirSrc = os.path.dirname(PathConfigModule)
        DirPrgRoot = os.path.realpath(os.path.join(DirSrc, ".."))

    Os = platform.system()

    DirWorkAbsPath = os.path.join(util.dir_user_home(), DirWorkFromUserHome)
    Path(DirWorkAbsPath).mkdir(parents=True, exist_ok=True)

    DirLog = os.path.join(DirWorkAbsPath, "log")
    Path(DirLog).mkdir(parents=True, exist_ok=True)
    print(f"== sentente seeker work path: {DirWorkAbsPath}")

    FileLog = f"log_prg_plan"
    DirDocuments = os.path.join(DirWorkAbsPath, "documents")
    FileDocumentsDb = os.path.join(DirDocuments, "documents.json")
    DefaultDocDb = '{"docs":{}, "source_names":{"gutenberg": "Project Gutenberg", "wikipedia": "Wikipedia"}}'
    util.file_create_if_necessary({}, FileDocumentsDb, ContentDefault=DefaultDocDb)
    _Status, JsonObjReply = util_json_obj.obj_from_file(FileDocumentsDb)
    DocumentsDb = JsonObjReply["docs"]

    Prg = { "Os": Os,
            "DirPrgRoot": DirPrgRoot, # parent dir of program, where sentence-seeker.py exists
            "DirWork": DirWorkAbsPath,
            "DirDocuments": DirDocuments,
            "DirTextSamples": os.path.join(DirPrgRoot, "text_samples"),
            "DirTestFiles": os.path.join(DirPrgRoot, "test_files"),
            "DirsDeleteAfterRun": list(),
            "FilesDeleteAfterRun": list(),
            "DirLog": DirLog,

            "FileDocumentsDb": FileDocumentsDb,
            "FileDocumentsDbContent": util.file_read_all({}, FileDocumentsDb)[1],
            "DocumentsDb": DocumentsDb,

            "FileLog": os.path.join(DirLog, FileLog),
            "TestResults": [],
            "TestExecution": Args.test,
            "PrintForDeveloper": PrintForDeveloper,
            "PdfToTextConvert": text_from_pdf(Os),
            "HtmlToTextConvert": text_from_html,
            "DocumentObjectsLoaded": dict(),
            "DocumentObjectsLoadedWordsCounterGlobal": dict(),
            "Statistics": [],
            "LimitDisplayedSampleSentences": 20,

            "UiThemes": {
                "ThemeNameActual": "SunSet",
                "SunSet": {
                    # https://www.schemecolor.com/collection-of-beautiful-pastel-color-schemes.php
                    # coolors.co
                    "Highlights": [
                        "yellow",
                        "#6BF178", # light green
                        "orange",
                        "pink",
                        "#90F1EF", # light blue "cyan",
                        "#85DE77", # light green
                        "#FF756D",
                        "black",
                        "white",
                        "gray",
                        "red",
                        "green",
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
            "WordSetsFounded": dict(),
            "ServerHost": "data.sentence-seeker.net" if socket.gethostname() == "vps" else "localhost",
            "ServerPort": 8000,
            "Licenses": """Licenses: Books from Gutenberg.org are in Public Domain.\nThe Wikipedia articles are typically under 'Creative Commons Attribution-ShareAlike License', please always check the original source page.""",
            "QueryExamples": {"bird_or_cat": "looks AND like AND (bird OR cat)"},
            "UsageInfo": "The program can collect sentences with given words.\n"
                         " - use lowercase words that you want\n"
                         " - use uppercase logical keywords: AND  OR\n\n"
                         " - you can use () to group words\n"
                         " - if you want, you can separate words with space/comma, too\n"
                         "   example:  eat AND (apple OR banana)\n"

                         " - space and comma means AND logically\n"
                         "   example:  egypt, russia, china\n\n"
                         "   in this case the program will find \n"
                         "   Russia, RUSSIA and russia too,\n"
                         "   but in input please use lower-case words",
            "MessagesForUser": []
            }
    return Prg

class DocHTMLParser(HTMLParser):
    def __init__(self):
        pass

def text_from_pdf(Os):
    parser = DocHTMLParser()
    return

def text_from_html(Prg, PathInput, PathOutput):
    return
