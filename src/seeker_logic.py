# -*- coding: utf-8 -*-
import text, util, util_ui, util_json_obj
import eng

# ? MINUS,
# ? NOT

# TESTED
def words_wanted_from_tokens(Tokens):
    Words = [] # select only lowercase words from tokens
    for Token in Tokens:
        if text.word_wanted(Token):
            Words.append(Token)
    return Words

# TESTED
def word_group_collect(Words):
    TokensWithSpecials = []
    TokensWithSpecials.append("(")

    for Word in Words:
        TokensWithSpecials.append(Word)
        TokensWithSpecials.append("OR")

    TokensWithSpecials.pop()  # remove last OR,
    TokensWithSpecials.append(")")
    return TokensWithSpecials

# TESTED
def token_split(Query):

    Query = Query.replace(",", " ")

    for Operator in Operators:
        Query = Query.replace(Operator, f" {Operator} ")

    ########################################################################
    # every special word has : sign as a separator.
    TokensWithSpecials = []
    for Token in Query.split(" "):
        if ":" in Token: # : means: special token

            if Token == ":iverbPs": # irregular verbs, past simple selector
                TokensWithSpecials.extend(word_group_collect(eng.IrregularVerbsPresentSimple))

            if Token == ":iverbPp": # irregular verbs, past participle selector
                TokensWithSpecials.extend(word_group_collect(eng.IrregularVerbsPastParticiple))

            if Token == ":iverbInf": # irregular verbs, past participle selector
                TokensWithSpecials.extend(word_group_collect(eng.IrregularVerbsInfinitive))

        else:
            TokensWithSpecials.append(Token)
    ########################################################################

    Tokens = []   # insert AND if necessary:
    TokenPrev = ""
    for Token in TokensWithSpecials:
    #for Token in Query.split(" "):
        if Token: # with multiple spaces a token can be "", too
            if TokenPrev:
                # two low char with one space between them - missing operator, AND is default
                if   (TokenPrev == ")" or text.word_wanted(TokenPrev)) \
                 and (text.word_wanted(Token) or Token == "("):
                    Tokens.append("AND")

            Tokens.append(Token)
            TokenPrev = Token
    return Tokens

# TESTED
def token_group_finder(Tokens):
    Group = []
    while Tokens:
        Token = Tokens.pop(0)
        if Token in Operators:
            if Token == "(":
                SubGroup = token_group_finder(Tokens)
                Group.append(SubGroup)
            elif Token == ")":
                break
            else:
                Group.append(Token) # AND OR
        else:
            Group.append(Token)

    return Group

# PRECEDENCE: 
#  NOT
#  AND
#  OR

#                  Tokens: list()
def operators_exec(Tokens, Explains):

    for Operator in Operators:
        while Operator in Tokens:
            Tokens = operator_exec_left_right(Operator, Tokens, Explains)

            # keep original Explains pointer but insert the new result into it

            # Explains.clear()
            # Explains.extend(ExplainsNew)

            # print(" Results: ", Results)
            # print("Explains: ", ExplainsNew)

    return Tokens, Explains


_EmptySet = set()
# TESTED   Tokens is a list with Token elems
def token_interpreter(TokensOrig, DocIndex, Explains): # Explains type: list()
    TokensResults = []

    for Token in TokensOrig:

        if util.is_list(Token):
            Result = token_interpreter(Token, DocIndex, Explains)

        elif is_operator(Token):
            Result = Token

        elif is_str_but_not_operator(Token):

            if Token in DocIndex:
                # DocIndex is dict: {'word': array('I', [1, 5, 21])} and list of nums
                IndexElems = set(DocIndex[Token])
            else:
                IndexElems = _EmptySet

            Result = (IndexElems, Token) # ResultLineNums, TokenName
            Explains.append((Token, len(IndexElems)))

        TokensResults.append(Result)

    TokensResults, Explains = operators_exec(TokensResults, Explains)

    if TokensResults:
        TokenFirst = TokensResults[0]
        ResultLineNums = TokenFirst[0]
        ResultExplains = TokenFirst[1]
    else:
        ResultLineNums = {}
        ResultExplains = "(empty_group)"  # empty group, example: "()"

    return (ResultLineNums, ResultExplains)

# Tested
def is_str_but_not_operator(Token): # Token can be List or Operator
    return (util.is_str(Token) and not is_operator(Token))

# Tested
def is_operator(Token):
    if util.is_str(Token): # if we got a string, then check in the Operators, else False
        return Token in Operators
    return False

# FIXME: INPROGRESS: test, operator_exec
#                                  TokensOrig: list()  ExplainsOrig: list
def operator_exec_left_right(Operator, TokensOrig, Explains):

    IdOperator = TokensOrig.index(Operator)

    TokenRight, NameRight = TokensOrig[IdOperator + 1]
    TokenLeft, NameLeft = TokensOrig[IdOperator - 1]

    if Operator == "OR":
        LineNumsOp = TokenLeft.union(TokenRight)
    else:
        LineNumsOp = TokenLeft.intersection(TokenRight)

    ResultName = f"({NameLeft} {Operator} {NameRight})"

    Tokens = TokensOrig[:IdOperator - 1]
    Tokens.append( (LineNumsOp, ResultName) )
    Tokens.extend( TokensOrig[IdOperator + 2:] )  # Right Token was IdOperator+1, attach from the next one

    Explains.append((ResultName, len(LineNumsOp)))
    return Tokens

Operators = {"AND", "OR", "(", ")"}


# ResultsSelected = []
# Selectors = [result_selectors.shorters_are_better,
#              result_selectors.duplication_removing]

# for MatchNum in MatchNums__Descending:

#     # PLUGIN ATTACH POINT
#     # - if it's possible keep the search word order?
#     # - the words distance (shorter is better)

#     ResultsGroup = GroupsSubsentenceBased_MatchNums_ResultInfos[MatchNum]
#     for Selector in Selectors:
#         ResultsGroup = Selector(ResultsGroup)
#     ResultsSelected.extend(ResultsGroup)
# TODO: result_selectors.py??

# receive results, give back results
# example Result Selector, Proof of concept
# FIXME: distances of wanted words are CRUCIAL
# tested in test_result_selectors
def resultSelectors(ResultsOrig, WordsMaybeDetected, SortBy=["SubSentenceLen", "SentenceLen"]):
    if not SortBy:
        return ResultsOrig

    ResultNew = []
    Groups = {}
    SortKey = SortBy[0]

    for Result in ResultsOrig:
        Score = Result[SortKey]
        util.dict_value_insert_into_key_group(Groups, Score, Result)

    for Score in sorted(Groups.keys()):
        # print(f"\nScore {Score} {SortKey}")
        ResultNew.extend(resultSelectors(Groups[Score], WordsMaybeDetected, SortBy[1:]))

    return ResultNew

def run_commands_in_query(Prg, Query):
    # it's not a problem if these commands stay in Query,
    # The token processor skips them
    CommandDetected = False

    if ":help" in Query:
        print("\n\n" + Prg["UsageInfo"] + "\n")
        CommandDetected = True

    if ":dirDocInGuiTitleOff" in Query:
        Prg["SettingsSaved"]["Ui"]["DisplayDirDocInGuiTitle"] = False
        util_ui.title_refresh(Prg)
        CommandDetected = True

    if ":dirDocInGuiTitleOn" in Query:
        Prg["SettingsSaved"]["Ui"]["DisplayDirDocInGuiTitle"] = True
        util_ui.title_refresh(Prg)
        CommandDetected = True

    if ":urlOff" in Query:
        Prg["SettingsSaved"]["Ui"]["DisplaySourceUrlBelowSentences"] = False
        CommandDetected = True

    if ":urlOn" in Query:
        Prg["SettingsSaved"]["Ui"]["DisplaySourceUrlBelowSentences"] = True
        CommandDetected = True

    if ":sourceOff" in Query:
        Prg["SettingsSaved"]["Ui"]["DisplaySourceFileNameBelowSentences"] = False
        CommandDetected = True

    if ":sourceOn" in Query:
        Prg["SettingsSaved"]["Ui"]["DisplaySourceFileNameBelowSentences"] = True
        CommandDetected = True

    if CommandDetected:
        util_json_obj.config_set(Prg, "SettingsSaved")
    else:
        print("Unknown command in Query>", Query)


def seek(Prg, Query, SentenceFillInResult=False, ExplainOnly=False, ResultSelectors=[resultSelectors]):
    Query = Query.strip()
    print(Query)
    util.log(Prg, f"Query: {Query}")

    run_commands_in_query(Prg, Query)

    Tokens = token_split(Query)
    WordsMaybeDetected = words_wanted_from_tokens(Tokens)

    TokenGroups = token_group_finder(Tokens)

    ResultsSelected = []
    TokenProcessExplainPerDoc = dict()

    TimeInterpreterSumma = 0

    for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

        # use one file during development
        #if FileSourceBaseName != "LFrankBaum__WonderfulWizardOz__gutenberg_org_pg55":
        #    continue

        Explains = []
        # print("TOKEN INTERPRETER >>>>", FileSourceBaseName)
        # TimeInterpreterStart = time.time()
        Results, _ResultName = token_interpreter(TokenGroups, DocObj["WordPosition"], Explains)
        # TimeInterpreter = time.time() - TimeInterpreterStart
        # TimeInterpreterSumma += TimeInterpreter
        # print("TOKEN INTERPRETER <<<<", TimeInterpreter)

        TokenProcessExplainPerDoc[FileSourceBaseName] = Explains

        if ExplainOnly: # no Results, only explain
            continue

        for LineNum__SubSentenceNum in Results: # if we have any result from WordPosition:
            LineNum, SubSentenceNum = text.linenum_subsentencenum_get(LineNum__SubSentenceNum, Prg["SubSentenceMultiplayer"])
            _Status, Obj = text.result_obj_from_memory(Prg, FileSourceBaseName,
                                                                LineNum,
                                                                SubSentenceNum,
                                                                SentenceFillInResult=SentenceFillInResult
                                                               )
            ResultsSelected.append(Obj)

    TokenProcessExplainSumma = token_explain_summa(TokenProcessExplainPerDoc)

    for ResultSelector in ResultSelectors:
        ResultsSelected = ResultSelector(ResultsSelected, WordsMaybeDetected)

    # print("Time interpreter summa", TimeInterpreterSumma)
    return TokenProcessExplainSumma, WordsMaybeDetected, ResultsSelected, len(ResultsSelected)

def token_explain_summa(TokenProcessExplainPerDoc):
    TokenProcessExplainSumma = []

    for Source, Explains in TokenProcessExplainPerDoc.items():
        if not TokenProcessExplainSumma:
            for Explain in Explains:
                TokenProcessExplainSumma.append(Explain)
        else:
            for Id, Explain in enumerate(Explains):
                Token, ResultsNumNow = Explain
                _, ResultsSumma = TokenProcessExplainSumma[Id]
                TokenProcessExplainSumma[Id] = (Token, ResultsSumma + ResultsNumNow)

        # print("exp:", Source, Explain)

    return TokenProcessExplainSumma

