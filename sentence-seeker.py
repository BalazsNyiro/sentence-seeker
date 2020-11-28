#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
from tkinter import *

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
sys.path.append(os.path.join(DirPrgParent, "test"))

import config, util_test, argparse, separated_prg_launcher
##########################################################

import seeker, ui_console

def main():
    parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
    parser.add_argument("--test", help="execute only tests", action='store_true')
    parser.add_argument("--usage", help="display sort usage info", action='store_true')
    parser.add_argument("--query", help="pass query as param. Program exits after display result", action='store', default="")

    parser.add_argument("--ui", help="select user interface. (console, tkinter, html)", action='store', default='tkinter')
    Args = parser.parse_args()

    Usage = Args.usage
    Ui = Args.ui
    TestExecution = Args.test
    # SysArgvOrig = sys.argv
    sys.argv = sys.argv[:1] # the testing environment gives a warning when I use a prg param so I hide it, temporary solution

    print("Under development:")
    print(" - GUI/tkinter pager for faster result processing (it's implemented yet in console mode!!!)")
    print(" - colorful terminal usage in windows 10")
    # https://devblogs.microsoft.com/commandline/updating-the-windows-console-colors/

    if TestExecution:
        test_exec(Args)
    else: # separated program start because of ssp program planner import
        separated_prg_launcher.run(Usage=Usage, Ui=Ui, TestExecution=False, QueryAsCmdlineParam=Args.query)

def test_exec(Args):
    Prg = config.prg_config_create(Args, PrintForDeveloper=False)

    print("\n" * 22)
    print("##################### TEST BEGIN #####################################")
    import test_text
    import test_eng
    import test_util_json
    import test_util_ui
    import test_seeker_logic
    import test_util
    import test_document
    import test_seeker
    import test_converter

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    test_converter.run_all_tests(Prg)
    test_text.run_all_tests(Prg)
    test_seeker.run_all_tests(Prg)
    test_seeker_logic.run_all_tests(Prg)
    test_util_ui.run_all_tests(Prg)
    test_eng.run_all_tests(Prg)
    util_test.result_all(Prg)
    print("##################### TEST END #####################################")
    sys.exit(0)
    # print("\n"*22)

    ### EXTRAS AFTER BASIC TESTS ###
    # execute search from ui
    seeker.be_ready_to_seeking(Prg)
    ui_console.seek_and_display(Prg, Prg["QueryExamples"]["bird_or_cat"])

    # color_paletta_tester(Prg["UiThemes"]["SunSet"]["Highlights"])



####################################################################################
# color paletta original source - thank you
# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter
def tkinter_gui_color_paletta_tester(Colors):

    FONT_SIZE = 16  # (pixels)
    RowLimit = 24

    Root = Tk()
    Root.title("Named colour chart")

    Row = 0
    Col = 0
    for Color in Colors:
        Elem = Label(Root, text=Color, background=Color,
                  font=(None, -FONT_SIZE))
        Elem.grid(row=Row, column=Col, sticky=E + W)
        Row += 1
        if Row > RowLimit:
            Row = 0
            Col += 1

    Root.mainloop()
####################################################################################

main()
