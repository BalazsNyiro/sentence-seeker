# sentence-seeker

Text analyzer program to find examples from real texts

 - Developer: Balazs Nyiro, diogenesz@pergamen.hu
 - facebook channel:  sentence-seeker.net
 - https://www.facebook.com/groups/2449430305347843
 
## Install
##### Empty Ubuntu Linux
 - apt install python3-tk
 - apt install python3-pip
   
## Performance
 - the program uses about 280Mb memory with all default texts,
   I try to decrease the memory usage.
   
 - The speed of search is extremely fast because of 
   int based line/subsentence positioning
   
##### Future functions:
  - use more than one daemon process to speed up the seeking
    separated controller process
  - http user interface, dark mode, 

  - document importing
    - user can import texts from precollected categories:
      - newspapers, wikipedia sites 
      - slow importing:
        - robots.txt usage
        - mix different domains in download order and wait 
          enough time between two importing

  - user can update his source if he wants
  - delete or temporarily skipped files in library?

  - use external dictionaries, Learner's dict for example 
    - it's an interesting possibility to use them, it's an idea only
    
  - use .epub, .mobi, .pdf, .doc, .rtf sources?
    - ?? do you need plugins, extendibility

#### "Get into Ubuntu repo"
  - https://askubuntu.com/questions/16446/how-to-get-my-software-into-ubuntu
    - https://wiki.debian.org/DebianMentorsFaq
    - https://www.debian.org/doc/manuals/developers-reference/pkgs.html#newpackage

#### More that we can do:
  - parallel text processing: 
    - one controller process
    - more worker process in same and different hosts

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
     
 


