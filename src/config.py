# -*- coding: utf-8 -*-
import os, platform, user, util, time, util_json_obj
from shlex import quote
from pathlib import Path

from html.parser import HTMLParser
from html.entities import name2codepoint

def PrgConfigCreate(DirWorkFromUserHome="", DirPrgRoot="", Os="", PrintForDeveloper=False):

    # print("__file__", __file__, sys.argv)
    if not Os: # "Linux", "Windows" "Darwin"
        Os = platform.system()

    if not DirPrgRoot:
        PathConfigModule = os.path.realpath(__file__)
        DirSrc = os.path.dirname(PathConfigModule)
        DirPrgRoot = os.path.realpath(os.path.join(DirSrc, ".."))

    if not DirWorkFromUserHome:
        DirWorkFromUserHome = util_json_obj.config_get("DirWorkFromUserHome", ".sentence-seeker", DirPrgRoot)

    DirWorkAbsPath = os.path.join(user.dir_home(), DirWorkFromUserHome)
    Path(DirWorkAbsPath).mkdir(parents=True, exist_ok=True)

    DirLog = os.path.join(DirWorkAbsPath, "log")
    Path(DirLog).mkdir(parents=True, exist_ok=True)
    print(f"== sentente seeker work path: {DirWorkAbsPath}")

    Time = int(time.time())
    FileLog = f"log_{Time}"
    DirDocuments = os.path.join(DirWorkAbsPath, "documents")
    Path(DirDocuments).mkdir(parents=True, exist_ok=True)

    # we can use Prg as class, too - but the new code doesn't acceptable for me
    # Prg.Os would be the result but it's ugly in IDEA
    # class Dict(dict):
    #     def join(self, KeyInPrg, OtherVal):
    #         return os.path.join(self[KeyInPrg], OtherVal)

    # Prg = Dict({"Key":1}) works, too

    FileDocumentsDb = os.path.join(DirDocuments, "documents.json")

    PathSamples = os.path.join(DirPrgRoot, "text_samples", "document_samples.json")
    DocumentsDbDefault = util.file_read_all_simple(PathSamples)
    util.file_create_if_necessary({}, FileDocumentsDb, ContentDefault=DocumentsDbDefault, LogCreate=False)

    DocumentsDb = dict()
    for Doc in util_json_obj.obj_from_file(FileDocumentsDb)["docs"]:
        FileName = Doc["file_name"]
        if FileName[-3:] == ".gz":
            FileName = FileName[:-3]
        DocumentsDb[FileName] = Doc

    Prg = { "Os": Os,
            "DirPrgRoot": DirPrgRoot, # parent dir of program, where sentence-seeker.py exists
            "DirWork": DirWorkAbsPath,
            "DirDocuments": DirDocuments,
            "DirTextSamples": os.path.join(DirPrgRoot, "text_samples"),
            "DirTestFiles": os.path.join(DirPrgRoot, "test_files"),
            "DirsDeleteAfterRun": list(),
            "FilesDeleteAfterRun": list(),
            "DirLog": DirLog,

            "FileDocumentsDb": os.path.join(DirDocuments, "documents.json"),
            "DocumentsDb": DocumentsDb,

            "FileLog": os.path.join(DirLog, FileLog),
            "TestResults": [],
            "TestExecution": False,
            "PrintForDeveloper": PrintForDeveloper,
            "PdfToTextConvert": fun_pdf_to_text_converter(Os),
            "HtmlToTextConvert": fun_html_to_text_converter,
            "DocumentObjectsLoaded": dict(),
            "Statistics": [],

    }

    return Prg

# Naive html text extractor.
# unfortunatelly it saves css data tags, too
# TODO: save only <p>, <h>, <div>, <ul>, <li> elems instead of all
class DocHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
        self.Level_P = 0

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        if tag == "p":
            self.Level_P += 1

    def handle_endtag(self, tag):
        if tag == "p":
            self.Level_P -= 1

    def handle_data(self, data):
        # self.data.append(data)
        if self.Level_P > 0:
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

def fun_html_to_text_converter(Prg, PathInput, PathOutput):
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
def fun_pdf_to_text_converter(Os):
    ConverterDetected = False

    def PdfToTextFun(_Prg, _PathInput, _PathOutput):
        return False

    # pdfminer.six inserts unwanted (cid:XXX) and binary chars
    # into output so if it's possible I use pdftotext, if both are available

    Location = ""
    for Line in util.shell("pip show pdfminer.six -f").split("\n"):
        if "Location" in Line:
            print(Line)
            Location = Line.split()[1]

        if ".pyc" not in Line and "pdf2txt.py" in Line:
            PathRelative = Line.strip()
            PathPdfMinerSix = os.path.join(Location, PathRelative)
            Interpreter = "python3" if "python3" in PathPdfMinerSix else "python2"

            print(f"pdf converter detected: {Interpreter}, {PathPdfMinerSix}")
            # python2 Path/pdf2txt.py   test.pdf --outfile test.txt
            def PdfToTextFun(_Prg, PathInput, PathOutput):
                util.shell(f"{Interpreter} {PathPdfMinerSix} {shlex.quote(PathInput)} --outfile {shlex.quote(PathOutput)}")
                return True

            ConverterDetected = True

    if True:
        PathPdfToText = util.shell("which pdftotext").strip()
        if "linux" in Os.lower() and "/pdftotext" in PathPdfToText:
            print(f"pdf converter detected: {PathPdfToText}")

            def PdfToTextFun(_Prg, PathInput, PathOutput):
                util.shell(f"{PathPdfToText} -nopgbrk {quote(PathInput)} {quote(PathOutput)}")
                return True

            ConverterDetected = True

    if not ConverterDetected:
        print("\n== There are more available pdf to text converters ==\n\n"
                "Win/Linux/Mac pdf to text converter - pdfminer.six:  \n"
                "    pip install pdfminer.six \n"
                "    https://github.com/pdfminer/pdfminer.six\n"
                "\n"
                "Linux/Mac: you can install poppler-utils,\n"
                "    apt install poppler-utils    (on Ubuntu Linux)"
              )

    return PdfToTextFun
