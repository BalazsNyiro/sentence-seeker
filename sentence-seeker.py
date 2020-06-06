#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))

import config, util_test, document, argparse
##########################################################

import seeker, ui_cli, ui_tkinter, util

Prg = config.PrgConfigCreate(PrintForDeveloper=False)

parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
parser.add_argument("--test", help="execute only tests", action='store_true')

parser.add_argument("--ui", help="select user interface. (cli, tkinter, web)", action='store', default='tkinter')
Args = parser.parse_args()

SysArgvOrig = sys.argv
sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

if Args.test:
    print("\n"*22)
    print("##########################################################")
    import test_util, test_util_json, test_document, test_text, test_seek
    import test_converter

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    test_converter.run_all_tests(Prg)
    util_test.result_all(Prg)
    test_text.run_all_tests(Prg)
    test_seek.run_all_tests(Prg)
    print("##########################################################")
    print("\n"*22)

    # execute search from ui
    seeker.be_ready_to_seeking(Prg)
    ui_cli.seek_and_display(Prg, "looks, like, bird")
    sys.exit(0)

document.docs_copy_samples_into_dir_if_necessary(Prg)

#########################################
seeker.be_ready_to_seeking(Prg)

#sys.setprofile(util.TraceFunc)
if Args.ui == "cli":
    ui_cli.user_interface_start(Prg, Args)

elif Args.ui == "tkinter":
    ui_tkinter.win_main(Prg, Args)

print(Prg["Statistics"])


