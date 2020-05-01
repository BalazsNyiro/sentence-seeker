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
parser.add_argument("--gui", help="select user interface. (cli, tkinter, web)", action='store')
Args = parser.parse_args()

SysArgvOrig = sys.argv
sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

if Args.test:
    import test_util, test_util_json, test_document, test_text

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    test_text.run_all_tests(Prg)
    util_test.result_all(Prg)
    sys.exit(0)

document.docs_copy_samples_into_dir_if_necessary(Prg)

#########################################
import method_a_naive_01, gui_cli
method_a_naive_01.be_ready_to_seeking(Prg)

gui_cli.user_interface_start(Prg, Args)

print(Prg["Statistics"])


