# -*- coding: utf-8 -*-
import os, util, json

############ JSON #############################

# Tested
def obj_from_file(JsonFileName):
    try:
        _ReadStatus, FileContent = util.file_read_all(Prg={}, Fname=JsonFileName)
        return "ok", json.loads(FileContent)

    except json.decoder.JSONDecodeError:
        FileContent = util.file_read_all_simple(JsonFileName)
        Msg = f"Json decoder error: {JsonFileName}:>>" + FileContent + "<<"
        print(Msg)
        return "error", Msg

# Tested
def obj_to_file(JsonFileName, Data):
    with open(JsonFileName, 'w') as OutFile:
        json.dump(Data, OutFile, sort_keys=True, indent=4)

# Tested
def doc_source_webpages_update_in_file_and_Prg(Prg, BaseNameNoExtAdd=None, DocObjAdd=None, BaseNameNoExtRemove=None):
    doc_source_webpages_update_in_Prg(Prg, BaseNameNoExtAdd=BaseNameNoExtAdd, DocObjAdd=DocObjAdd, BaseNameNoExtRemove=BaseNameNoExtRemove)
    doc_source_webpages_save_from_memory_to_file(Prg)

# Tested with in_file_and_Prg
def doc_source_webpages_update_in_Prg(Prg, BaseNameNoExtAdd=None, DocObjAdd=None, BaseNameNoExtRemove=None):
    if BaseNameNoExtAdd and DocObjAdd: # if we receive new elem, insert it
        if "DocumentsSourceWebpages" not in Prg: # from tests fake Prg can arrive
            Prg["DocumentsSourceWebpages"] = dict()
        Prg["DocumentsSourceWebpages"][BaseNameNoExtAdd] = DocObjAdd

    if BaseNameNoExtRemove and BaseNameNoExtRemove in Prg["DocumentsSourceWebpages"]:
        del Prg["DocumentsSourceWebpages"][BaseNameNoExtRemove]

# Tested with in_file_and_Prg
def doc_source_webpages_save_from_memory_to_file(Prg):
    DocumentsSourceWebpagesFileName = Prg["DocumentsSourceWebpagesFileName"]
    Status, DocSources = obj_from_file(DocumentsSourceWebpagesFileName)
    if Status == "ok": # obj_from_file display error if something is wrong

        if "docs" not in DocSources:
            DocSources["docs"] = {}

        DocSources["docs"] = Prg["DocumentsSourceWebpages"]
        obj_to_file(DocumentsSourceWebpagesFileName, DocSources)

        Prg["DocumentsSourceWebpagesFileContent"] = json_to_str(DocSources)

# tested in test_util_json
def json_to_str(Obj):
    return json.dumps(Obj, sort_keys=True, indent=4)

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

    _Status, Json = obj_from_file(FileConfigAbsPath)
    if Key in Json:
        return Json[Key]
    return DefaultVal


