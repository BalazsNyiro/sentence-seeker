# -*- coding: utf-8 -*-
import os, platform, user, sys, util, time

def PrgConfigCreate(DirWorkFromUserHome=".sentence-seeker", DirPrgRoot="", Os=""):
    print("__file__", __file__, sys.argv)
    if not DirPrgRoot:
        PathConfigModule = os.path.realpath(__file__)
        DirSrc = os.path.dirname(PathConfigModule)
        DirPrgRoot = os.path.realpath(os.path.join(DirSrc, ".."))

    if not Os: # "Linux", "Windows" "Darwin"
        Os = platform.system()

    DirWorkAbsPath = os.path.join(user.dir_home(), DirWorkFromUserHome)
    DirLog = os.path.join(DirWorkAbsPath, "log")

    Time = int(time.time())
    FileLog = f"log_{Time}"
    DirDocuments = os.path.join(DirWorkAbsPath, "documents")

    Prg = { "Os": Os,
            "DirPrgRoot":  DirPrgRoot, # parent dir of program, where sentence-seeker.py exists
            "DirWork": DirWorkAbsPath,
            "DirDocuments": DirDocuments,
            "DirsDeleteAfterRun": list(),
            "FilesDeleteAfterRun": list(),
            "DirLog": DirLog,
            "FileDocumentsDb": os.path.join(DirDocuments, "docs.json"),
            "FileLog": os.path.join(DirLog, FileLog),
            "TestResults": [],
            "TestExecution": False
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


