#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))

import config, util_test, document, argparse
##########################################################

Prg = config.PrgConfigCreate(PrintForDeveloper=True)
config.DirsFilesConfigCreate(Prg)

parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
parser.add_argument("--test", help="execute only tests", action='store_true')
args = parser.parse_args()

if args.test:
    import test_util, test_util_json, test_document

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    util_test.result_all(Prg)
    sys.exit(0)

DocumentsAvailable = document.collect_docs_from_working_dir(Prg)
