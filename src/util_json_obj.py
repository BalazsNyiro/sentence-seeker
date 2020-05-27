# -*- coding: utf-8 -*-
import os, user, util, json

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
def doc_db_update(Prg, BaseNameOrig):
    global _DocsSampleInfo
    if not _DocsSampleInfo: # read only once, save it into global var
        _DocsSampleInfo = obj_from_file(os.path.join(Prg["DirTextSamples"], "document_samples.json"))
    DocDb = obj_from_file(Prg["FileDocumentsDb"])
    DocDb["docs"][BaseNameOrig] = _DocsSampleInfo["docs"][BaseNameOrig]
    obj_to_file(Prg["FileDocumentsDb"], DocDb)

# Used in tests
# read wanted key from config file
def config_get(Key, DefaultVal, DirPrgRoot, DirConfigFileParent=user.dir_home(), FileConfigBaseName=".sentence-seeker.config"):
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


