# -*- coding: utf-8 -*-
import text, util, util_ui, util_json_obj
import eng, result_selectors
import time
# ? MINUS,
# ? NOT

# TESTED
def words_wanted_from_tokens(Tokens):
    Words = set() # select only lowercase words from tokens
    for Token in Tokens:
        if text.word_wanted(Token):
            Words.add(Token)
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
# FIXME: TEST WITH PRG PARAM
TokensSpecial = set([":iverbPs", ":iverbInf", ":iverbPp", "end:", "start:"])
def token_split(Query, Prg=dict()):

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

            if Token.startswith("end:"):
                End = Token.split(":")[1]
                TokensWithSpecials.extend(word_group_collect(eng.groups_of_word_ending(Prg, End)))

            if Token.startswith("start:"):
                Start = Token.split(":")[1]
                TokensWithSpecials.extend(word_group_collect(eng.groups_of_word_starting(Prg, Start)))

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
    OperatorPositions = {}
    for Operator in Operators:
        OperatorPositions[Operator] = []

    for Position, Token in enumerate(Tokens):
        if is_operator(Token):
            OperatorPositions[Token].append(Position)

    for Operator in Operators:
        while OperatorPositions[Operator]:
            OperatorPositionLast = OperatorPositions[Operator].pop()
            operator_exec_left_right(Operator, Tokens, Explains, OperatorPositionLast)

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

    TimeFor = time.time()
    for Token in TokensOrig:

        if util.is_str(Token):

            if is_operator(Token):
                Result = Token

            else: # str but not operator
                # DocIndex is dict: {'word': array('I', [1, 5, 21])} and list of nums
                # IndexElems has to be set, because later we use Union, Intersect operators on these results
                IndexElems = set(DocIndex.get(Token, _EmptySet))
                Explains.append((Token, len(IndexElems)))
                Result = (IndexElems, Token)  # ResultLineNums, TokenName

        elif util.is_list(Token):
            Result = token_interpreter(Token, DocIndex, Explains)

        TokensResults.append(Result)

    TimeDelta= time.time() - TimeFor
    print(">> Token, time for", TimeDelta)
    if TimeDelta > 0.3:
        pass
        #print(TokensOrig)

    TimeExec = time.time()
    TokensResults, Explains = operators_exec(TokensResults, Explains)
    TimeDelta= time.time() - TimeExec
    print(">> operator exec", TimeDelta)

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
#                                  Tokens: list()  Explains: list
def operator_exec_left_right(Operator, Tokens, Explains, IdOperator):

    TokenLeft, NameLeft = Tokens[IdOperator - 1]
    TokenRight, NameRight = Tokens[IdOperator + 1]

    if Operator == "OR":
        LineNumsOp = TokenLeft.union(TokenRight)
    else:
        LineNumsOp = TokenLeft.intersection(TokenRight)

    ResultName = f"({NameLeft} {Operator} {NameRight})"

    Tokens[IdOperator-1] = (LineNumsOp, ResultName)
    Tokens.pop(IdOperator + 1)
    Tokens.pop(IdOperator)

    Explains.append((ResultName, len(LineNumsOp)))

Operators = {"AND", "OR", "(", ")"}

def run_commands_in_query(Prg, Query):
    # it's not a problem if these commands stay in Query,
    # The token processor skips them
    CommandDetected = False

    if ":" in Query:

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
           print(": detected but not command in Query>", Query)


def seek(Prg, Query, SentenceFillInResult=False, ExplainOnly=False,
         ResultSelectors=[result_selectors.sortSentences]):
    Query = Query.strip()
    print(Query)
    util.log(Prg, f"Query: {Query}")

    run_commands_in_query(Prg, Query)

    TimeTokenSplitStart = time.time()
    Tokens = token_split(Query, Prg=Prg)
    print("token split time", time.time() - TimeTokenSplitStart)

    TimeMaybeStart = time.time()
    WordsMaybeDetected = words_wanted_from_tokens(Tokens)
    print("maybe time", time.time() - TimeMaybeStart)

    TimeGroups = time.time()
    TokenGroups = token_group_finder(Tokens)
    print("groups time", time.time() - TimeGroups)

    ResultsSelected = []
    TokenProcessExplainPerDoc = dict()

    TimeBigFor  = time.time()
    TimeInterpreterSumma = 0
    for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

        # use one file during development
        #if FileSourceBaseName != "LFrankBaum__WonderfulWizardOz__gutenberg_org_pg55":
        #    continue

        Explains = []
        # print("TOKEN INTERPRETER >>>>", FileSourceBaseName)
        TimeInterpreterStart = time.time()
        Results, _ResultName = token_interpreter(TokenGroups, DocObj["WordPosition"], Explains)
        TimeInterpreterSumma += time.time() - TimeInterpreterStart
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

    print("time interpreter summa", TimeInterpreterSumma)
    print("big for time", time.time() - TimeBigFor)


    TokenProcessExplainSumma = token_explain_summa(TokenProcessExplainPerDoc)

    for ResultSelector in ResultSelectors:
        ResultsSelected = ResultSelector(Prg, ResultsSelected, WordsMaybeDetected)

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

