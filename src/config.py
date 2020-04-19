# -*- coding: utf-8 -*-
import os, platform, user, sys, util

def PrgConfigCreate(DirWorkFromUserHome=".sentence-seeker", DirPrgRoot="", Os=""):
    print("__file__", __file__, sys.argv)
    if not DirPrgRoot:
        PathConfigModule = os.path.realpath(__file__)
        DirSrc = os.path.dirname(PathConfigModule)
        DirPrgRoot = os.path.realpath(os.path.join(DirSrc, ".."))

    if not Os: # "Linux", "Windows" "Darwin"
        Os = platform.system()

    DirWorkAbsPath = os.path.join(user.dir_home(), DirWorkFromUserHome)

    Prg = {
        "Os": Os,
        "DirPrgRoot":  DirPrgRoot, # parent dir of program, where sentence-seeker.py exists
        "DirWork": DirWorkAbsPath,
        "DirTmp": os.path.join(DirWorkAbsPath, "tmp"),
        "DirsDeleteAfterRun": list(),
        "FilesDeleteAfterRun": list(),
        "DirLog": os.path.join(DirWorkAbsPath, "log")
    }

    for Dir in [Prg["DirWork"], Prg["DirLog"] ]:
        # if these dirs don't exist, I can't create log in the proper file
        util.dir_create_if_necessary(Prg, Dir, LogCreate=False)

    # here the log dir exists, so I can save any error message :-)
    util.dir_create_if_necessary(Prg, Prg["DirTmp"])

    return Prg