# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk
# https://www.geeksforgeeks.org/progressbar-widget-in-tkinter-python/

def bar_display(Prg, FunBehindBar):
    Root = Tk()
    Root.title(f"sentence-seeker: {Prg['DirDocuments']}")
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
