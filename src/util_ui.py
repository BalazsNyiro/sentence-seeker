# -*- coding: utf-8 -*-
import text, json

def sentence_get_from_result(Prg, Result, ReturnType="complete_sentence"):
    Source = Result["FileSourceBaseName"]
    LineNum = Result["LineNumInSentenceFile"]

    Sentence = text.sentence_loaded(Prg, Source, LineNum)
    Sentence = Sentence.strip() # remove possible newline at end

    Url = ""
    if Source in Prg["DocumentsDb"]:
        Url = Prg["DocumentsDb"][Source]["url"]

    if ReturnType == "separated_subsentences":
        SubSentenceNum = Result["SubSentenceNum"]
        SubSentences = text.subsentences(Sentence)

        SubSentenceResult = SubSentences[SubSentenceNum]
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
