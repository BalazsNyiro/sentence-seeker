# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.ttk

root = Tk()
progress = tkinter.ttk.Progressbar(root, orient=HORIZONTAL,
                       length=100, mode='determinate')
def bar():
    import time
    progress['value'] = 20
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    root.update_idletasks()
    time.sleep(1)
    progress['value'] = 100
    root.destroy()

progress.pack(pady=10)
Button(root, text='Start', command=bar).pack(pady=10)

# infinite loop
mainloop()
