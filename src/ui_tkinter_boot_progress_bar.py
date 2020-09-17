# -*- coding: utf-8 -*-
import util_ui
# https://www.geeksforgeeks.org/progressbar-widget-in-tkinter-python/

def bar_display(Prg, FunBehindBar):
    # STRANGE BUT NECESSARY import here
    # Don't import these on module level because in some environment
    # tkinter is not available and progressbar_close/refresh is
    # linked/used from seeker.py which is used from console UI, too
    # if I want to keep close/refresh here, it's necessary to hide imports in this fun
    from tkinter import HORIZONTAL, Tk, mainloop
    import tkinter.ttk
    ################################################################

    Root = Tk()
    Root.title(util_ui.title(Prg))
    Root.resizable(False, False)
    ProgressBar = tkinter.ttk.Progressbar(Root, orient=HORIZONTAL,
                                          length=600, mode='determinate')
    ProgressBar.pack(pady=10)
    Prg["ProgressBar"] = ProgressBar
    Prg["ProgressBarRoot"] = Root

    # start a function after mainloop
    # https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
    Root.after(10, FunBehindBar, Prg)

    mainloop()

def progressbar_refresh_if_displayed(Prg, Files, FileNumActual):
    if "ProgressBar" in Prg:
        Prg["ProgressBar"]["value"] = int((FileNumActual * 100.0) / len(Files))
        Prg["ProgressBarRoot"].update_idletasks()

def progressbar_close(Prg):
    if "ProgressBarRoot" in Prg:
        Prg["ProgressBarRoot"].destroy()
        Prg["ProgressBarRoot"].quit()
        del Prg["ProgressBar"]
        del Prg["ProgressBarRoot"]
