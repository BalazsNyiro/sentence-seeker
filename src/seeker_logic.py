# -*- coding: utf-8 -*-
import text, util
import result_selectors
import time, tokens
import ui_console_progress_bar
from ui_color import *

def seek(Prg, Query, SentenceFillInResult=False, ExplainOnly=False, ResultSelectors=None):
    util.log(Prg, f"Query: {Query}")
    TextFromCommandResult = False
    DisplaySeekResultLater = True
    Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowOddOnly"] = False

    Location = "seeker_logic"
    Prg["UserInputHistory"].event_new(Location, "seek()", Query)

    ## don't give back any real text result in result viewer ##
    CommandDetected, MatchNums__ResultInfo, ResultDisplay, WordsDetectedCmd = tokens.run_commands_in_query(Prg, Query)
    if CommandDetected:
        TextFromCommandResult = True
        ExplainSumma = dict()
        if not ResultDisplay:
            print(color("Blue") + f"{Query}  executed" + color_reset())
        else:
            # if after a command basically we display anything without row coloring
            Prg["SettingsSaved"]["Ui"]["Console"]["ColorRowOddOnly"] = False

        return ExplainSumma, WordsDetectedCmd, MatchNums__ResultInfo, len(MatchNums__ResultInfo), ResultDisplay, TextFromCommandResult

    Query = Query.strip()
    print(Query)

    Tokens = tokens.token_split(Query, Prg=Prg)
    WordsDetected = set()
    TokenGroups = tokens.token_group_finder(Tokens)
    ResultsSelected = []
    TokenProcessExplainPerDoc = dict()

    TimeBigFor = time.time()
    TimeInterpreterSumma = 0

    SubSentenceMultiplier = Prg["SubSentenceMultiplier"]
    WordPositionMultiplier = Prg["WordPositionMultiplier"]

    Flattened = util.list_flat_embedded_lists(TokenGroups)
    NumOfTokens = len(Flattened) * len(Prg["DocumentObjectsLoaded"])
    ProgressBarConsole = ui_console_progress_bar.progress_bar_console(ValueTo=NumOfTokens)

    def TxtToObj(TokenTxtList, Index, FileSourceBaseName): # recursive txt-> TokenObj converter
        TokenObjects = []
        for Elem in TokenTxtList:
            if util.is_str(Elem):
                TokenObjects.append(tokens.TokenObj(Elem, Index, Prg=Prg, WordsDetected=WordsDetected, FileSourceBaseName=FileSourceBaseName))
            if util.is_list(Elem):
                TokenObjects.append(TxtToObj(Elem, Index, FileSourceBaseName))
        return TokenObjects

    if TokenGroups: # if user gave real input, not an Enter for example
        for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

            DocIndex = DocObj["WordPosition"]
            #TimeStart = time.time()
            Tokens = TxtToObj(TokenGroups, DocIndex, FileSourceBaseName)
            #print(">>> time end TxtToObj", time.time() - TimeStart)

            # if we haven't got any operator, then change==1.
            # if we have an operator, change = 1+(Op+1 in operator_exec) = 3.
            if ProgressBarConsole:
                ProgressBarConsole.update(Change=1)

            #TimeStart = time.time()
            tokens.operator_exec(Tokens, ProgressBarConsole=ProgressBarConsole, ProgressBarChange=2, Scope=Prg["SettingsSaved"]["Scope"])
            #print(">>> time end opExec  ", time.time() - TimeStart)
            #print()

            Results = Tokens[0].get_results()
            Explains = Tokens[0].explain()

            TokenProcessExplainPerDoc[FileSourceBaseName] = Explains

            if ExplainOnly: # no Results_Line_Subsen_Wordpos, only explain
                continue

            Results_Per_Sentence = dict()
            # Same sentence can be more than once in Results_Line_Subsen_Wordpos if you search more words.
            for LineNum__SubSentenceNum__WordNum in Results: # if we have any result from WordPosition:
                LineNum, SubSentenceNum, WordNum = \
                    text.linenum_subsentencenum_wordnum_get(LineNum__SubSentenceNum__WordNum, SubSentenceMultiplier, WordPositionMultiplier)

                if LineNum not in Results_Per_Sentence:

                    Obj = text.sentence_obj_from_memory(Prg,
                                                        FileSourceBaseName,
                                                        LineNum,
                                                        SubSentenceNum,
                                                        WordNum,
                                                        SentenceFillInResult)
                    Results_Per_Sentence[LineNum] = Obj
                else:
                    Obj = Results_Per_Sentence[LineNum]
                    Obj.subsentence_num_add(SubSentenceNum)
                    Obj.word_num_add(WordNum)

            for ResultObj in Results_Per_Sentence.values():
                ResultsSelected.append(ResultObj)

    # print("time interpreter summa", TimeInterpreterSumma)
    # print("\nbig for time", time.time() - TimeBigFor)

    TokenProcessExplainSumma = tokens.token_explain_summa(TokenProcessExplainPerDoc)

    #########################################################
    if not ResultSelectors:
        ResultSelectors = [
            # result_selectors.sort_by_relevance, # too big sentences can't fit on screen with this
            result_selectors.sort_by_sentence_len,
            result_selectors.remove_duplicated_sentences
        ]

    ResultsSelectedGroups = [ResultsSelected] # the selectors work with groups. At the beginning we have only one group.
    for ResultSelector in ResultSelectors:    # the last uniq selector flatten the groups into a single list
        ResultSelector(Prg, ResultsSelectedGroups, WordsDetected)
    ResultsSelected = util.list_flat_embedded_lists(ResultsSelectedGroups)
    #########################################################

    return TokenProcessExplainSumma, WordsDetected, ResultsSelected, len(ResultsSelected), DisplaySeekResultLater, TextFromCommandResult


