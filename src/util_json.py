# -*- coding: utf-8 -*-
import json, os, user, util

############ JSON #############################

# Tested
def json_obj_from_file(JsonFileName):
    with open(JsonFileName) as f:
        return json.load(f)

# Tested
def json_obj_to_file(JsonFileName, Data):
    with open(JsonFileName, 'w') as OutFile:
        json.dump(Data, OutFile, sort_keys=True, indent=4)

# Used in tests
# read wanted key from config file
def config_get(Key, DefaultVal, DirPrgRoot, DirConfigFileParent=user.dir_home(), FileConfigBaseName=".sentence-seeker.config"):
    FileConfigAbsPath = os.path.join(DirConfigFileParent, FileConfigBaseName)

    if not os.path.isfile(FileConfigAbsPath):
        print(f"create new config file from default: {FileConfigAbsPath}")
        util.file_copy(os.path.join(DirPrgRoot, FileConfigBaseName), FileConfigAbsPath)
    else:
        print(f"config file exists: {FileConfigAbsPath}")

    Json = json_obj_from_file(FileConfigAbsPath)
    if Key in Json:
        return Json[Key]
    return DefaultVal


