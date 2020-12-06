# -*- coding: utf-8 -*-
import text, util
import result_selectors
import time, tokens
import ui_console_progress_bar

def seek(Prg, Query, SentenceFillInResult=False, ExplainOnly=False,
         ResultSelectors=[
             result_selectors.short_sorter,
             result_selectors.uniq_filter
             ]):
    util.log(Prg, f"Query: {Query}")

    CommandDetected = tokens.run_commands_in_query(Prg, Query)
    if CommandDetected:
        Query = "special_command_executed"
    Query = Query.strip()
    print(Query)

    Tokens = tokens.token_split(Query, Prg=Prg)
    WordsMaybeDetected = set()
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

    def TxtToObj(TokenTxtList, Index): # recursive txt-> TokenObj converter
        TokenObjects = []
        for Elem in TokenTxtList:
            if util.is_str(Elem):
                TokenObjects.append(tokens.TokenObj(Elem, Index, Prg=Prg, WordsMaybeDetected=WordsMaybeDetected))
            if util.is_list(Elem):
                TokenObjects.append(TxtToObj(Elem, Index))
        return TokenObjects

    if TokenGroups: # if user gave real input, not an Enter for example
        for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

            DocIndex = DocObj["WordPosition"]
            #TimeStart = time.time()
            Tokens = TxtToObj(TokenGroups, DocIndex)
            #print(">>> time end TxtToObj", time.time() - TimeStart)

            #TimeStart = time.time()
            tokens.operator_exec(Tokens, ProgressBarConsole=ProgressBarConsole)
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

    for ResultSelector in ResultSelectors:
        ResultsSelected = ResultSelector(Prg, ResultsSelected, WordsMaybeDetected)

    return TokenProcessExplainSumma, WordsMaybeDetected, ResultsSelected, len(ResultsSelected)


