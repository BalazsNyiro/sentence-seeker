# sentence-seeker

Sentence seeker, text analyzer program to find examples from real texts

Developer: Balazs Nyiro, diogenesz@pergamen.hu

## Install
##### Empty Ubuntu Linux
 - apt install python3-tk
   apt install python3-pip
 - the program uses about 280Mb memory with all default texts,
   I try to decrease the memory usage.
   
   The speed of search is extremely fast because of 
   int based line/subsentence positioning
   


## Roadmap
31 may, 2020:
 - Desktop Gui implemented 

23 may, 2020:
 - facebook channel:  sentence-seeker.net
   https://www.facebook.com/groups/2449430305347843
 
 - I implemented the simple sentence analyser logic
   in the online version of the program:
   http://www.sentence-seeker.net
   
   and I realised that I know a more efficient way to
   find the wanted result from database
   so I want to rewrite the result selection
   logic in desktop and online version, too.

   The current desktop version can analyse
   about 20 books in 0.02 second so it's fast enough
   but this solution has too wide response time
   on the web server   

19 may, 2020: 
 - Web page development with desktop Text analyser logic is in progress. 
 - First Refactor period is over.

In the far, far future a controller process are going to send requests for nodes in same host and in different hosts too, so the whole seeking happens simultaneously

### "Future plans:"
##### "Get some rest"
  - Main program: use REST API to search, 
  - simple user interface, in browsers 

##### "Documentation update"

##### "Daemons"
  - use more than one daemon process to speed up the seeking
    separated controller process
  - http user interface, dark mode, 

##### "Documentation update"

##### "Argus's eyes"
Thinking period, how can I refactor the program

  - Refine text preprocessing:
    - what is a sentence? 
    - how fast is seeking?

##### "My Business - Import from offered sources"
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

#### "Get into Ubuntu repo"
  - https://askubuntu.com/questions/16446/how-to-get-my-software-into-ubuntu
    - https://wiki.debian.org/DebianMentorsFaq
    - https://www.debian.org/doc/manuals/developers-reference/pkgs.html#newpackage


#### "A little pause"
  - At this point 
    - the user can search in his own library
    - the user can import from predefined articles, sets

#### More that we can do:

  - store precompiled format for faster processing
    (it can be recompiled after version switchting)

  - parallel text processing: 
    - one controller process
    - more worker process in same and different hosts

  - use .epub, .mobi, .pdf, .doc, .rtf sources?

  - ?? do you need plugins, extendibility

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
     
 


