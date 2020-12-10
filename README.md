# sentence-seeker

Text analyzer program to find examples from real texts

- Developer: Balazs Nyiro, diogenesz@pergamen.hu
- facebook channel:  sentence-seeker.net
- https://www.facebook.com/groups/2449430305347843

## Quick start: ##

### console mode start: ##
  ./sentence-seeker.py --ui console

  When you start the program in console mode, it displays
  your 'Docs' dir path above the 'wanted>' prompt.

### GUI start: ###
  ./sentence-seeker.py --ui tkinter

  Documents dir is displayed in window title.
  The program detects it's environment and if it's able,
  it starts the gui if you don't pass ui.

### automata start: ###
  ./sentence-seeker.py

  and the program chooses console mode if you use it from virtual
  console from example or starts Tkinter if you have Window manager.

## Quick Tour - Documents dir: ##
The program searches sentences in documents of this dir.

- copy your documents into your 'Documents'
  you can create subdirs as you want

  default:  user_home/.sentence-seeker/documents

            the program create it at first start,
            if it doesn't exist

The program will detect the files that it can analyse

## How to seek: ##
- lowercase words: that you seek in sentences
- Sentence|SENTENCE|sentence will be found: seeking is NOT case sensitive
- AND OR: logical operators
- () group words: (apple, grape) OR (banana, orange)
- space and comma means AND:  (apple,orange banana)

- THEN operator: 'go home' is typical. But 'go' is after 'home'?
  example: 'home THEN go'

  '>' shorter form of THEN:
  example: 'one > of > them'

Examples:
- 'enormous (quantity OR volume)

## Word class selectors: ##
- iverb:inf *irregular verbs, Infinitive*
- iverb:ps  *irregular verbs, Past Simple*
- iverb:pp  *irregular verbs, Past Participle*
  - example: *would AND iverb:ps*
  - example: *would have iverb:pp*

## Word class with pattern selectors: ##
- start:ha words with 'ha' prefix *HAve, HAd...*
- end:ed words with 'ed' postfix *highlightED*
- in:cl words with 'cl' included *inCLuded, CLear*

## Quick writing forms, everybody can use his favourite: ##
-  '..look.. AND like.. AND ..ing'
-  '*look* AND like* AND *ing'
   means: 'in:look AND start:like AND end:ing'

## Examples:
- 'move.. since' *...has moved since...*
- 'plant.. grow..' *...plants grown...*
- '..ible' *impossible, incredible, terrible...*

## Other selectors: ##
- have:all (have,has,had,haven,hasn,hadn,ve)
- pronouns:subject (i,you,he,she,it,we,they)
- pronouns:object (me,you,him,her,it,we,us)
- pronouns:personal (pronouns:subject + pronouns:object)

## Complex examples: ##
- pronouns:personal AND have:all AND iverb:pp  *They've written*

## On/Off commands, turn on/off some settings: ##
- :urlOn/Off *show/hide url of the result*
- :sourceOn/Off *show/hide source doc name of the result*
- :dirDocDisplayOn/Off *hide/show your document directory path in gui title*

## Console mode pager keys if you received results: ##
- page next: *n, Space, ArrowRight, ArrowDown, Enter, j (from vim)*
- page prev: *p, BackSpace, ArrowLeft, ArrowUp, k (from vim)*

Exit from console mode: *:q  :quit, :exit*

# User guide #

The program uses a Working directory, based on user_home/.sentence-seeker.config

- DirWorking/documents:
    - original document
    - indexed text info to boost up analysing

- when the program find a document first time, it extract
  text info to boost up the seeking in the text

- if the indexed text is available, the program uses it

## Install ##
- please install Python 3.8 or newer

### Empty Ubuntu Linux ###
 - apt install python3-tk
 - apt install python3-pip

### Windows 10 ###
Please install Python for Windows, the installer contains Tkinter automatically.
https://www.python.org/downloads/windows/
   


