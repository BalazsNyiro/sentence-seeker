# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox
import webbrowser
import seeker, util_ui

WordsEntry = None
SentencesArea = None
PrgGlob = None

def seek_and_display(KeypressEvent=""):
    Words = WordsEntry.get()
    # msg_box(Words)
    SentencesArea.delete('1.0', tk.END)
    WordsWanted, MatchNums__ResultInfo, ResultsTotalNum = seeker.seek(PrgGlob, Words)
    # sentence_result_all_display(Prg, MatchNums__ResultInfo)
    # print(f"Results Total: {ResultsTotalNum}")
    SentencesArea.insert(tk.END, f"words: {Words}\n\n", "TextTitle")
    SentencesArea.insert(tk.END, "Sentences:\n", "TextTitle")

    ##############################################################
    for DisplayedCounter, SentenceObj in enumerate(MatchNums__ResultInfo, start=1):
        sentence_result_one_display(PrgGlob, SentenceObj, SentencesArea, DisplayedCounter)
        if DisplayedCounter >= PrgGlob["LimitDisplayedSampleSentences"]:
            break

    SentencesArea.insert(tk.END, f"Total:{ResultsTotalNum}\n", "follow")
    for WordWanted in WordsWanted:
        SentencesArea.highlight_pattern(WordWanted, "Highlighted")

# This class came from here
# https://stackoverflow.com/questions/3781670/how-to-highlight-text-in-a-tkinter-text-widget
class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tk.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


def sentence_result_one_display(Prg, Result, SentencesArea, DisplayedCounter):
    WordsDetectedInSubsentence, Url, Sentence, WordsDetectedNum, Source = util_ui.sentence_get_from_result(Prg, Result)
    SentencesArea.insert(tk.END, Sentence + "\n", "SentenceDisplayed")
    SentencesArea.insert(tk.END, f"Source: {Source}\n", "SourceDisplayed")

    TagName = f"tag_{DisplayedCounter}"
    SentencesArea.tag_configure(TagName,
                                foreground="blue",
                                underline=1,
                                font=('Tempus Sans ITC', 9, 'normal'))
    SentencesArea.tag_bind(TagName, "<1>",
                           lambda e, UrlToOpen=Url: webbrowser.open_new_tab(UrlToOpen)
                          )

    SentencesArea.insert(tk.END, Url + "\n\n",  TagName)

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
    MenuAbout.add_command(label="Contact", compound='left', command=msg_contact)

    Root.config(menu=MenuBar)

    Theme = util_ui.theme_actual(Prg)
    ################################################
    tk.Label(Root, text="Words").grid(row=0, sticky=tk.W)

    global WordsEntry
    WordsEntry = tk.Entry(Root, background=Theme["BgWords"])
    WordsEntry.focus()
    WordsEntry.bind("<Return>", seek_and_display)
    WordsEntry.bind("<FocusIn>", lambda _: WordsEntry.delete(0, 999)) # clear when clicked
    WordsEntry.grid(row=0, column=1, sticky=tk.W)

    tk.Button(Root, text="Get example sentences", command=seek_and_display).grid(row=2, column=1, sticky=tk.W)

    ################################################
    global SentencesArea
    SentencesArea = CustomText(Root, height=Theme["SentencesHeight"], width=Theme["SentencesWidth"],
                            background=Theme["BgAreaSentences"], foreground=Theme["FgAreaSentences"])
    SentencesArea.grid(row=3, column=1, sticky=tk.E)
    scroll = tk.Scrollbar(Root, command=SentencesArea.yview)
    SentencesArea.configure(yscrollcommand=scroll.set)
    scroll.grid(row=3, column=2, sticky=tk.NS)

    SentencesArea.tag_configure("Highlighted", background="yellow")
    SentencesArea.tag_configure("TextTitle", font=("Verdana", 20, "bold"))
    SentencesArea.tag_configure("SentenceDisplayed",
                                foreground=Theme["FgSentence"],
                                font=Theme["FontTitle"])
    SentencesArea.tag_configure("UrlDisplayed",
                                foreground=Theme["FgUrl"],
                                font=Theme["FontUrl"])
    SentencesArea.tag_configure("SourceDisplayed",
                                foreground=Theme["FgSource"],
                                font=Theme["FontSource"])
    SentencesArea.tag_bind("follow", "<1>",
                           lambda e, t=SentencesArea: t.insert(tk.END, "Click is detected :-)"))

    Root.mainloop()

def website_open():
    webbrowser.open_new_tab("http://www.sentence-seeker.net")

def facebook_group_open():
    webbrowser.open("https://www.facebook.com/groups/2449430305347843")

def msg_box(Msg="no msg", Title="Info"):
    tkinter.messagebox.showinfo(Title, Msg)

def msg_contact():
    msg_box("Author: Balazs Nyiro\ndiogenesz@pergamen.hu")
