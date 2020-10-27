# -*- coding: utf-8 -*-
import os, util, json

############ JSON #############################

# Tested
def obj_from_file(JsonFileName):
    try:
        _ReadStatus, FileContent = util.file_read_all(Prg={}, Fname=JsonFileName)
        JsonObj = json.loads(FileContent)
        return "ok", JsonObj
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
    DocumentsSourceWebpagesFileName = Prg["DocumentsSourceWebpagesFileName"]

    Status, DocSources = obj_from_file(DocumentsSourceWebpagesFileName)
    if Status == "ok": # obj_from_file display error if something is wrong

        if "docs" not in DocSources:
            DocSources["docs"] = {}

        UpdatedInMemory = False
        if BaseNameNoExtAdd and DocObjAdd: # if we receive new elem, insert it
            DocSources["docs"][BaseNameNoExtAdd] = DocObjAdd
            UpdatedInMemory = True

        if BaseNameNoExtRemove and BaseNameNoExtRemove in DocSources["docs"]:
            del DocSources["docs"][BaseNameNoExtRemove]
            UpdatedInMemory = True

        if UpdatedInMemory: # then save it back to file
            # the file is updated AND DocumentsSourceWebpages is updated, too, and DocumentsSourceWebpagesFileContent, too
            obj_to_file(DocumentsSourceWebpagesFileName, DocSources)
            Prg["DocumentsSourceWebpages"] = DocSources["docs"]

            # here we load it once and in ui_html
            # we don't have to reload it at every request
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


