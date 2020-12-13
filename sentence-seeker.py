#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys
from tkinter import *

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))
sys.path.append(os.path.join(DirPrgParent, "test"))

import config, util_test, argparse, prg_obj, util
##########################################################

import seeker, ui_console

def main():
    parser = argparse.ArgumentParser(prog="sentence-seeker", description="Collect example sentences from texts")
    parser.add_argument("--test", help="execute only tests", action='store_true')
    parser.add_argument("--usage", help="display sort usage info", action='store_true')
    parser.add_argument("--query", help="pass query as param. Program exits after display result", action='store', default="")
    parser.add_argument("--docs_load_defaults_forced", help="reload sample texts into document directory anyway - useful after git pull to load new books", action='store_true', default=False)
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
        prg_obj.run(Usage=Usage, Ui=Ui, TestExecution=False, QueryAsCmdlineParam=Args.query, DocsLoadDefaultsForced=Args.docs_load_defaults_forced)

def test_exec(Args):
    Prg = config.prg_config_create(TestExecution=True, PrintForDeveloper=False)

    print("\n" * 22)
    print("##################### TEST BEGIN #####################################")
    import test_converter
    import test_document
    import test_eng
    import test_result_selectors
    import test_seeker
    import test_seeker_logic
    import test_text
    import test_tokens
    import test_ui_html
    import test_util
    import test_util_json
    import test_util_ui

    # for token testing I need a real, huge text base.
    # to avoid plus storage, I use the text samples
    BooksForTest = [("_novels", "WilliamShakespeare__CompleteWorks__gutenberg_org_100-0")]
    for Book in BooksForTest:
        DirSample, BookBaseName = Book
        PathTest = os.path.join(Prg["DirDocuments"], BookBaseName + ".txt")
        PathSource = os.path.join(Prg["DirTextSamples"], DirSample, BookBaseName + ".txt.gz")
        if not os.path.isfile(PathTest):
            print("Doesn't EXIST:", PathTest)
            #print(PathSource)
            _, Txt = util.file_read_all(Fname=PathSource, Gzipped=True)
            util.file_write_utf8_error_avoid(dict(), Fname=PathTest, Content=Txt)
        else:
            print("       EXISTs:", PathTest)

    test_util.run_all_tests(Prg)
    test_util_json.run_all_tests(Prg)
    test_document.run_all_tests(Prg)
    test_converter.run_all_tests(Prg)
    test_text.run_all_tests(Prg)
    test_seeker.run_all_tests(Prg)
    test_seeker_logic.run_all_tests(Prg)
    test_util_ui.run_all_tests(Prg)
    test_eng.run_all_tests(Prg)
    test_ui_html.run_all_tests(Prg)
    test_tokens.run_all_tests(Prg)
    test_result_selectors.run_all_tests(Prg)
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
