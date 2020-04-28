# -*- coding: utf-8 -*-
import re

SentenceEnds = [".", "!", "?", "…"]
AbcEngUpper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MarksQuotation = '"“”'

# Tested
_PatternNotAbc = re.compile(r'[^a-zA-Z]')
def remove_not_abc_chars(Text, TextNew=""):
    return replace_regexp(Text, _PatternNotAbc, TextNew)

# Tested with abbreviations,
# FromToPairsExample = [("Mr.", "Mr")]
def replace(Txt, FromToPairs):
    for Old, New in FromToPairs:
        Txt = Txt.replace(Old, New)
    return Txt

_PatternWhitespaces = re.compile(r'\s+')
# Tested
def replace_whitespaces_to_one_space(Text):
    return replace_regexp(Text, _PatternWhitespaces, " ")

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

