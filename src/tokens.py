import eng, util, text
# python has token module so i use tokens here.

Operators = {"AND", "OR", "(", ")"}

# ..pattern..  -> in:pattern
import util_json_obj
import util_ui

def quick_form_convert_to_special_form(Token, Sign):
    LenSign = len(Sign)
    if Sign in Token:
        StarPrefix = Token.startswith(Sign)
        StarPostfix = Token.endswith(Sign)
        if StarPrefix and StarPostfix: Token = "in:" + Token[LenSign:-LenSign]
        if StarPrefix and not StarPostfix: Token = "start:" + Token[LenSign:]
        if not StarPrefix and StarPostfix: Token = "end:" + Token[:-LenSign]
    return Token

########################################################################
def group_words_collect(Prg, Query):
    TokensWithGroups = []
    def word_group_into_tokens(Group):
        TokensWithGroups.extend(word_group_collect(Group))

    # every special word has : sign as a separator.
    for Token in Query.split(" "):
        Sign = ".."
        Token = quick_form_convert_to_special_form(Token, "*")
        Token = quick_form_convert_to_special_form(Token, "..")
        if ":" in Token:  # : means: special token

            if Token == "iverb:ps":  # irregular verbs, past simple selector
                word_group_into_tokens(eng.IrregularVerbsPresentSimple)

            elif Token == "iverb:pp":  # irregular verbs, past participle selector
                word_group_into_tokens(eng.IrregularVerbsPastParticiple)

            elif Token == "iverb:inf":  # irregular verbs, past participle selector
                word_group_into_tokens(eng.IrregularVerbsInfinitive)

            elif Token.startswith("end:"):
                End = Token.split(":")[1]
                word_group_into_tokens(eng.groups_of_word_ending(Prg, End))

            elif Token.startswith("start:"):
                Start = Token.split(":")[1]
                word_group_into_tokens(eng.groups_of_word_starting(Prg, Start))

            elif Token.startswith("in:"):
                In = Token.split(":")[1]
                word_group_into_tokens(eng.groups_of_word_include(Prg, In))

            else:
                print("unknown special group selector:", Query)

        else:
            TokensWithGroups.append(Token)
    return TokensWithGroups
    ########################################################################

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

    return CommandDetected

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
def operators_exec(Tokens, Explains, TooManyTokenLimit=300):
    OperatorPositions = {}
    for Operator in Operators:
        OperatorPositions[Operator] = []

    for Position, Token in enumerate(Tokens):
        if is_operator(Token):
            OperatorPositions[Token].append(Position)

    TooManyTokens = len(Tokens) >= TooManyTokenLimit

    for Operator in Operators:

        while OperatorPositions[Operator]:
            OperatorPositionLast = OperatorPositions[Operator].pop()

            TokenLeft, NameLeft = Tokens[OperatorPositionLast - 1]
            TokenRight, NameRight = Tokens[OperatorPositionLast + 1]

            if Operator == "OR":
                LineNumsOp = TokenLeft.union(TokenRight)
            else:
                LineNumsOp = TokenLeft.intersection(TokenRight)

            # the string creation/concatenation is too slow if you use thousands of tokens
            if TooManyTokens: # no explain, no detailed/explained token info
                Tokens[OperatorPositionLast-1] = (LineNumsOp, "")
                Tokens.pop(OperatorPositionLast + 1)
                Tokens.pop(OperatorPositionLast)
            else:
                ResultName = f"({NameLeft} {Operator} {NameRight})"

                Tokens[OperatorPositionLast-1] = (LineNumsOp, ResultName)
                Tokens.pop(OperatorPositionLast + 1)
                Tokens.pop(OperatorPositionLast)

                Explains.append((ResultName, len(LineNumsOp)))

    return Tokens, Explains

# Tested
def is_str_but_not_operator(Token): # Token can be List or Operator
    return (util.is_str(Token) and not is_operator(Token))

# Tested
def is_operator(Token):
    if util.is_str(Token): # if we got a string, then check in the Operators, else False
        return Token in Operators
    return False

# TESTED
# FIXME: TEST WITH PRG PARAM
def token_split(Query, Prg=dict()):

    Query = Query.replace(",", " ")

    for Operator in Operators:
        # example query:  (apple,orange) OR (banana,kiwi)
        # insert space around parenthesis
        Query = Query.replace(Operator, f" {Operator} ")

    ########################################################################
    TokensWithGroups = group_words_collect(Prg, Query)

    Tokens = []   # insert AND if necessary:
    TokenPrev = ""
    for Token in TokensWithGroups:
        if Token: # with multiple spaces a token can be "", too
            if TokenPrev:
                # two low char with one space between them - missing operator, AND is default
                if (TokenPrev == ")" or text.word_wanted(TokenPrev)) \
                        and (text.word_wanted(Token) or Token == "("):
                    Tokens.append("AND")

            Tokens.append(Token)
            TokenPrev = Token
    return Tokens

# TESTED
def words_wanted_collect(Tokens):
    Words = set() # select only lowercase words from tokens
    for Token in Tokens:
        if text.word_wanted(Token):
            Words.add(Token)
    return Words

def token_explain_summa(TokenProcessExplainPerDoc):
    TokenProcessExplainSumma = dict()
    for Source, Explains in TokenProcessExplainPerDoc.items():
        for Explain in Explains:
            Token, ResultsNumNow = Explain
            util.dict_key_insert_if_necessary(TokenProcessExplainSumma, Token, 0)
            TokenProcessExplainSumma[Token] += ResultsNumNow

    return TokenProcessExplainSumma

#################################################################################
_EmptySet = set()
# TESTED   Tokens is a list with Token elems
def token_interpreter(TokensOrig, DocIndex, Explains, TooManyTokenLimit=300): # Explains type: list()
    TokensResults = []

    TooManyTokens = len(TokensOrig) >= TooManyTokenLimit

    for Token in TokensOrig:

        if util.is_str(Token):

            if is_operator(Token):
                TokensResults.append(Token)

            else: # str but not operator
                # DocIndex is dict: {'word': array('I', [1, 5, 21])} and list of nums
                # IndexElems has to be set, because later we use Union, Intersect operators on these results
                IndexElems = set(DocIndex.get(Token, _EmptySet))

                if TooManyTokens: # SPEED UP: REMOVE NOT IMPORTANT OPERATOR:

                    if TokensResults and (not IndexElems) and TokensResults[-1] == "OR":
                        # remove Last "OR", because:
                        # ELEMS OR NOTHING -> ELEMS, you can remove 'OR NOTHING'
                        TokensResults.pop()
                    else:
                        # HERE we don't append Explain: no Explains.append()
                        Result = (IndexElems, Token)
                        TokensResults.append(Result)  # ResultLineNums, TokenName

                else: # not Too Many Tokens, normal/base process
                    Explains.append((Token, len(IndexElems)))
                    Result = (IndexElems, Token)
                    TokensResults.append(Result) # ResultLineNums, TokenName

        elif util.is_list(Token):
            Result = token_interpreter(Token, DocIndex, Explains, TooManyTokenLimit=TooManyTokenLimit)
            TokensResults.append(Result)

    TokensResults, Explains = operators_exec(TokensResults, Explains, TooManyTokenLimit=TooManyTokenLimit)

    if TokensResults:
        TokenFirst = TokensResults[0]
        ResultLineNums = TokenFirst[0]
        ResultExplains = TokenFirst[1]
    else:
        ResultLineNums = {}
        ResultExplains = "(empty_group)"  # empty group, example: "()"

    return (ResultLineNums, ResultExplains)
