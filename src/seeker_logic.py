# -*- coding: utf-8 -*-
import text, copy, time, util
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
def token_split(Query):

    Query = Query.replace(",", " ")

    for Operator in Operators:
        Query = Query.replace(Operator, f" {Operator} ")

    ########################################################################
    # every special word has : sign as a separator.
    # RULES:   From:what
    # example, long:  Englishlanguage:irregular_verbs_form_2  but I need to use small format:
    # example, applied   eng:iverb2, iverb3
    # but in real life we often  use From==eng so if : is starter, it means eng

    TokensWithSpecials = []
    for Token in Query.split(" "):
        if ":" in Token: # : means: special token
            if Token == ":iverb_ps": # past simple
                TokensWithSpecials.append("(")
                for FormPresentSimple in eng.IrregularVerbsPresentSimple:
                    TokensWithSpecials.append(FormPresentSimple)
                    TokensWithSpecials.append("OR")
                TokensWithSpecials.pop() # remove last OR,
                TokensWithSpecials.append(")")

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

def operators_exec(Tokens, Explains):

    for Operator in Operators:
        while Operator in Tokens:
            Tokens, ExplainsNew = operator_exec_left_right(Operator, Tokens, Explains)

            # keep original Explains pointer but insert the new result into it
            Explains.clear()
            Explains.extend(ExplainsNew)
            # print(" Results: ", Results)
            # print("Explains: ", ExplainsNew)

    return Tokens, Explains

# TESTED   Tokens is a list with Token elems
def token_interpreter(TokensOrig, DocIndex, Explains):
    TokensResults = []

    for Token in TokensOrig:

        if util.is_list(Token):
            Result = token_interpreter(Token, DocIndex, Explains)

        if is_operator(Token):
            Result = Token

        if is_str_but_not_operator(Token):
            IndexElems = index_list_to_set(Token, DocIndex)
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
    if isinstance(Token, str): # don't call, maybe it's faster
    #if util.is_str(Token): # if we got a string, then check in the Operators, else False
        return Token in Operators
    return False

# FIXME: INPROGRESS: test, operator_exec
def operator_exec_left_right(Operator, TokensOrig, ExplainsOrig):

    Explains = copy.deepcopy(ExplainsOrig)
    Tokens = copy.deepcopy(TokensOrig)
    IdOperator = Tokens.index(Operator)

    TokenRight, NameRight = Tokens.pop(IdOperator + 1) # remove right param
    Tokens.pop(IdOperator)  # remove the operator
    TokenLeft, NameLeft = Tokens[IdOperator - 1]

    if Operator == "OR":
        LineNumsOp = index_union(TokenLeft, TokenRight)
    else:
        LineNumsOp = index_intersect(TokenLeft, TokenRight)

    ResultName = f"({NameLeft} {Operator} {NameRight})"
    Tokens[IdOperator - 1] = (LineNumsOp, ResultName)

    Explains.append((ResultName, len(LineNumsOp)))
    return Tokens, Explains

def index_list_to_set(Word, DocIndex):
    # DocIndex is dict: {'word': array('I', [1, 5, 21])} and list of nums
    Result = set()
    if Word in DocIndex:
        for Position in DocIndex[Word]:
            Result.add(Position)
    return Result

def index_intersect(ResultLeft, ResultRight):
    return ResultLeft.intersection(ResultRight)

def index_union(ResultLeft, ResultRight):
    return ResultLeft.union(ResultRight)


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

def seek(Prg, Query, SentenceFillInResult=False, ExplainOnly=False, ResultSelectors=[resultSelectors]):
    Query = Query.strip()
    print(Query)
    util.log(Prg, f"Query: {Query}")

    Tokens = token_split(Query)
    WordsMaybeDetected = words_wanted_from_tokens(Tokens)

    print("group finder 1")
    TokenGroups = token_group_finder(Tokens)
    print("group finder 2")

    ResultsSelected = []
    TimeLogicStart = time.time()
    TokenProcessExplainPerDoc = dict()

    for FileSourceBaseName, DocObj in Prg["DocumentObjectsLoaded"].items():

        # use one file during development
        #if FileSourceBaseName != "LFrankBaum__WonderfulWizardOz__gutenberg_org_pg55":
        #    continue

        Explains = []
        print("TOKEN INTERPRETER >>>>", FileSourceBaseName)
        Results, _ResultName = token_interpreter(TokenGroups, DocObj["WordPosition"], Explains)
        print("TOKEN INTERPRETER <<<<")
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

    TimeLogicUsed = time.time() - TimeLogicStart
    # print("Time logic: ", TimeLogicUsed)
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

