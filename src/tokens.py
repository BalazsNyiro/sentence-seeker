import eng, util, text
# python has token module so i use tokens here.

Operators = {"AND", "OR", "(", ")", "THEN"}

# ..pattern..  -> in:pattern
import util_json_obj
import util_ui

########################################################################

def run_commands_in_query(Prg, Query):
    # it's not a problem if these commands stay in Query,
    # The token processor skips them
    CommandDetected = False

    if ":" in Query:

        if ":help_plain" in Query:
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


# create intersection WHEN the order if from left to right
def exec_THEN_operator(PositionsLeftScoped, PositionsRightScoped,
                       PositionsLeft,       PositionsRight,
                       SubSentenceMulti,    WordPositionMulti, Scope):

    if not PositionsLeft: return set()
    if not PositionsRight: return set()

    Intersect = PositionsLeftScoped.intersection(PositionsRightScoped)
    if not Intersect: return set()

    # scopes that appear on both side, selected with intersection
    PositionsPairedScoped = dict()
    for Pos in Intersect:
        PositionsPairedScoped[Pos] = {"ExactsLeft": set(), "ExactsRight": set()}

    #### collect exact positions into scopes ##############
    for PositionExact in PositionsLeft:
        _, Scoped = result_scope_modify(PositionExact, SubSentenceMulti, WordPositionMulti, Scope)
        if Scoped in PositionsPairedScoped:
            PositionsPairedScoped[Scoped]["ExactsLeft"].add(PositionExact)

    for PositionExact in PositionsRight:
        _, Scoped = result_scope_modify(PositionExact, SubSentenceMulti, WordPositionMulti, Scope)
        if Scoped in PositionsPairedScoped:
            PositionsPairedScoped[Scoped]["ExactsRight"].add(PositionExact)

    ######## select where the order is acceptable: ##########

    PositionsOrdered = set()
    for PosScope, Exacts in PositionsPairedScoped.items():
        Accepted = False
        for ExactLeft in Exacts["ExactsLeft"]:

            if Scope == "sentence":
                for ExactRight in Exacts["ExactsRight"]:
                    if ExactLeft < ExactRight:
                        Accepted = True
                        break
                if Accepted:
                    break
            elif Scope == "subsentence":
                for ExactRight in Exacts["ExactsRight"]:
                    if subsentence_same(ExactLeft, ExactRight, WordPositionMulti):
                        if ExactLeft < ExactRight:
                            Accepted = True
                            break
                if Accepted:
                    break
        if Accepted:
            PositionsOrdered.add(PosScope)
    return PositionsOrdered

def subsentence_same(PosExactLeft, PosExactRight, WordPositionMulti):
    return (PosExactLeft // WordPositionMulti) == (PosExactRight // WordPositionMulti)

# Tested
def is_operator(Token):
    if util.is_str(Token): # if we got a string, then check in the Operators, else False
        return Token in Operators
    return False

# TESTED
def token_split(Query, Prg=dict()):

    Replaces = (
        (",", " "),
        (">", " THEN ")
    )
    Query = text.replace_pairs(Query, Replaces)

    for Operator in Operators:
        # example query:  (apple,orange) OR (banana,kiwi)
        # insert space around parenthesis
        Query = Query.replace(Operator, f" {Operator} ")

    ########################################################################

    # TokensWithGroups = group_words_collect(Prg, Query)
    TokensWithGroups = Query.split(" ")

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

def token_explain_summa(TokenProcessExplainPerDoc):
    TokenProcessExplainSumma = dict()
    for Source, Explains in TokenProcessExplainPerDoc.items():
        for Explain in Explains:
            Token, ResultsNumNow = Explain
            util.dict_key_insert_if_necessary(TokenProcessExplainSumma, Token, 0)
            TokenProcessExplainSumma[Token] += ResultsNumNow

    return TokenProcessExplainSumma

############################# REFACTOR ###########################

def get_operator_positions(Tokens):
    OperatorPositions = {}
    for Position, Token in enumerate(Tokens):
        if Token.IsOperator:
            util.dict_key_insert_if_necessary(OperatorPositions, Token.OperatorName, list())
            OperatorPositions[Token.OperatorName].append(Position)
    return OperatorPositions

def operator_exec(Tokens, Scope="subsentence", SubSentenceMulti=100, WordPositionMulti=100, CallLevel=0, ProgressBarConsole=None):

    for Position in range(0, len(Tokens)): # expand all groups in all levels first
        Token = Tokens[Position]
        if util.is_list(Token):
            operator_exec(Token, Scope=Scope, SubSentenceMulti=SubSentenceMulti, WordPositionMulti=WordPositionMulti, CallLevel=CallLevel+1, ProgressBarConsole=ProgressBarConsole)
            Tokens[Position] = Token[0]
            Tokens[Position].IsGroup = True # the main, collector, result object is group

    for Operator in Operators:

        # during operator exec, the positions can be changed so I have to check them in every Op
        OperatorPositions = get_operator_positions(Tokens)

        # if operator exist in the position lists and it has any open position
        while (Operator in OperatorPositions) and OperatorPositions[Operator]:

            if ProgressBarConsole:                  # I work with 3 tokens in same time:
                ProgressBarConsole.update(Change=3) # the operators and two operands

            OperatorPositionLast = OperatorPositions[Operator].pop()
            ParamLeft  = Tokens[OperatorPositionLast - 1]
            ParamRight = Tokens[OperatorPositionLast + 1]

            ###############################################################
            if Operator == "OR": # slow test: ..eading
                ResultOpExec = ParamLeft.Results + ParamRight.Results

            ###############################################################
            elif Operator == "AND": # slow test: prefer AND reading AND cards AND the AND yet
                if len(ParamLeft.Results) >= len(ParamRight.Results):
                    ResultsBig =  ParamLeft.Results
                    ResultsSmall = ParamRight.Results
                else:
                    ResultsBig = ParamRight.Results
                    ResultsSmall = ParamLeft.Results

                ResBigScoped = set()
                for ResBig in ResultsBig:
                    ResBigScoped.add(ResBig.Scopes[Scope])

                ResultOpExec = []
                for ResSmall in ResultsSmall:
                    if ResSmall.Scopes[Scope] in ResBigScoped:
                        ResultOpExec.append(ResSmall)

            ###############################################################
            elif Operator == "THEN":

                ResRightScoped = dict()
                for ResRight in ParamRight.Results:
                    # store the current scope AND the finest scope to detect the word order later
                    ResRightScoped[ResRight.Scopes[Scope]] = ResRight.Scopes["word"]

                ResultOpExec = []
                for ResLeft in ParamLeft.Results:
                    if ResLeft.Scopes[Scope] in ResRightScoped:
                        if ResLeft.Scopes["word"] < ResRightScoped[  ResLeft.Scopes[Scope]   ]:
                            ResultOpExec.append(ResLeft)
            ###############################################################

            OperatorObj = Tokens[OperatorPositionLast]
            ObjResult = TokenObj(ParamLeft.words() + OperatorObj.words() + ParamRight.words(), Results=ResultOpExec)
            ObjResult.Explain = [ParamLeft, OperatorObj, ParamRight]
            Tokens[OperatorPositionLast-1] = ObjResult
            Tokens.pop(OperatorPositionLast + 1)
            Tokens.pop(OperatorPositionLast)

class ResultObj():
    def __init__(self, Line_SubSentence_WordPos, SubSentenceMultiplier=100, WordMultiplier=100):
        LineNum, SubSentenceNum, WordNum = \
            text.linenum_subsentencenum_wordnum_get(Line_SubSentence_WordPos, SubSentenceMultiplier, WordMultiplier)
        self.Scopes = { "subsentence":  LineNum * SubSentenceMultiplier + SubSentenceNum,
                        "sentence": LineNum,
                        "word": Line_SubSentence_WordPos}

_EmptySet = set()
class TokenObj():
    def explain(self):
        if self.IsOperator:
            return [] # operators don't have explains

        ExplainTotal = [(self.words(ToStr=True), len(self.Results))]
        for Parent in self.Explain:
            ExplainTotal.extend(Parent.explain())
        return ExplainTotal

    def words(self, ToStr=False):
        if ToStr:
            Pre = Post = ""
            if self.IsGroup:
                Pre, Post = "(", ")"

            # there can be ( ) signs in Words, too
            Out = []
            for W in self.Words:
                if W == "(":
                    Out.append(W) # add "(", ")" signs without space into text
                elif W == ")":
                    if Out[-1] == " ":
                        Out.pop()
                    Out.append(W)  # add "(", ")" signs without space into text
                else:
                    Out.append(W)
                    Out.append(" ")

            if Out[-1] == " ": # if we have a space as last elem, remove it
                Out.pop()
            return Pre + "".join(Out) + Post
        else:
            Pre = Post = []
            if self.IsGroup:
                Pre, Post = ["("], [")"]
            return Pre + self.Words + Post

    def __init__(self, Words, DocIndex=dict(), Results=[], SubSentenceMultiplier=100, WordMultiplier=100, Prg=dict(), WordsDetected=set()):

        if util.is_str(Words): Words = [Words]

        self.Words = Words   # ["apple"]  name is a list with used keywords+operators
                             # if you have more than one elem in Words, you get it after an operator exec

        self.Prg = Prg
        self.WordsDetected = WordsDetected
        self.DocIndex = DocIndex
        self.SubSentenceMultiplier = SubSentenceMultiplier
        self.WordMultiplier = WordMultiplier

        self.IsOperator = False
        self.IsKeyword = False
        self.IsGroup = False

        self.Results = [] # list, because set can't differentiate objects with wame values
        self.Explain = []
        self.OperatorName = ""

        if len(Words) == 1:
            Word = Words[0]
            if is_operator(Word):
                self.IsOperator = True
                self.OperatorName = Word

            elif util.is_str(Word):
                self.IsKeyword = True
                self.load_from_docindex([Word])

                if not self.Results:
                    self.group_words_collect(Word)

        elif len(Words) > 1:
            self.IsGroup = True
            if Results:
                self.Results = Results

    def get_results(self, Scope="word", ToList=True):  # this func is used from tests
        ResultsCollected = set()
        for Res in self.Results:
            ResultsCollected.add(Res.Scopes[Scope])
        if ToList:
            return sorted(
                list(ResultsCollected))  # for testing, give same results in same order: set order is undefined
        return ResultsCollected

    def load_from_docindex(self, Words):
        for Word in Words:
            if Word in self.DocIndex:
                self.WordsDetected.add(Word)
                for Line_SubSentence_WordPos in self.DocIndex[Word]:
                    self.Results.append(ResultObj(Line_SubSentence_WordPos, self.SubSentenceMultiplier, self.WordMultiplier))

    # WANTED WORDS EXTENDING!!!
    def group_words_collect(self, KeyWord):
        KeyWord = quick_form_convert_to_special_form(KeyWord, "*")
        KeyWord = quick_form_convert_to_special_form(KeyWord, "..")
        if ":" in KeyWord:  # : means: special token

            if   KeyWord == "have:all":           self.load_from_docindex(eng.HaveAll)
            elif KeyWord == "pronouns:subject":   self.load_from_docindex(eng.PronounsSubject)
            elif KeyWord == "pronouns:object":    self.load_from_docindex(eng.PronounsObject)
            elif KeyWord == "pronouns:personal":  self.load_from_docindex(eng.PronounsPersonal)
            elif KeyWord == "iverb:ps":           self.load_from_docindex(eng.IrregularVerbsPresentSimple)
            elif KeyWord == "iverb:pp":           self.load_from_docindex(eng.IrregularVerbsPastParticiple)
            elif KeyWord == "iverb:inf":          self.load_from_docindex(eng.IrregularVerbsInfinitive)

            elif KeyWord.startswith("end:"):
                End = KeyWord.split(":")[1]
                self.load_from_docindex(eng.groups_of_word_ending(self.Prg, End))

            elif KeyWord.startswith("start:"):
                Start = KeyWord.split(":")[1]
                self.load_from_docindex(eng.groups_of_word_starting(self.Prg, Start))

            elif KeyWord.startswith("in:"):
                In = KeyWord.split(":")[1]
                self.load_from_docindex(eng.groups_of_word_include(self.Prg, In))
            else:
                print("unknown special group selector:", KeyWord)

def quick_form_convert_to_special_form(Token, Sign):
    LenSign = len(Sign)
    if Sign in Token:
        StarPrefix = Token.startswith(Sign)
        StarPostfix = Token.endswith(Sign)
        if StarPrefix and StarPostfix: Token = "in:" + Token[LenSign:-LenSign]

        #  *move  -> reMOVE
        if StarPrefix and (not StarPostfix): Token = "end:" + Token[LenSign:]

        # move* -> MOVEment
        if (not StarPrefix) and StarPostfix: Token = "start:" + Token[:-LenSign]
    return Token

