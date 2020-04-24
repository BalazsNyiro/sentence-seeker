# -*- coding: utf-8 -*-
import json, os

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
def config(DirPrgRoot, Key, Default):
    Json = config_obj(DirPrgRoot)
    if Key in Json:
        return Json[Key]
    return Default

def config_obj(DirPrgRoot):
    FileConfig = os.path.join(DirPrgRoot, "config.json")
    return json_obj_from_file(FileConfig)

