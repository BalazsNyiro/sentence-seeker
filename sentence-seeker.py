#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))

import config, util_test, argparse, prg_start
##########################################################

import seeker, ui_console

def main():
    parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
    parser.add_argument("--test", help="execute only tests", action='store_true')
    parser.add_argument("--usage", help="display sort usage info", action='store_true')

    parser.add_argument("--ui", help="select user interface. (console, tkinter, html)", action='store', default='tkinter')
    Args = parser.parse_args()

    Usage = Args.usage
    Ui = Args.ui
    TestExecution = Args.test
    # SysArgvOrig = sys.argv
    sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

    if TestExecution:
        test_exec(Args)
    else: # separated program start because of ssp program planner import
        prg_start.run(Usage=Usage, Ui=Ui, TestExecution=False)

def test_exec(Args):
    Prg = config.prg_config_create(Args, PrintForDeveloper=False)

    print("\n" * 22)
    print("##################### TEST BEGIN #####################################")
    import test_util, test_util_json, test_document, test_text, test_seeker, test_seeker_logic
    import test_converter

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    test_converter.run_all_tests(Prg)
    util_test.result_all(Prg)
    test_text.run_all_tests(Prg)
    test_seeker.run_all_tests(Prg)
    test_seeker_logic.run_all_tests(Prg)
    print("##################### TEST END #####################################")
    # sys.exit(0)
    # print("\n"*22)

    # execute search from ui
    seeker.be_ready_to_seeking(Prg)
    ui_console.seek_and_display(Prg, Prg["QueryExamples"]["bird_or_cat"])

main()
