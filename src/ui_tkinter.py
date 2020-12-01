# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.messagebox
import webbrowser
import seeker_logic, util_ui

WordsEntry = None
ExplainOnly = None
SentencesArea = None
PrgGlob = None

LeftMarginFirstLine = 6
LeftMarginOtherLines = 2

# can't display too complex explanation
ExplainLimit = 24

def seek_and_display(KeypressEvent=""):
    Words = WordsEntry.get()
    # msg_box(Words)
    SentencesArea.delete('1.0', tk.END)
    TokenProcessExplainSumma, WordsWanted, MatchNums__ResultInfo, ResultsTotalNum = seeker_logic.seek(PrgGlob, Words, ExplainOnly=(ExplainOnly.get()==1))

    TokenExplain = util_ui.token_explain_summa_to_text(TokenProcessExplainSumma, ExplainLimit=ExplainLimit)
    SentencesArea.insert(tk.END, f"Token explanation: \n{TokenExplain}\n\n", "SentenceDisplayed")
    SentencesArea.insert(tk.END, f"words: {Words}\n\n", "TextTitle")
    SentencesArea.insert(tk.END, "Sentences:\n", "TextTitle")

    ##############################################################
    for DisplayedCounter, SentenceObj in enumerate(MatchNums__ResultInfo, start=1):
        sentence_result_one_display(PrgGlob, SentenceObj, SentencesArea, DisplayedCounter)
        if DisplayedCounter >= PrgGlob["SettingsSaved"]["Ui"]["LimitDisplayedSentences"]:
            break

    Theme = util_ui.theme_actual(PrgGlob)
    SentencesArea.insert(tk.END, f"Total:{ResultsTotalNum}\n", "follow")

    NumOfColorThemes = len(Theme["Highlights"])
    for WordId, WordWanted in enumerate(WordsWanted):
        TagName = f"Highlighted_{WordId}"

        # here we have problems at irregular verbs
        ThemeId = WordId % NumOfColorThemes # if we have too much words, keep the id in the range of available colors
        SentencesArea.tag_configure(TagName, background=Theme["Highlights"][ThemeId])
        SentencesArea.highlight_pattern(fr"\y{WordWanted}\y", TagName, regexp=True, NoCase=True)


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
                          regexp=False, NoCase=False):
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
                                count=count, regexp=regexp, nocase=NoCase)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")

# http://effbot.org/tkinterbook/text.htm
# https://bytes.com/topic/python/answers/46109-programmatic-links-tkinter-textbox
def show_hand_cursor(event):
    #print("<Enter> show hand cursor")
    event.widget.configure(cursor="hand1")
def show_arrow_cursor(event):
    #print("<Leave> show hand cursor")
    event.widget.configure(cursor="")

def sentence_result_one_display(Prg, Result, SentencesArea, DisplayedCounter):
    Url, Sentence, Source = util_ui.sentence_text_from_obj(Prg, Result, ReturnType="separated_subsentences")

    # SentencesArea.insert(tk.END, Sentence + "\n", "SentenceDisplayed")
    SentencesArea.insert(tk.END, Sentence["subsentences_before"], "SentenceDisplayed")
    SentencesArea.insert(tk.END, Sentence["subsentence_result"], "SentenceDisplayedResult")
    SentencesArea.insert(tk.END, Sentence["subsentences_after"] + "\n", "SentenceDisplayed")


    if Prg["SettingsSaved"]["Ui"]["DisplaySourceFileNameBelowSentences"]:
        SentencesArea.insert(tk.END, f"Source: {Source}\n", "SourceDisplayed")

    #######################################################
    TagName = f"tag_{DisplayedCounter}"
    SentencesArea.tag_configure(TagName,
                                foreground="blue",
                                underline=1,
                                font=('Tempus Sans ITC', 9, 'normal'),
                                lmargin1=LeftMarginOtherLines)
    if Prg["SettingsSaved"]["Ui"]["DisplaySourceUrlBelowSentences"]:
        SentencesArea.tag_bind(TagName, "<1>",
                               lambda e, UrlToOpen=Url: webbrowser.open_new_tab(UrlToOpen)
                              )
        SentencesArea.tag_bind(TagName, "<Enter>", show_hand_cursor)
        SentencesArea.tag_bind(TagName, "<Leave>", show_arrow_cursor)
        SentencesArea.insert(tk.END, Url, TagName)
    SentencesArea.insert(tk.END, "\n\n", TagName)

def win_main(Prg):
    global PrgGlob
    PrgGlob = Prg

    Root = tk.Tk()
    Prg["UiRootObj"] = Root

    util_ui.title_refresh(Prg)

    Root.geometry(Prg["UiWindowGeometry"])

    MenuBar = tk.Menu(Root)

    MenuAbout = tk.Menu(MenuBar, tearoff=1)
    MenuBar.add_cascade(label='About', menu=MenuAbout)
    MenuAbout.add_command(label="Site", compound='left', command=website_open)
    MenuAbout.add_command(label="Facebook group", compound='left', command=facebook_group_open)
    MenuAbout.add_command(label="Contact", compound='left', command=msg_contact)

    Root.config(menu=MenuBar)

    Theme = util_ui.theme_actual(Prg)
    ################################################

    # placeholder, small distance from left frame
    tk.Label(Root, text=" ").grid(row=0, column=0, sticky=tk.W)

    global WordsEntry
    WordsEntry = tk.Entry(Root, background=Theme["BgWords"], font=Theme["QueryWordEntry"])

    WordsEntry.focus() # focus
    WordsEntry.delete(0, tk.END)
    WordsEntry.insert(0, Prg["QueryExamples"]["bird_or_cat"])

    WordsEntry.bind("<Return>", seek_and_display)
    WordsEntry.bind("<Control-KeyRelease-a>", select_all_words_entry)

    # don't delete entry because user maybe wants to edit prev query
    #WordsEntry.bind("<FocusIn>", lambda _: WordsEntry.delete(0, 999)) # clear when clicked

    WordsEntry.grid(row=0, column=1, sticky=tk.W, ipadx=220, ipady=0, columnspan=3)

    tk.Button(Root, text="Get example sentences", command=seek_and_display).grid(row=2, column=1, sticky=tk.W)

    global ExplainOnly
    ExplainOnly = tk.IntVar()
    tk.Checkbutton(Root, text="explain only", variable=ExplainOnly).grid(row=2, column=2, sticky=tk.W)

    ################################################
    global SentencesArea
    SentencesArea = CustomText(Root, height=Theme["SentencesHeight"], width=Theme["SentencesWidth"],
                            background=Theme["BgAreaSentences"], foreground=Theme["FgAreaSentences"])
    SentencesArea.grid(row=3, column=1, sticky="nsew", columnspan=3) # tk.E
    # https://effbot.org/tkinterbook/grid.htm
    # https://stackoverflow.com/questions/24945467/python-tkinter-set-entry-grid-width-100
    # https://stackoverflow.com/questions/27614037/python-3-tkinter-create-text-widget-covering-100-width-with-grid
    Root.grid_columnconfigure(1, weight=1)
    Root.grid_rowconfigure(3, weight=1)

    scroll = tk.Scrollbar(Root, command=SentencesArea.yview)
    SentencesArea.configure(yscrollcommand=scroll.set)
    scroll.grid(row=3, column=4, sticky=tk.NS)

    SentencesArea.tag_configure("TextTitle", font=("Verdana", 20, "bold"))
    SentencesArea.tag_configure("SentenceDisplayedResult",
                                foreground=Theme["FgSubSentenceResult"],
                                font=Theme["FontSentenceResult"],
                                lmargin1=LeftMarginFirstLine,
                                lmargin2=LeftMarginOtherLines)
    SentencesArea.tag_configure("SentenceDisplayed",
                                foreground=Theme["FgSentence"],
                                font=Theme["FontSentenceNormal"],
                                lmargin1=LeftMarginFirstLine,
                                lmargin2=LeftMarginOtherLines)
    SentencesArea.tag_configure("SourceDisplayed",
                                foreground=Theme["FgSource"],
                                font=Theme["FontSource"],
                                lmargin1=LeftMarginOtherLines)
    SentencesArea.tag_bind("follow", "<1>",
                           lambda e, t=SentencesArea: t.insert(tk.END, "Click is detected :-)"))

    SentencesArea.insert(tk.END, "Usage\n\n", "TextTitle")
    SentencesArea.insert(tk.END, Prg["UsageInfo"], "SentenceDisplayed")

    SentencesArea.insert(tk.END, "\n\nLicense info\n\n", "TextTitle")
    SentencesArea.insert(tk.END, Prg["Licenses"] + "\n", "SentenceDisplayed")

    Root.mainloop()

def website_open():
    webbrowser.open_new_tab("http://www.sentence-seeker.net")

def facebook_group_open():
    webbrowser.open("https://www.facebook.com/groups/2449430305347843")

def msg_box(Msg="no msg", Title="Info"):
    tkinter.messagebox.showinfo(Title, Msg)

def msg_contact():
    msg_box("Author: Balazs Nyiro\ndiogenesz@pergamen.hu")

# Select all the text in textbox
def select_all_words_entry(event):
    # select text
    WordsEntry.select_range(0, 'end')
    # move cursor to the end
    WordsEntry.icursor('end')

# based on: https://pythonprogramming.altervista.org/tkinters-messagebox-without-the-root-window/
def independent_yes_no_window(Title, Question, Geometry="200x150"):
    Root = tkinter.Tk()
    Root.overrideredirect(1)
    Root.geometry(Geometry)
    Root.withdraw()
    Reply = tkinter.messagebox.askyesno(Title, Question)
    Root.destroy()
    return Reply

