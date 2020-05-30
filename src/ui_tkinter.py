# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox
import webbrowser
import seeker, util_ui

SentencesWidth = 100
SentencesHeight = 50
WordsEntry = None
SentencesArea = None
PrgGlob = None

def seek_and_display(KeypressEvent=""):
    Wanted = WordsEntry.get()
    # msg_box(Words)
    _WordsWanted, MatchNums__ResultInfo, ResultsTotalNum = seeker.seek(PrgGlob, Wanted)
    # sentence_result_all_display(Prg, MatchNums__ResultInfo)
    # print(f"Results Total: {ResultsTotalNum}")
    SentencesArea.insert(tk.END, "\nSentences:\n", "TextTitle")

    ##############################################################
    # Sentences.insert(tk.END, str(MatchNums__ResultInfo), "color")
    for DisplayedCounter, SentenceObj in enumerate(MatchNums__ResultInfo, start=1):
        sentence_result_one_display(PrgGlob, SentenceObj, SentencesArea)
        if DisplayedCounter >= PrgGlob["LimitDisplayedSampleSentences"]:
            break
    SentencesArea.insert(tk.END, f"Total:{ResultsTotalNum}\n", "follow")

def sentence_result_one_display(Prg, Result, Area):
    WordsDetectedInSubsentence, Url, Sentence, WordsDetectedNum, Source = util_ui.sentence_get_from_result(Prg, Result)
    Area.insert(tk.END, Sentence+"\n\n", "color")

def win_main(Prg, Args):
    global PrgGlob
    PrgGlob = Prg

    Root = tk.Tk()
    Root.title("sentence-seeker")

    MenuBar = tk.Menu(Root)

    MenuAbout = tk.Menu(MenuBar, tearoff=1)
    MenuBar.add_cascade(label='About', menu=MenuAbout)
    MenuAbout.add_command(label="Site", compound='left', command=website_open)
    MenuAbout.add_command(label="Facebook group", compound='left', command=facebook_group_open)

    Root.config(menu=MenuBar)

    ################################################
    tk.Label(Root, text="Words").grid(row=0, sticky=tk.W)

    global WordsEntry
    WordsEntry = tk.Entry(Root)
    WordsEntry.focus()
    WordsEntry.bind("<Return>", seek_and_display)
    WordsEntry.grid(row=0, column=1, sticky=tk.W)

    tk.Button(Root, text="Get example sentences", command=seek_and_display).grid(row=2, column=1, sticky=tk.W)

    ################################################
    global SentencesArea
    SentencesArea = tk.Text(Root, height=SentencesHeight, width=SentencesWidth)
    SentencesArea.grid(row=3, column=1, sticky=tk.E)
    scroll = tk.Scrollbar(Root, command=SentencesArea.yview)
    SentencesArea.configure(yscrollcommand=scroll.set)
    scroll.grid(row=3, column=2, sticky=tk.NS)

    SentencesArea.tag_configure('bold_italics', font=('Arial', 12, 'bold', 'italic'))
    SentencesArea.tag_configure('TextTitle', font=('Verdana', 20, 'bold'))
    SentencesArea.tag_configure('color',
                                foreground='#476042',
                                font=('Tempus Sans ITC', 12, 'bold'))
    SentencesArea.tag_bind('follow',
                   '<1>',
                           lambda e, t=SentencesArea: t.insert(tk.END, "Not now, maybe later!"))

    Root.mainloop()

def website_open():
    webbrowser.open_new_tab("http://www.sentence-seeker.net")

def facebook_group_open():
    webbrowser.open("https://www.facebook.com/groups/2449430305347843")

def msg_box(Msg="no msg", Title="Info"):
    tkinter.messagebox.showinfo(Title, Msg)
