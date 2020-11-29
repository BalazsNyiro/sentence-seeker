# -*- coding: utf-8 -*-
import text, util
import result_selectors
import time, tokens
# ? MINUS,
# ? NOT

def seek(Prg, Query, SentenceFillInResult=False, ExplainOnly=False,
         ResultSelectors=[result_selectors.sortSentences]):
    util.log(Prg, f"Query: {Query}")

    CommandDetected = tokens.run_commands_in_query(Prg, Query)
    if CommandDetected:
        Query = "special_command_executed"
    Query = Query.strip()
    print(Query)

    #TimeTokenSplitStart = time.time()
    Tokens = tokens.token_split(Query, Prg=Prg)
    #print("token split time", time.time() - TimeTokenSplitStart)

    #TimeMaybeStart = time.time()
    WordsMaybeDetected = tokens.words_wanted_collect(Tokens)
    #print("maybe time", time.time() - TimeMaybeStart)

    #TimeGroups = time.time()
    TokenGroups = tokens.token_group_finder(Tokens)
    #print("groups time", time.time() - TimeGroups)

    ResultsSelected = []
    TokenProcessExplainPerDoc = dict()

    TimeBigFor = time.time()
    TimeInterpreterSumma = 0

    SubSentenceMultiplayer = Prg["SubSentenceMultiplayer"]

    for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

        # use one file during development
        #if FileSourceBaseName != "LFrankBaum__WonderfulWizardOz__gutenberg_org_pg55":
        #    continue

        Explains = []
        # print("TOKEN INTERPRETER >>>>", FileSourceBaseName)
        #TimeInterpreterStart = time.time()
        Results, _ResultName = tokens.token_interpreter(TokenGroups, DocObj["WordPosition"], Explains, TooManyTokenLimit=Prg["TooManyTokenLimit"])
        #TimeInterpreterSumma += time.time() - TimeInterpreterStart
        # print("TOKEN INTERPRETER <<<<", TimeInterpreter)

        TokenProcessExplainPerDoc[FileSourceBaseName] = Explains

        if ExplainOnly: # no Results, only explain
            continue

        for LineNum__SubSentenceNum in Results: # if we have any result from WordPosition:
            LineNum, SubSentenceNum = text.linenum_subsentencenum_get(LineNum__SubSentenceNum, SubSentenceMultiplayer)
            _Status, Obj = text.result_obj_from_memory(Prg,
                                                       FileSourceBaseName,
                                                       LineNum,
                                                       SubSentenceNum,
                                                       SentenceFillInResult=SentenceFillInResult)
            ResultsSelected.append(Obj)

    # print("time interpreter summa", TimeInterpreterSumma)
    print("big for time", time.time() - TimeBigFor)

    TokenProcessExplainSumma = tokens.token_explain_summa(TokenProcessExplainPerDoc)

    for ResultSelector in ResultSelectors:
        ResultsSelected = ResultSelector(Prg, ResultsSelected, WordsMaybeDetected)

    return TokenProcessExplainSumma, WordsMaybeDetected, ResultsSelected, len(ResultsSelected)


