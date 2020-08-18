#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))

import config, util_test, document, argparse
##########################################################

import seeker, ui_console, ui_tkinter, ui_json, ui_html
from http.server import HTTPServer
import ui_tkinter_boot_progress_bar

Prg = config.PrgConfigCreate(PrintForDeveloper=False)

parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
parser.add_argument("--test", help="execute only tests", action='store_true')
parser.add_argument("--usage", help="display sort usage info", action='store_true')

parser.add_argument("--ui", help="select user interface. (console, tkinter, web)", action='store', default='tkinter')
Args = parser.parse_args()

if Args.usage:
    print(Prg["UsageInfo"])
    input("press ENTER to start program")

SysArgvOrig = sys.argv
sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

if Args.test:
    print("\n"*22)
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
    sys.exit(0)
    print("\n"*22)

    # execute search from ui
    seeker.be_ready_to_seeking(Prg)
    ui_cli.seek_and_display(Prg, "looks, like, bird")
    sys.exit(0)

document.docs_copy_samples_into_dir_if_necessary(Prg)

#########################################

#sys.setprofile(util.TraceFunc)
print(f"\nUI start: {Args.ui}")
if Args.ui == "console":
    seeker.be_ready_to_seeking(Prg)
    ui_console.user_interface_start(Prg, Args)

elif Args.ui == "tkinter":
    # seeker.be_ready_to_seeking(Prg)
    ui_tkinter_boot_progress_bar.bar_display(Prg, seeker.be_ready_to_seeking)
    ui_tkinter.win_main(Prg, Args)
elif Args.ui == "json":
    seeker.be_ready_to_seeking(Prg)
    ui_json.SimpleHTTPRequestHandler.Prg = Prg
    httpd = HTTPServer((Prg["ServerHost"], Prg["ServerPort"]), ui_json.SimpleHTTPRequestHandler)
    httpd.serve_forever()
elif Args.ui == "html":
    seeker.be_ready_to_seeking(Prg)
    ui_html.SimpleHTTPRequestHandler.Prg = Prg
    httpd = HTTPServer((Prg["ServerHost"], Prg["ServerPort"]), ui_html.SimpleHTTPRequestHandler)
    httpd.serve_forever()

print(Prg["Statistics"])


