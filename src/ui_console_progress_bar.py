import sys
# I use console progress bar from util.py and util_ui imports util.py
# avoid cross reference this fun is outsourced
from ui_console import AnsiControlInit
# originally it's place was in util_ui
class progress_bar_console():
    def __init__(self, BarLen=30, ValueFrom=0, ValueTo=100, ValueNow=0, DisplayDifferencePercent=4, Title=""):

        self.Title = Title + " " if Title else ""
        self.ValueFrom = ValueFrom
        self.ValueTo = ValueTo
        if ValueFrom > ValueTo: # ValueFrom < ValueTo!!! if not, replace them to guarantee it.
            self.ValueFrom = ValueTo
            self.ValueTo = ValueFrom

        self.ValueRange = self.ValueTo - self.ValueFrom
        self.ValueNow = ValueNow
        self.BarLen = BarLen
        self.DisplayDifferencePercent = DisplayDifferencePercent
        self.Percent = 0
        self.PercentLastDisplayed = 0

        self.OneHundredPercentDisplayed = False
        print("") # to be sure that display starts from first char

    def update(self, Change=1, Msg="", Title=""):
        self.Title = Title + " " if Title else ""
        self.ValueNow += Change
        Progress = self.ValueNow - self.ValueFrom
        self.Percent = (Progress / self.ValueRange) * 100
        if self.Percent > 100: # with too high Change the caller can reach higher than 100%
            self.Percent = 100

        if not self.OneHundredPercentDisplayed: # Display the result only once
            if (self.Percent - self.PercentLastDisplayed > self.DisplayDifferencePercent) or self.Percent == 100:
                self.PercentLastDisplayed = self.Percent
                self.display(Msg=Msg)

            if self.Percent >= 100:
                self.OneHundredPercentDisplayed = True

    # here we simply display a given value instead of any inner calculation
    def display_percent(self, Percent):
        if Percent > 100: Percent = 100
        self.Percent = Percent
        self.display()

    def display(self, Msg=""):
        CharBack = AnsiControlInit + f"{111}D" # move back to the first column of line
        BarFilledLen = int((self.BarLen/100)*self.Percent)
        BarEmptyLen = self.BarLen - BarFilledLen
        BarFilled = "=" * BarFilledLen
        BarEmpty = "." * BarEmptyLen
        sys.stdout.write(f"{CharBack}{self.Title}[{BarFilled}{BarEmpty}] {int(self.Percent)}%")
        sys.stdout.flush()

        if self.Percent == 100:
            print("")  # leave the row of progress bar



