# -*- coding: utf-8 -*-
import util_ui
# https://www.geeksforgeeks.org/progressbar-widget-in-tkinter-python/

def bar_display(Prg, FunBehindBar, FunParams=(), Title=""):
    # STRANGE BUT NECESSARY import here
    # Don't import these on module level because in some environment
    # tkinter is not available and progressbar_close/refresh is
    # linked/used from seeker.py which is used from console UI, too
    # if I want to keep close/refresh here, it's necessary to hide imports in this fun
    from tkinter import HORIZONTAL, Tk, mainloop
    import tkinter.ttk
    ################################################################

    if not Title:
        Title = util_ui.title(Prg)

    Root = Tk()
    Root.title(Title)
    Root.resizable(False, False)
    ProgressBar = tkinter.ttk.Progressbar(Root, orient=HORIZONTAL,
                                          length=600, mode='determinate')
    ProgressBar.pack(pady=10)
    Prg["ProgressBar"] = ProgressBar
    Prg["ProgressBarFunParams"] = FunParams
    Prg["ProgressBarRoot"] = Root

    # start a function after mainloop
    # https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
    Root.after(10, FunBehindBar, Prg)

    mainloop()

def progressbar_refresh_if_displayed(Prg, TotalNum, ActualNum):
    ProgressPercent = int((ActualNum * 100.0) / TotalNum)
    if "ProgressBar" in Prg:
        Prg["ProgressBar"]["value"] = ProgressPercent
        Prg["ProgressBarRoot"].update_idletasks()
    return ProgressPercent

def progressbar_close(Prg):
    if "ProgressBarRoot" in Prg:
        Prg["ProgressBarRoot"].destroy()
        Prg["ProgressBarRoot"].quit()
        del Prg["ProgressBar"]
        del Prg["ProgressBarRoot"]
        del Prg["ProgressBarFunParams"]
