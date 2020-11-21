import time
verbs_irregular = {
    # Base Form	Past Simple	Past Participle
    ("arise",	"arose",	"arisen"),
    ("awake",	"awoke",	"awoken"),
    ("beat",	"beat",	    "beaten"),
    ("bid",	    "bade",	    "bidden"),
    ("bite",	"bit",	    "bitten"),
    ("break",	"broke",	"broken"),
    ("choose",	"chose",	"chosen"),
    ("drive",	"drove",	"driven"),
    ("eat",	    "ate",	    "eaten"),
    ("fall",	"fell",	    "fallen"),
    ("forbid",	"forbade",	"forbidden"),
    ("forget",	"forgot",	"forgotten"),
    ("forgive",	"forgave",	"forgiven"),
    ("forsake",	"forsook",	"forsaken"),
    ("freeze",	"froze",	"frozen"),
    ("give",	"gave",	    "given"),
    ("hide",	"hid",	    "hidden"),
    ("ride",	"rode",	    "ridden"),
    ("rise",	"rose",	    "risen"),
    ("shake",	"shook",	"shaken"),
    ("shrive",	"shrove",	"shriven"),
    ("speak",	"spoke",	"spoken"),
    ("steal",	"stole",	"stolen"),
    ("strive",	"strove",	"striven"),
    ("take",	"took",	    "taken"),
    ("wake",	"woke",	    "woken"),
    ("weave",	"wove",	    "woven"),
    ("write",	"wrote",	"written"),

    ("bear",	"bore",	    "borne"),
    ("blow",	"blew",	    "blown"),
    ("draw",	"drew",	    "drawn"),
    ("fly",	    "flew",	    "flown"),
    ("grow",	"grew",	    "grown"),
    ("know",	"knew",	    "known"),
    ("lie",	    "lay",	    "lain"),
    ("see",	    "saw",	    "seen"),
    ("shine",	"shone",	"shone"),
    ("swear",	"swore",	"sworn"),
    ("tear",	"tore",	    "torn"),
    ("throw",	"threw",	"thrown"),
    ("wear",	"wore",	    "worn"),
    ("win",	    "won",	    "won"),


    ("begin",	"began",	"begun"),
    ("cling",	"clung",	"clung"),
    ("drink",	"drank",	"drunk"),
    ("fling",	"flung",	"flung"),
    ("hang",	"hung",	    "hung"),
    ("ring",	"rang",	    "rung"),
    ("shrink",	"shrank",	"shrunk"),
    ("sing",	"sang",	    "sung"),
    ("sink",	"sank",	    "sunk"),
    ("sling",	"slung",	"slung"),
    ("spin",	"spun",	    "spun"),
    ("spring",	"sprang",	"sprung"),
    ("sting",	"stung",	"stung"),
    ("stink",	"stank",	"stunk"),
    ("swim",	"swam",	    "swum"),
    ("swing",	"swung",	"swung"),
    ("wring",	"wrung",	"wrung"),

    ("bend",	"bent",	    "bent"),
    ("bet",	    "bet",      "bet"),
    ("bid",	    "bid",	    "bid"),
    ("bleed",	"bled",	    "bled"),
    ("breed",	"bred",	    "bred"),
    ("build",	"built",	"built"),
    ("burn",	"burnt",	"burnt"),
    ("burst",	"burst",	"burst"),
    ("cast",	"cast",     "cast"),
    ("cost",	"cost",	    "cost"),
    ("creep",	"crept",	"crept"),
    ("cut",	    "cut",	    "cut"),
    ("deal",	"dealt",	"dealt"),
    ("dig",	"dug",	"dug"),
    ("dwell",	"dwelt",	"dwelt"),
    ("feel",	"felt",	"felt"),
    ("forecast",	"forecast", "forecast"),
    ("get",	"got",	"got"),
    ("have",	"had",	"had"),
    ("hear",	"heard",	"heard"),
    ("hit",	"hit",	"hit"),
    ("hold",	"held",	"held"),
    ("hurt",	"hurt",	"hurt"),
    ("keep",	"kept",	"kept"),
    ("lean",	"leant",	"leant"),
    ("learn",	"learnt",	"learnt"),
    ("leave",	"left",	"left"),
    ("lend",	"lent",	"lent"),
    ("let",	"let",	"let"),
    ("light",	"lit",	"lit"),
    ("lose",	"lost",	"lost"),
    ("mean",	"meant",	"meant"),
    ("meet",	"met",	"met"),
    ("put",	"put",	"put"),
    ("rend",	"rent",	"rent"),
    ("rid ",	"rid",	"rid"),
    ("run",	"ran",	"run"),
    ("send",	"sent",	"sent"),
    ("set",	"set",	"set"),
    ("shoot",	"shot",	"shot"),
    ("shut",	"shut",	"shut"),
    ("sit",	"sat",	"sat"),
    ("sleep",	"slept",	"slept"),
    ("slide",	"slid",	"slid"),
    ("slit",	"slit",	"slit"),
    ("spend",	"spent",	"spent"),
    ("spit",	"spat",	"spat"),
    ("split",	"split",	"split"),
    ("spoil",	"spoilt",	"spoilt"),
    ("stick",	"stuck",	"stuck"),
    ("sweep",	"swept",	"swept"),
    ("thrust",	"thrust",	"thrust"),
    ("weep",	"wept",	"wept"),
    ("wet",	"wet",	"wet"),

    ("beseech",	"besought",	"besought"),
    ("bring",	"brought",	"brought"),
    ("buy",	"bought",	"bought"),
    ("catch",	"caught",	"caught"),
    ("fight",	"fought",	"fought"),
    ("seek",	"sought",	"sought"),
    ("teach",	"taught",	"taught"),
    ("think",	"thought",	"thought"),

    ("bind",	"bound",	"bound"),
    ("find",	"found",	"found"),
    ("grind",	"ground",	"ground"),
    ("wind",	"wound",	"wound"),

    ("feed",	"fed",	"fed"),
    ("flee",	"fled",	"fled"),
    ("lay",	"laid",	"laid"),
    ("lead",	"led",	"led"),
    ("lie",	"lied",	"lied"),
    ("make",	"made",	"made"),
    ("pay",	"paid",	"paid"),
    ("read",	"read",	"read"),
    ("say",	"said",	"said"),
    ("shed",	"shed",	    "shed"),
    ("speed",	"sped",	    "sped"),
    ("spread",	"spread",	"spread"),
    ("wed",	    "wed",	    "wed"),

    ("abide",	"abode",	"abode"),
    ("heave",	"hove",	    "hove"),
    ("sell",	"sold",	    "sold"),
    ("stand",	"stood",	"stood"),
    ("tell",	"told",	    "told"),
    ("tread",	"trod",	    "trod"),
    ("understand",	"understood",	"understood"),

    ("become",	"became",	"become"),
    ("come",	"came",	"come"),
    ("do",	"did",	"done"),
    ("go",	"went",	"gone"),

    # be has 2 variations in past simple
    ("be",	"was",	"been"),
    (None,  "were", None)
}

IrregularVerbsInfinitive = set()
IrregularVerbsPresentSimple = set()
IrregularVerbsPastParticiple = set()

for Elem in verbs_irregular: #
    Form1, Form2, Form3 = Elem
    if Form1:
        IrregularVerbsInfinitive.add(Form1)
    if Form2:
        IrregularVerbsPresentSimple.add(Form2)
    if Form3:
        IrregularVerbsPastParticiple.add(Form3)

#######################################
# TESTED
def selector_word_end(Word, Pattern):
    return Word.endswith(Pattern)

# TESTED
def selector_word_start(Word, Pattern):
    return Word.startswith(Pattern)

# TESTED
def word_selecting(Prg, Selector, Params):
    Selecteds = set()
    #TimeStart = time.time()
    for Doc in Prg["DocumentObjectsLoaded"].values():
        for Word in Doc["WordPosition"].keys():
            if Selector(Word, Params):
                Selecteds.add(Word)
    #print("selecting total:", time.time() - TimeStart)
    print("word selecting total:", len(Selecteds))
    return Selecteds

# TESTED
def groups_of_word_ending(Prg, End):
    if "Cache" not in Prg:
        Prg["Cache"] = dict()
    if End in Prg["Cache"]:
        return Prg["Cache"][End]

    Selecteds = word_selecting(Prg, selector_word_end, End)

    Prg["Cache"][End] = Selecteds
    return Selecteds

# TESTED
def groups_of_word_starting(Prg, Start):
    if Start in Prg["Cache"]:
        return Prg["Cache"][Start]

    Selecteds = word_selecting(Prg, selector_word_start, Start)

    Prg["Cache"][Start] = Selecteds
    return Selecteds
