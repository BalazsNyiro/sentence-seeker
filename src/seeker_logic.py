# -*- coding: utf-8 -*-
import text, util, util_ui
import result_selectors
import time, tokens
import ui_console_progress_bar
# ? MINUS,
# ? NOT

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

    #TimeTokenSplitStart = time.time()
    Tokens = tokens.token_split__group_words_collect(Query, Prg=Prg)
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

    SubSentenceMultiplier = Prg["SubSentenceMultiplier"]
    WordPositionMultiplier = Prg["WordPositionMultiplier"]

    Flattened = util.list_flat_embedded_lists(TokenGroups)
    NumOfOperators = len([T for T in Flattened if tokens.is_operator(T)]) * len(Prg["DocumentObjectsLoaded"])
    ProgressBarConsole = ui_console_progress_bar.progress_bar_console(ValueTo=NumOfOperators)

    for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

        # use one file during development
        #if FileSourceBaseName != "LFrankBaum__WonderfulWizardOz__gutenberg_org_pg55":
        #    continue

        Explains = []
        # print("TOKEN INTERPRETER >>>>", FileSourceBaseName)
        #TimeInterpreterStart = time.time()
        # print("TokenGroups: ", TokenGroups)
        # input("PRESS ENTER")
        Results_Line_Subsen_Wordpos, _ResultName = tokens.token_interpreter(
            TokenGroups, DocObj["WordPosition"], Explains, TooManyTokenLimit=Prg["TooManyTokenLimit"], ProgressBarConsole=ProgressBarConsole)

        #TimeInterpreterSumma += time.time() - TimeInterpreterStart
        # print("TOKEN INTERPRETER <<<<", TimeInterpreter)

        TokenProcessExplainPerDoc[FileSourceBaseName] = Explains

        if ExplainOnly: # no Results_Line_Subsen_Wordpos, only explain
            continue

        Results_Per_Sentence = dict()
        # Same sentence can be more than once in Results_Line_Subsen_Wordpos if you search more words.
        for LineNum__SubSentenceNum__WordNum in Results_Line_Subsen_Wordpos: # if we have any result from WordPosition:
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
    print("big for time", time.time() - TimeBigFor)

    TokenProcessExplainSumma = tokens.token_explain_summa(TokenProcessExplainPerDoc)

    for ResultSelector in ResultSelectors:
        ResultsSelected = ResultSelector(Prg, ResultsSelected, WordsMaybeDetected)

    return TokenProcessExplainSumma, WordsMaybeDetected, ResultsSelected, len(ResultsSelected)


