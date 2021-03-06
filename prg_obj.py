#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import config, document, seeker, ui_console, ui_html, util
import ui_tkinter_boot_progress_bar, ui_tkinter, ui_json
from http.server import HTTPServer
import os

# prg start is important because I import/start sentence-seeker
# from ssp program planner and this is a simple executable interface
def run(Ui="ssp_program_planner",
        Usage=False,
        TestExecution=False,
        QueryAsCmdlineParam="",
        DocsLoadDefaultsForced=False,
        DirDocuments=""):
    Prg = config.prg_config_create(TestExecution, PrintForDeveloper=False, DirDocuments=DirDocuments)

    if Usage:
        print(Prg["UsageInfo"])
        input("press ENTER to start program")

    # sys.setprofile(util.TraceFunc)

    # check: can we start gui?
    if Ui == "tkinter" and Prg["OsIsLinux"]:
        if "DISPLAY" not in os.environ:
            print("Can't start tkinter ui because DISPLAY environment variable is not available -> switch to console ui")
            Ui = "console"

    print(f"\nUI start: {Ui}")
    Prg["Ui"] = Ui

    # not only console mode but gui/tkinter can print to the terminal
    util.if_win__set_windows_console_enable_ansi_escapes(Prg)

    document.docs_copy_samples_into_dir_if_necessary(Prg, LoadDefaultsForced=DocsLoadDefaultsForced)

    # the program planner analyses one execution
    if Ui == "ssp_program_planner":
        seeker.be_ready_to_seeking(Prg)
        ui_console.seek_and_display(Prg, "looks, like, bird")

    if Ui == "console":
        seeker.be_ready_to_seeking(Prg)
        ui_console.user_interface_start(Prg, Ui, QueryAsCmdlineParam=QueryAsCmdlineParam)

    elif Ui == "tkinter":
        # seeker.be_ready_to_seeking(Prg)
        ui_tkinter_boot_progress_bar.bar_display(Prg, seeker.be_ready_to_seeking)
        ui_tkinter.win_main(Prg)
    elif Ui == "json":
        seeker.be_ready_to_seeking(Prg)
        ui_json.SimpleHTTPRequestHandler.Prg = Prg
        httpd = HTTPServer((Prg["ServerHost"], Prg["ServerPort"]), ui_json.SimpleHTTPRequestHandler)
        httpd.serve_forever()
    elif Ui == "html":
        print("the simple html ui can run for 2-3 days without execution.\n"
              "if you want to run it on server use this from sentence-seeker root dir:\n"
              "./tools/http_server_restart_daily.sh"
              "the used port is blocked after 2 days, It's a hotfix.")
        seeker.be_ready_to_seeking(Prg)
        ui_html.SimpleHTTPRequestHandler.Prg = Prg
        httpd = HTTPServer((Prg["ServerHost"], Prg["ServerPort"]), ui_html.SimpleHTTPRequestHandler)
        print("httpd server starts...")
        httpd.serve_forever()

    # print("Statistics", Prg["Statistics"])
