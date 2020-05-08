# sentence-seeker

Sentence seeker, text analyzer program to find examples from real texts

Developer: Balazs Nyiro, diogenesz@pergamen.hu

## Roadmap

In the far, far future a controller process are going to send requests for nodes in same host and in different hosts too, so the whole seeking happens simultaneously

## Future plans:
  - "Naive" 0.1 version is finished (please see details below)
  - I will spend more time to document processes.
    next version deadline: May 15th

### FINISHED: "Naive" v0.1 version: (18 april - april 30, 2020) 
  - text-loader script: from a source load text into working dir.
    - store original format
    - extract preprocessed simple txt format. 
      (newlines deleted, separated by sentence endings with simple logic)
    - insert text info into simple db
      - store the source (wiki page for example), maybe the user wants to update it

  - Main program, console based, Json input/output
    - In user's home dir 
      - use/create a working dir
      - use/create default config file
    - Load texts from working dir
    - waiting for user requests (python console)
      (speed tests, regexp usage tests, memory usage analysing)

Hi, "Naive" version is ready.
  - The program extracts sentences, creates index and search in it.
  - the speed test was manual, I guess with a slow desktop pc 
    about 40-50 books can be processed in a second.
    It was a manual test and in the future it can change.
  - the raw memory usage was about 200 megabytes with 18 books
    at first manual tests. I try to decrease it

Hi, "v0.11 Documentation/refactor period" is ready, the program's main structure is represented in doc.
  - variable names'/func names' first refactor happened
  - NEXT: "Simple user interfaces" (15 May - 15 June)

## "Documentation" v0.11 (1 May - 15 May, 2020) 
  - create diagram about the program structure

## "Get some rest" v0.2 version: (15 May - 15 June)
  - Main program: use REST API to search, 
  - simple user interface, in browsers 

## "Documentation update" v0.21 (15 June - 30 June, 2020)

## "Daemons" v0.3 version (1 July - 15 July, 2020)
  - use more than one daemon process to speed up the seeking
    separated controller process
  - http user interface, dark mode, 

## "Documentation update" v0.31 (15 July - 1 Aug)

## "Argus's eyes" v0.4: (1 Aug- 31 Aug)
Thinking period, how can I refactor the program

  - Refine text preprocessing:
    - what is a sentence? 
    - how fast is seeking?

## "My Business - Import from offered sources" v1.0:
  - user can import texts from precollected categories:
    - newspapers, wikipedia sites 
    - slow importing:
      - robots.txt usage
      - mix different domains in download order and wait 
        enough time between two importing

  - user can update his source if he wants
  - delete or temporarily skipped files in library?

"The Call v1.1" - use external dictionaries, Learner's dict for example 
  - it's an interesting possibility to use them, it's an idea only


## "Get into Ubuntu repo"
  - https://askubuntu.com/questions/16446/how-to-get-my-software-into-ubuntu
    - https://wiki.debian.org/DebianMentorsFaq
    - https://www.debian.org/doc/manuals/developers-reference/pkgs.html#newpackage


## "A little pause"
  - At this point 
    - the user can search in his own library
    - the user can import from predefined articles, sets

### Future plans:
    - "Maybe v1.xy":
      - Native Windows/Linux programs to detect selected text
        in browsers, text editors and execute search based on them

  - store precompiled format for faster processing
    (it can be recompiled after version switchting)

  - parallel text processing: 
    - one controller process
    - more worker process in same and different hosts

  - use .epub, .mobi, .pdf, .doc, .rtf sources?

  - ?? do you need plugins, extendibility

# TODO: 
  - extract gzip files and process them as normal files
  - remove too old log files 
  - REST communication between controller and seeker processes
    - use more than one node to search parallel

## Coding guideline - Naming conventions
 - Variable names: UpperCamelCase, exception: self.
   - naming order: ObjectAttribute
     example: FileOld, FileNew
     
 - Private variables: starts with underscore
 - function naming: 
     - object_operation(), example: 
       - file_read(), file_write()
       - connection_open(), connection_close()
       
 - Usage of classes: 
   I try to minimize the direct usage of classes and OOP techniques.
   It's a feeling only but at the end, at parallel text processing
   It's better to use simple data structures and functions.
     
 


