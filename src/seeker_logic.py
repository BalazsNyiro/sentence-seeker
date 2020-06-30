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

# TESTED
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



# TESTED   Tokens is a list with Token elems
def token_interpreter(Tokens, DocIndex):

    Results = []

    for Token in Tokens:

        if is_list(Token):
            Result = token_interpreter(Token, DocIndex)

        if operator(Token):
            Result = Token

        if is_str_but_not_operator(Token):
            Result = index_list_to_dict(Token, DocIndex)

        Results.append(Result)

    for Operator, Fun in Operator_Functions:
        while Operator in Results:
            Results = operator_exec_left_right(Operator, Results, Fun)

    if Results:
        return Results[0]
    return {}  # empty group, example: "()"



def is_str_but_not_operator(Token):
    return (is_str(Token) and not operator(Token))

def operator(Token):
    if is_str(Token): # if we got a string, then check in the Operators, else False
        return Token in Operators_Meaning
    return False

def is_list(Obj):
    return isinstance(Obj, list)

def is_str(Obj):
    return isinstance(Obj, str)

def is_dict(Obj):
    return isinstance(Obj, dict)

def is_tuple(Obj):
    return isinstance(Obj, tuple)

def operator_exec_left_right(Operator, TokensOrig, FunOperator):
    Tokens = copy.deepcopy(TokensOrig)
    IdOperator = Tokens.index(Operator)

    TokenRight = Tokens.pop(IdOperator + 1) # remove right param
    Tokens.pop(IdOperator)  # remove the operator
    TokenLeft = Tokens[IdOperator - 1]

    LineNumsOp = FunOperator(TokenLeft, TokenRight)
    Tokens[IdOperator - 1] = LineNumsOp
    return Tokens

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

Operator_Functions = (("AND", index_intersect), ("OR", index_union))



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

        Results = token_interpreter(TokenGroups, DocObj["Index"])
        # TokenProcessExplainPerDoc[FileSourceBaseName] = TokenProcessExplainOneDoc

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

