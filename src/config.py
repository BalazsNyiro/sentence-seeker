# -*- coding: utf-8 -*-
import os, platform, user, util, time, util_json_obj
from shlex import quote

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
    DirLog = os.path.join(DirWorkAbsPath, "log")
    print(f"== sentente seeker work path: {DirWorkAbsPath}")

    Time = int(time.time())
    FileLog = f"log_{Time}"
    DirDocuments = os.path.join(DirWorkAbsPath, "documents")


    # we can use Prg as class, too - but the new code doesn't acceptable for me
    # Prg.Os would be the result but it's ugly in IDEA
    # class Dict(dict):
    #     def join(self, KeyInPrg, OtherVal):
    #         return os.path.join(self[KeyInPrg], OtherVal)

    # Prg = Dict({"Key":1}) works, too


    Prg = { "Os": Os,
            "DirPrgRoot": DirPrgRoot, # parent dir of program, where sentence-seeker.py exists
            "DirWork": DirWorkAbsPath,
            "DirDocuments": DirDocuments,
            "DirTextSamples": os.path.join(DirPrgRoot, "text_samples"),
            "DirsDeleteAfterRun": list(),
            "FilesDeleteAfterRun": list(),
            "DirLog": DirLog,
            "FileDocumentsDb": os.path.join(DirDocuments, "documents.json"),
            "FileLog": os.path.join(DirLog, FileLog),
            "TestResults": [],
            "TestExecution": False,
            "PrintForDeveloper": PrintForDeveloper,
            "PdfToTextConvert": fun_pdf_to_text_converter(Os),
            "DocumentObjectsLoaded": dict(),
            "Statistics": []
    }

    return Prg

def DirsFilesConfigCreate(Prg):
    for Dir in [Prg["DirWork"], Prg["DirLog"]]:
        # if these dirs don't exist, I can't create log in the proper file
        util.dir_create_if_necessary(Prg, Dir, LogCreate=False)

    # here the log dir exists, so I can save any error message :-)
    util.dir_create_if_necessary(Prg, Prg["DirDocuments"])

    Default = "{}"
    util.file_create_if_necessary(Prg, Prg["FileDocumentsDb"], ContentDefault=Default)

def fun_pdf_to_text_converter(Os):
    PdfToTextFun = lambda _PathSource, _PathOutput: ""
    Detected = False

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
            PdfToTextFun = lambda PathSource, PathOutput: util.shell(f"{Interpreter} {PathPdfMinerSix} {shlex.quote(PathSource)} --outfile {shlex.quote(PathOutput)}")
            Detected = True

    if True:
        PathPrgConv = util.shell("which pdftotext").strip()
        if "linux" in Os.lower() and "/pdftotext" in PathPrgConv:
            print(f"pdf converter detected: {PathPrgConv}")
            PdfToTextFun = lambda PathIn, PathOut: util.shell(f"{PathPrgConv} -nopgbrk {quote(PathIn)} {quote(PathOut)}")
            Detected = True

    if not Detected:
        print("\n== There are more available pdf to text converters ==\n\n"
                "Win/Linux/Mac pdf to text converter - pdfminer.six:  \n"
                "    pip install pdfminer.six \n"
                "    https://github.com/pdfminer/pdfminer.six\n"
                "\n"
                "Linux/Mac: you can install poppler-utils,\n"
                "    apt install poppler-utils    (on Ubuntu Linux)"
              )

    return PdfToTextFun
