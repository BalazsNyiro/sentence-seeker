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

def doc_db_update_in_file_and_reload(Prg, FileWithoutExtension, DocObj=None):
    DocDb = obj_from_file(Prg["FileDocumentsDb"])
    DocDb["docs"][FileWithoutExtension] = DocObj
    obj_to_file(Prg["FileDocumentsDb"], DocDb)
    Prg["DocumentsDb"] = obj_from_file(Prg["FileDocumentsDb"])["docs"]
    Prg["FileDocumentsDbContent"] = json.dumps(DocDb, sort_keys=True, indent=4)

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


