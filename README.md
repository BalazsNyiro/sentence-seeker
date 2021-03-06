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

### Seeking ###
example: 'dog AND cat' 
the program create a lowercase based index about texts from documents dir, and search the lowercase version of keywords in the indexes.
Please use operators in ALL CAPS.

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
- be:all (be,was,were,been,wasn,weren,am,are,is,aren,isn)
- count:all (much,many,little,few,lot,plenty)  
- do:all (do,did,done,does,don,didn,doesn)  
- have:all (have,has,had,haven,hasn,hadn,ve)
- pronouns:subject (i,you,he,she,it,we,they,anybody,somebody,nobody,nothing,anything,something,anyone,someone)
- pronouns:object (me,you,him,her,it,we,us,them,whom)
- pronouns:personal (pronouns:subject + pronouns:object)
- questionwords:all (who,where,when,why,what,which,whose,how)

## Complex examples: ##
- pronouns:personal AND have:all AND iverb:pp  *They've written*

## Settings, on/off commands ##
- url:on/off *show/hide url of the result*
- source:o/off *show/hide source doc name of the result*
- privacy:on/off *hide/show your document directory path in gui title*
- :info * show informations about current program settings

## Plain help display ##
 - help:plain display this documentation without any formatting/coloring
  
## Scopes ##
- scope:sentence  * search words in whole sentences*
- scope:subsentence *search words in subsentences only: a comma, a dot, a questionmark or other non-alphanumeric chars limits the range of search* 

## Console mode pager keys if you received results: ##
- page next: *n, Space, ArrowRight, ArrowDown, Enter, j (from vim)*
- page prev: *p, BackSpace, ArrowLeft, ArrowUp, k (from vim)*

Exit from console mode: *q :q  :quit, :exit*

# Big question: why does the program have more exit/quit command? # 
At the prompt where you write your query, somehow I have to
separate the query from special commands - the ':' sign does this.
The main rule: every special command has ':' sign,

Answer: ':q', ':quit' come from vim. For users who likes it, it's comfortable.
but in result viewer the program uses one character to 'next', 'prev' and 'quit'
because there I detect keypresses - there the ':' character and Enter pressing
is not important, you can handle the result viewer with simple key presses,

And when you often use the program, from the result viewer 
you associate the simple Q with quit. But at the prompt a simple 'q' would be
a normal query.

So this is an exception, for the better user experience. And I don't want
to break my rule so the program has normal quit commands, and others that users like.

In the Result viewer you can use space, enter, right-arrow, n, j as a next button,
because it's natural. Sorry about it, I try to find the balance between
rules and the acceptable comfort.

And I use the program every day so I will implement the most fine solutions.

## Special commands: ##
- :back N    *where N can be 1, 2, 3, 4, 5, 6 or empty.*
  short form: b
  the 'b' works from result viewer too, in tty console.
You can use it only in Linux virtual consoles (not from any GUI!)
This is a special command but really USEFUL
if you use sentence-seeker.py from virtual-console mode where
you can change between consoles with Alt+F1, ALT+F2, you can use
and editor in one terminal (I use vim in console 1) and sentence-seeker.py in
another virtual terminal.
when you type :back,  the program switch back into the given terminal without
any magic with ALT+Fn


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
   
# Program demo #
 - youtube records:
    - 2020 dec 11: https://youtu.be/cYZlCB7Hdew
 - start consol/gui mode

 - the program arrives with pre-packed text files, they are in 
   .sentence-seeker/documents directory in your home dir after
   the first execution.

 - the program creates index at first execution, it takes about 2 minutes.
   if you simply copy a txt/html/pdf file into the doc dir, at next start
   the program indexes it at start automatically.

 - simple query: 
    AND: order is not important, THEN: order is important
    - cat AND dog
    - cat AND dog > day..
    - cat > dog    ==  cat THEN dog  
    - (apple OR orange) AND eat
    - (apple OR orange) AND (eat OR drink)
 - operators: AND, OR, THEN, >, (,)
 - class usage: 
   - pronouns:personal AND have:all AND iverb:pp 
     example result: 'They've written'
   - be:all > ..ywhere  
   - (be:all) > ..ible
   - move.. > (from OR to) > ..where 
     
# Personal examples - request collection #
- (sack OR bag) > of
- (take OR took) off
- questionwords:all AND count:all 
- look.. back
- have:all yet
- touch hair head
- fell argument


# Branches #
 - master: tested/offered for end users
 - dev: it work generally, sometime tests are failed/missing/under repair,
        smaller issues can appear.
 - sandbox: I try out ideas, refactors here - maybe works, maybe not.  

Merge order: sandbox -> dev -> master

## Memory usage ## 
If you load the Encyclopaedia Britannica (~120 volume) and all other samples into your document dir, then the program uses about 1 Gigabyte memory. 

