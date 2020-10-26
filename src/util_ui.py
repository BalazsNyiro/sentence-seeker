# -*- coding: utf-8 -*-
import text, json

def sentence_get_from_result(Prg, Result, ReturnType="complete_sentence"):
    Source = Result["FileSourceBaseName"]
    LineNum = Result["LineNumInSentenceFile"]

    _Status, Sentence = text.sentence_from_memory(Prg, Source, LineNum, Strip=True)

    Url = ""
    if Source in Prg["DocumentsSourceWebpages"]:
        Url = Prg["DocumentsSourceWebpages"][Source]["url"]

    if ReturnType == "separated_subsentences":
        SubSentenceNum = Result["SubSentenceNum"]
        _Status, SubSentenceResult = text.subsentences(Prg, Sentence, SubSentenceNum)
        SubSentencesBefore, SubSentencesAfter = Sentence.split(SubSentenceResult)

        Sentence = {"subsentences_before": SubSentencesBefore,
                    "subsentence_result": SubSentenceResult,
                    "subsentences_after": SubSentencesAfter
                    }

    return Url, Sentence, Source

def theme_actual(Prg):
    ThemeActual = Prg["UiThemes"]["ThemeNameActual"]
    Theme = Prg["UiThemes"][ThemeActual]
    return Theme

def ui_json_answer(Prg, MatchNums__ResultInfo, TokenProcessExplainSumma, NewLine="\n"):
    Txt = token_explain_summa_to_text(TokenProcessExplainSumma, NewLine=NewLine) + 2*NewLine
    Reply = {"results": MatchNums__ResultInfo[:Prg["LimitDisplayedSampleSentences"]],
             "token_process_explain": Txt}
    Reply = json.dumps(Reply).encode('UTF-8')
    return Reply

def token_explain_summa_to_text(TokenProcessExplainSumma, NewLine="\n"):
    TokenExplainText = []

    for Exp in TokenProcessExplainSumma:
        Token, ResultNum = Exp
        TokenExplainText.append(f"{Token}: {ResultNum}")

    return NewLine.join(TokenExplainText)

def title(Prg):
    return f"sentence-seeker: {Prg['DirDocuments']}"