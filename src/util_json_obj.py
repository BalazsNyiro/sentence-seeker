# -*- coding: utf-8 -*-
import os, util, json

############ JSON #############################

# Tested
def obj_from_file(JsonFileName):
    with open(JsonFileName) as f:
        return json.load(f)

# Tested
def obj_to_file(JsonFileName, Data):
    with open(JsonFileName, 'w') as OutFile:
        json.dump(Data, OutFile, sort_keys=True, indent=4)

_DocsSampleInfo = None
def doc_db_update(Prg, File, DocObj=None):
    BaseNameOrig = os.path.basename(File)
    global _DocsSampleInfo
    if not _DocsSampleInfo: # read only once, save it into global var
        _DocsSampleInfo = obj_from_file(os.path.join(Prg["DirTextSamples"], "document_samples.json"))
    DocDb = obj_from_file(Prg["FileDocumentsDb"])

    if not DocObj:
        if BaseNameOrig in _DocsSampleInfo["docs"]:
            DocObj = _DocsSampleInfo["docs"][BaseNameOrig]

    if DocObj:
        DocDb["docs"][BaseNameOrig] = DocObj
        obj_to_file(Prg["FileDocumentsDb"], DocDb)

# Used in tests
# read wanted key from config file
def config_get(Key, DefaultVal, DirPrgRoot,
               DirConfigFileParent=None,
               FileConfigBaseName=".sentence-seeker.config"):

    if not DirConfigFileParent:
        DirConfigFileParent = util.dir_user_home()

    FileConfigAbsPath = os.path.join(DirConfigFileParent, FileConfigBaseName)

    if not os.path.isfile(FileConfigAbsPath):
        print(f"create new config file from default: {FileConfigAbsPath}")
        util.file_copy(os.path.join(DirPrgRoot, FileConfigBaseName), FileConfigAbsPath)
    else:
        print(f"config file exists: {FileConfigAbsPath}")

    Json = obj_from_file(FileConfigAbsPath)
    if Key in Json:
        return Json[Key]
    return DefaultVal


