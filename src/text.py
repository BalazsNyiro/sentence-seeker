# -*- coding: utf-8 -*-
import re

SentenceEnds = ["...", "!?", "??", "…", "!", "?", "."]

# Tested with abbreviations,
# FromToPairsExample = [("Mr.", "Mr")]
def replace(Txt, FromToPairs):
    for Old, New in FromToPairs:
        Txt = Txt.replace(Old, New)
    return Txt

# Tested
def replace_spaces_to_one_space(Text):
    Pattern = re.compile(r'[ ]+')
    return replace_regexp(Text, Pattern, " ")

# Tested
def replace_regexp(Text, Pattern, TextNew):
    P = re.compile(Pattern)
    return P.sub(TextNew, Text)

# Tested
def html_tags_remove(Src, TextNew=""):
    Pattern = r'<.*?>'
    return replace_regexp(Src, Pattern, TextNew)

# Tested
def replace_abbreviations(Txt):
    ReplaceAbbreviations = [("Mr.", "Mr"),
                            ("Mrs.", "Mrs"),
                            ("Ms.", "Ms")]
    return replace(Txt, ReplaceAbbreviations)

