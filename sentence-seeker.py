#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, time

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))

import config, util_test, document, argparse, stats
##########################################################

Prg = config.PrgConfigCreate(PrintForDeveloper=True)
config.DirsFilesConfigCreate(Prg)

parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
parser.add_argument("--test", help="execute only tests", action='store_true')
args = parser.parse_args()

SysArgvOrig = sys.argv
sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

if args.test:
    import test_util, test_util_json, test_document

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    util_test.result_all(Prg)
    sys.exit(0)

document.docs_load_all_to_be_ready_to_seeking(Prg)

# REALLY UGLY PROCESSING BUT I WANT TO MEASURE TIME USAGE
# FIXME LATER and use indexes.
print("=============  FIRST SEEK ===========")
LinesSelected = []
stats.save(Prg, "first seek =>")
TimeStart = time.time()
CharCounter = 0
for DocBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():
    Text = DocObj["Text"]

    print(DocBaseName, len(Text))
    CharCounter += len(Text)
    for Line in Text.split("\n"):
        if "where" in Line:
            LinesSelected.append(Line)

TimeEnd = time.time()
print("\n".join(LinesSelected))
print("Time USED:", TimeEnd - TimeStart, f"CharCounter: {CharCounter}, page: {CharCounter/2000}")
stats.save(Prg, "first seek <=")

print(Prg["Statistics"])
