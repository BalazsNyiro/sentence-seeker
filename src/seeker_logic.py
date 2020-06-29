# -*- coding: utf-8 -*-
import util, text, copy, time

# seek words are ALWAYS lowercase chars
Operators_Meaning = {"(": "set_create_new_begin",
                     ")": "set_create_new_end",
                     "AND": "set_intersect",
                     "OR": "set_union"
                     }
# ? MINUS,
# ? NOT

# TESTED
def words_wanted_from_tokens(Tokens):
    Words = [] # select only lowercase words from tokens
    for Token in Tokens:
        if Token[0] in util.ABC_Eng_Lower and Token[-1] in util.ABC_Eng_Lower:
            Words.append(Token)
    return Words

# TESTED
def token_split(Query):
    Query = Query.replace(",", " AND ")
    for Operator in Operators_Meaning.keys():
        Query = Query.replace(Operator, f" {Operator} ")

    Tokens = []   # insert AND if necessary:
    TokenPrev = ""
    for Token in Query.split(" "):
        if Token: # with multiple spaces a token can be "", too
            if TokenPrev:
                # two low char with one space between them - missing operator, AND is default
                if TokenPrev[-1] in util.ABC_Eng_Lower and Token[0] in util.ABC_Eng_Lower:
                    Tokens.append("AND")
            Tokens.append(Token)
            TokenPrev = Token
    return Tokens

def token_group_finder(Tokens):
    Group = []
    while Tokens:
        Token = Tokens.pop(0)
        if Token in Operators_Meaning:
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
def token_interpreter(Prg, Tokens, DocIndex, TokenProcessExplain, FirstRun=False):
    if FirstRun:
        Tokens = copy.deepcopy(Tokens) # we work with Tokens, and separate it from original Token Groups
    # print("\ninterpreter: ", Tokens)

    if isinstance(Tokens, list):
        # while operator in Tokens
        while "AND" in Tokens:
            operator_exec_left_right("AND", Prg, Tokens, DocIndex, index_intersect, TokenProcessExplain)

        while "OR" in Tokens:
            operator_exec_left_right("OR", Prg, Tokens, DocIndex, index_union, TokenProcessExplain)

        # ['birds']   simple word or dict stays at the end in the list
        if len(Tokens):
            return token_interpreter(Prg, Tokens[0], DocIndex, TokenProcessExplain)
        return {} # Tokens = ["(", ")"] without any elem, no token

    # at the end only one token can stay as result
    if isinstance(Tokens, str):
        LineNums = index_list_to_dict(Tokens, DocIndex)
        explain_add(Tokens, LineNums, TokenProcessExplain)
        return LineNums

    elif isinstance(Tokens, dict):
        return Tokens

def explain_add(WordOrToken, Result, TokenProcessExplain):
    TokenProcessExplain.append((WordOrToken, len(Result.keys())))

def operator_exec_left_right(Operator, Prg, Tokens, DocIndex, FunOperator, TokenProcessExplain):
    IdOperator = Tokens.index(Operator)

    TokenRight = Tokens.pop(IdOperator + 1)
    Tokens.pop(IdOperator)  # remove And
    TokenLeft = Tokens[IdOperator - 1]

    LineNumsLeft = token_interpreter(Prg, TokenLeft, DocIndex, TokenProcessExplain)
    TokenNameLeft = TokenProcessExplain[-1][0]

    LineNumsRight = token_interpreter(Prg, TokenRight, DocIndex, TokenProcessExplain)
    TokenNameRight = TokenProcessExplain[-1][0]

    LineNumsOp = FunOperator(LineNumsLeft, LineNumsRight)
    OperatorInfo = f"{TokenNameLeft} {Operator} {TokenNameRight}"
    explain_add(OperatorInfo, LineNumsOp, TokenProcessExplain)

    Tokens[IdOperator - 1] = LineNumsOp

def index_list_to_dict(Word, DocIndex):
    Result = dict()
    if Word in DocIndex:
        for Position in DocIndex[Word]:
            Result[Position] = True
    return Result

def index_intersect(ResultLeft, ResultRight):
    Result = dict()
    for Key in ResultLeft:
        if Key in ResultRight:
            Result[Key] = True
    return Result

def index_union(ResultLeft, ResultRight):
    Result = dict()
    for Key in ResultLeft:
        Result[Key] = True
    for Key in ResultRight:
        Result[Key] = True
    return Result




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
def seek(Prg, Query, SentenceFillInResult=False):
    Query = Query.strip()
    print(Query)
    Tokens = token_split(Query)
    WordsMaybeDetected = words_wanted_from_tokens(Tokens)

    TokenGroups = token_group_finder(Tokens)
    # print("Grp", TokenGroups)

    ResultsSelected = []
    TimeLogicStart = time.time()
    TokenProcessExplainPerDoc = dict()

    for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

        # use one file during development
        #if FileSourceBaseName != "LFrankBaum__WonderfulWizardOz__gutenberg_org_pg55":
        #    continue

        TokenProcessExplainOneDoc = []
        Results = token_interpreter(Prg, TokenGroups, DocObj["Index"], TokenProcessExplainOneDoc, FirstRun=True)
        TokenProcessExplainPerDoc[FileSourceBaseName] = TokenProcessExplainOneDoc

        for LineNum__SubSentenceNum in Results: # if we have any result from Index:
            LineNum, SubSentenceNum = text.linenum_subsentencenum_get(LineNum__SubSentenceNum)
            ResultsSelected.append(
                text.result_obj(Prg, FileSourceBaseName,
                                LineNum,
                                SubSentenceNum,
                                SentenceFillInResult=SentenceFillInResult
                )
            )
    TokenProcessExplainSumma = token_explain_summa(TokenProcessExplainPerDoc)
    # for Explain in TokenProcessExplainSumma:
    #     print("Summa exp:", Explain)

    TimeLogicUsed = time.time() - TimeLogicStart
    print("Time logic: ", TimeLogicUsed)
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

