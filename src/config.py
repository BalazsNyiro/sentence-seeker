# -*- coding: utf-8 -*-
import os, platform, user, util, time, util_json_obj

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


