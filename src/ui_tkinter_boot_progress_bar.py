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
    Prg["ProgressBar"] = {"TtkProgressbar": ProgressBar,
                          "FunParams": FunParams,
                          "Root": Root,
                          }

    # start a function after mainloop
    # https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
    Root.after(200, FunBehindBar, Prg)

    mainloop()

def progressbar_refresh_if_displayed(Prg, TotalNum, ActualNum):
    if "ProgressBar" in Prg:
        Prg["ProgressBar"]["TtkProgressbar"]["value"] = int((ActualNum * 100.0) / TotalNum)
        Prg["ProgressBar"]["Root"].update_idletasks()

def progressbar_close(Prg):
    if "ProgressBar" in Prg:
        Prg["ProgressBar"]["Root"].destroy()
        Prg["ProgressBar"]["Root"].quit()
        del Prg["ProgressBar"]
