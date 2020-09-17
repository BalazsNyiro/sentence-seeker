# -*- coding: utf-8 -*-
import os, gzip, shutil, pathlib, urllib.request, util_json_obj
import sys, array, re, datetime, io

ABC_Eng_Upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ABC_Eng_Lower = ABC_Eng_Upper.lower()

# Tested
def shell(Cmd):
    with os.popen(Cmd) as OsProcess:
        return OsProcess.read()

    # the subprocess solution is not correct with shell grep commands

    # if isinstance(Cmd, str):
    #     Cmd = Cmd.split()

    # # https://stackoverflow.com/questions/51124745/inexplicable-resourcewarning-unclosed-file-io-textiowrapper-name-3
    # # with os.popen(Cmd) as os_process:
    # Result = subprocess.run(Cmd, capture_output=True)
    # if StdoutOnly:
    #     return str(Result.stdout, 'utf-8')
    # return Result

# wrapper, not tested
def date_now():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

# Tested
def dict_key_insert_if_necessary(Dict: dict, Key: any, Default: any):
    if Key not in Dict:
        Dict[Key] = Default
        return True
    return False

# Tested
def dict_value_insert_into_key_group(Dict, Key, Val):
    dict_key_insert_if_necessary(Dict, Key, [])
    Dict[Key].append(Val)

# Tested
def dict_key_sorted(Dict: dict, Reverse=True):
    Keys = list(Dict.keys())
    Keys.sort(reverse=Reverse)
    return Keys

# Tested, it can delete empty dirs
def dir_delete_if_exist(Prg, Path, Print=False):
    Ret = ""
    if os.path.isdir(Path):
        Msg = f"Dir exists, delete it: {Path}"
        os.rmdir(Path)
        Ret = "deleted"
    else:
        Msg = f"Dir doesn't exist: {Path}"

    if Print:
        print(Msg)
    log(Prg, Msg)

    return Ret

# Tested
def dir_create_if_necessary(Prg, Path, LogCreate=True):
    Created = False

    if os.path.isdir(Path):
        Msg = f"not created: dir exists, {Path}"

    elif os.path.isfile(Path):
        Msg = f"not created: it was a filename, {Path}"

    else:
        os.mkdir(Path)
        Msg = f"dir created, it was necessary: {Path}"
        Created = True

    if LogCreate:
        log(Prg, Msg)

    print_dev(Prg, "\ndir create if necessary Ret:", Msg)
    return Created

# Tested
def file_create_if_necessary(Prg, Path, ContentDefault="", LogCreate=True):
    Created = False

    if os.path.isfile(Path):
        Msg = f"\nfile create if necessary - not created: it was a filename, {Path}"
    else:
        Created = file_write(Prg, Fname=Path, Content=ContentDefault, LogCreate=LogCreate)
        Msg = f"\nfile create if necessary - created: {Created}  {Path}"
        print(Msg)

    if LogCreate:
        log(Prg, Msg)

    return Created

def has_uppercase(Txt):
    return True if Txt.lower() != Txt else False

# Tested
def filename_extension(Fname): # works with fullpath, too: /home/user/file.txt
    return pathlib.Path(Fname).suffix
# Tested
def filename_without_extension(Fname):
    Extension = filename_extension(Fname)
    if not Extension:
        return Fname
    return Fname.rsplit(Extension, 1)[0]

# Tested in file_read_lines's test / wrappe fun, test not necessary
def file_read_all_simple(Fname="", mode="r"): # if you want read binary, write "rb"
    with open(Fname, mode) as f:
        return f.read()
# tested
def file_read_lines(Prg, Fname, Strip=False, Lower=False):
    _Success, TextAll = file_read_all(Prg, Fname)
    Lines = []
    for Line in TextAll.split("\n"):

        if Lower:
            Line = Line.lower()

        if Strip:
            Lines.append(Line.strip())
        else:
            Lines.append(Line+"\n") # give back ending newline

    if Lines:
        Lines[-1] = Lines[-1].replace("\n", '') # the last elem can't have \n at end

    return Lines

# Tested, Prg is important for log, or maybe we should skip logging?
def file_read_all(Prg={}, Fname="", Gzipped=False):
    # print("Fname:", Fname, "isfile:", os.path.isfile(Fname))
    if not os.path.isfile(Fname):
        Msg = f"file_read_all - file doesn't exist: {Fname}"
        log(Prg, Msg)
        print(Msg)
        return False, Msg
    else:
        if Gzipped:
            with gzip.open(Fname, 'rb') as f:
                try:
                    log(Prg, f"file_read_all - gzip read start: {Fname}")
                    ContentBytes = f.read()
                    log(Prg, f"file_read_all - gzip utf-8 conv BEGIN {Fname}")

                    Content = utf8_conversion_with_warning(Prg, ContentBytes, Fname, FunCaller="file_read_all gzipped")
                    # Content = str(ContentBytes, 'utf-8', 'ignore')  # errors can be ignored
                    # Content = str(ContentBytes, 'utf-8')  # return with "" in this case

                    log(Prg, f"file_read_all - gzip utf-8 conv END {Fname}")
                    log(Prg, f"file_read_all - gzip utf-8 ok    {Fname}")
                    return True, Content
                except:
                    log(Prg, f"file_read_all - gzip read error or convert to unicode error: {Fname}")
                    return False, "gzip read error"
        else:
            # with bytes the utf-8 conversion can be tuned, errors ignored
            try:
                Content = _file_read_unicode(Prg, Fname)
                log(Prg, f"file_read_all - text: {Fname}")
                return True, Content
            except:
                log(Prg, f"file_read_all - read error, in 'with' block: {Fname}")
                return False, "read error"

# I want to keep parameter order, but Prg is optional here.
def _file_read_unicode(Prg={}, Fname=""):
    if Fname: # Prg can be empty, if it's necessary, then we read without logging
        with open(Fname, 'rb') as f:
            ContentBytes = f.read()
            return utf8_conversion_with_warning(Prg, ContentBytes, Fname, FunCaller="file_read_unicode")
    else:
        print("file_read_unicode, Fname can't be empty!")
        sys.exit(1)

# Tested
def file_del(Path, Verbose=False):
    if os.path.isfile(Path):
        os.remove(Path)
        if Verbose:
            print(f"\nfile removed: {Path}")
        return True

    if Verbose:
        print(f"\nfile NOT EXISTS to remove: {Path}")
    return False

# Tested
def file_append(Prg, Fname="", Content="", Mode="a"):  # you can append in binary mode, too
    return file_write(Prg, Fname=Fname, Content=Content, Mode=Mode)

def file_write_utf8_error_avoid(Prg, Fname, Content):
    # convert text to bytes. On Linux without any error
    # we can write texts but on Windows I receive conversion error message:
    # I don't understand why it doesn't use utf8 instead of cp1252
    # File "C:\Users\dioge\AppData\Local\Programs\Python\Python38-32\lib\encodings\cp1252.py", line
    # 19, in encode return codecs.charmap_encode(input, self.errors, encoding_table)[0]
    # UnicodeEncodeError: 'charmap'
    # codec
    # can
    # 't encode character '\ufeff
    # ' in position 0: character maps to <undefined>

    # Mode has to be wb because of .encode()
    return file_write(Prg, Fname, Content.encode(), Mode="wb")

# Tested
def file_write(Prg, Fname="", Content="", Mode="w", Gzipped=False, CompressLevel=9, LogCreate=True):
    if not Fname:
        Msg = "file write error: fname is unknown util:file_write"
        if LogCreate:
            log(Prg, Msg)
        return False

    # if we received a list of string, convert it to string:
    if isinstance(Content, list):
        Content = '\n'.join(Content)

    if Gzipped:
        if not "b" in Mode:
            Mode = Mode + "b"
        OutputBytes = bytes(Content, 'utf-8')
        Content = gzip.compress(OutputBytes, CompressLevel)

    try:
        file_write_simple(Fname, Content, Mode)
        if LogCreate:
            log(Prg, f"File written: {Fname}")
        return True
    except:
        log(Prg, f"File write error: {Fname}")

    return False

# tested in test_util_json.py with usage
def file_write_simple(Fname, Content, Mode="w"):
    if "b" not in Mode: # fixed unix style end of line
        with open(Fname, Mode, newline="\n") as f:
            f.write(Content)
    else:
        with open(Fname, Mode) as f:
            f.write(Content)

# Tested
def file_write_with_check(Prg, Fname="", Content="", WriterFun=file_write_utf8_error_avoid):
    WriterFun(Prg, Fname, Content)

    _, Written = file_read_all(Prg, Fname)
    if not Written == Content:
        Msg = f"file_write_with_check Write Problem: {Fname}\n{Content}"
        print(Msg)
        log(Prg, Msg)
        return False
    return True

# not tested, simple wrapper func
def file_copy(FilePathFrom, FilePathTo):
    shutil.copyfile(FilePathFrom, FilePathTo)

# Tested
def file_is_gzipped(Prg, Path):
    if os.path.isfile(Path):
        try:
            with gzip.open(Path, "rb") as f:
                f.read() # sorry about reading, I don't know a better gzip detect method now
                log(Prg, f"is_gzipped - file_exists, gzipped: {Path}")
                return "file_exists", "gzipped"
        except:
            log(Prg, f"is_gzipped - file_exists, not gzipped: {Path}")
            return "file_exists", "not_gzipped"
    else:
        log(Prg, f"is_gzipped - file not found: {Path}")
        return "file_not_found", ""

# Tested
def files_abspath_collect_from_dir(DirRoot, Recursive=True):
    FilesAbsPath = []
    for DirPath, DirNames, FileNames in os.walk(DirRoot):
        FilesAbsPath += [os.path.join(DirPath, File) for File in FileNames]
        
        # https://stackoverflow.com/questions/4117588/non-recursive-os-walk
        if not Recursive:
            break

    return FilesAbsPath

# tested manually
def print_dev(Prg, *args):
    if Prg.get("PrintForDeveloper", False):
        print(*args)

# wrapper, not tested
def int_list_to_array(L):
    return array.array("I", L)

# Tested with usage in tests...
def log(Prg, Msg, Caller="-"):
    if not Prg:
        return
    print_dev(Prg, "\nLog received:", Msg)
    # from func log calls don't use Logging again
    Msg = str(Msg)
    if Prg.get("TestExecution", False):
        Msg = f"Testing... {Msg}"

    Msg = f"[{date_now()}] {Msg}"
    if "FileLog" in Prg:
        file_write(Prg, Fname=Prg["FileLog"], Content=Msg + "\n", Mode="a", LogCreate=False)

# used only in test creation process
def display_groups_matchnum_resultinfo(GroupsObj):
    for MatchNum, ResultInfos in GroupsObj.items():
        for ResultInfo in ResultInfos:
            print(MatchNum, ResultInfo)

# YOU CAN USE IT with empty PRG, if it's necessary
# of course somehow I have to test it, it's a magic :-)
# TODO: test it with texts
def utf8_conversion_with_warning(Prg, Bytes, Source, FunCaller="fun caller is unknown"):
    try:
        Content = str(Bytes, 'utf-8')
    except:
        print(f"WARNING: one or more char not convertable to utf-8 in: {Source}")
        if Prg:
            log(Prg, f"utf8 conversion error: {Source}")
        #Content = str(Bytes, 'utf-8', 'ignore')  # errors can be ignored
        #Content = str(Bytes, 'utf-8', 'xmlcharrefreplace')
        Content = str(Bytes, 'utf-8', 'backslashreplace')  # errors can be ignored
    return Content

# TODO? Test??
def web_get(Url, Binary=False, Verbose=True):
    Url = Url.strip()
    if Verbose:
        print(f"web html get: {Url}, Binary:{Binary}")

    with urllib.request.urlopen(Url) as Response:
        Length = Response.getheader('content-length')
        BlockSize = 1024*64  # default value

        if Length:
            Length = int(Length)

        BufferAll = io.BytesIO()
        Size = 0
        while True:
            BufferNow = Response.read(BlockSize)
            if not BufferNow:
                break
            BufferAll.write(BufferNow)
            Size += len(BufferNow)
            if Length:
                Percent = int((Size / Length)*100)
                print(f"download: {Percent}% {Url}")

        if Binary:
            # https://stackoverflow.com/questions/9419162/download-returned-zip-file-from-url
            #return Response.read() # simple read all version
            return BufferAll.getvalue()
        else:
            # return Response.read().decode('utf-8')
            return BufferAll.getvalue().decode("utf-8")

# not tested: wrapper fun
def console_available():
    return sys.stdout.isatty() # True if we run in console

# manually tested
def web_get_pack_wikipedia(Prg, DirTarget, WikiPagesUse=None):
    if WikiPagesUse == None: # param not given
        if console_available(): # we are in a real terminal
            WikiPagesUse = input("\nDo you want to use Wikipedia page pack from Sentence seeker server? (y/n) ").strip()
        else:
            #  piped or redirected or started without console
            WikiPagesUse = "y"

    if str(WikiPagesUse).strip().lower() == "y":
        Url = "http://sentence-seeker.net/texts/packs/wikipedia.txt.gz"
        try:
            BinaryFromWeb = web_get("http://sentence-seeker.net/texts/packs/wikipedia.txt.gz", Binary=True)
            Bytes = gzip.decompress(BinaryFromWeb)
            print("Url downloading is finished:", Url)
            Lines = utf8_conversion_with_warning(Prg, Bytes, Url, FunCaller="web_get_pack_wikipedia")
            print("Utf8 conversion finished...")

            SourceName = "wikipedia"
            Url = "-"
            License = "-"
            FileName = "-"

            LinesDoc = []

            for LineNum, Line in enumerate(Lines.split("\n")):
                # print(Line)
                if "###" == Line[:3]:

                    Token, Data = Line[3:].split(">>>")
                    # print("token, data",Token, Data)
                    if Token == "Url":      Url = Data
                    if Token == "License":  License = Data.strip()
                    if Token == "FileName": FileName = Data

                    if Token == "End":
                        FileNameWithoutExtension = filename_without_extension(FileName)
                        FileHtmlFullPath = os.path.join(DirTarget, FileNameWithoutExtension + ".txt")
                        Written = file_write(Prg, Fname=FileHtmlFullPath, Content="\n".join(LinesDoc))
                        # print("Written:", Written, FileHtmlFullPath)

                        DocObj = {"url": Url,
                                  "source_name": SourceName,
                                  "license": License}
                        # print("DocObj", DocObj)
                        util_json_obj.doc_db_update_in_file_and_Prg(Prg, FileNameWithoutExtension, DocObj)  # and reload the updated db

                        Url = License = FileName = "-"
                        LinesDoc = []
                else:
                    LinesDoc.append(Line)
        except:
            print("Download problem:", Url)

# No test - because wrapper
def dir_user_home():
    return str(pathlib.Path.home())

# https://stackoverflow.com/a/8315566/13281559
# devel fun, not tested
def TraceFunc(Frame, Event, Arg, Indent=[0]):
    Fun = Frame.f_code.co_name

    NotImportant = [
        # very often used
        "dict_key_insert_if_necessary",
        "dict_key_sorted",
        "sentence_loaded",
        
        
        
        "<lambda>",
        "<listcomp>",
        "<module>",
        "__call__",
        "__contains__",
        "__del__",
        "__getitem__",
        "__init__",
        "__new__",
        "__str__",
        "_bind",
        "_cnfmerge",
        "_configure",
        "_get_sep",
        "_handle_fromlist",
        "_loadtk",
        "_options",
        "_register",
        "_root",
        "_setup",
        "_splitext",
        "_stringify",
        "_substitute",
        "add",
        "add_cascade",
        "add_command",
        "basename",
        "bind",
        "configure",
        "daemon",
        "decode",
        "delete",
        "destroy",
        "encode",
        "flush",
        "focus_set",
        "get",
        "getint_event",
        "grid_configure",
        "index",
        "insert",
        "isfile",
        "join",
        "mainloop",
        "mark_set",
        "nametowidget",
        "readprofile",
        "release",
        "search",
        "set",
        "shutdown",
        "splitext",
        "stream",
        "tag_add",
        "tag_bind",
        "tag_configure",
        "wm_title",
        "wm_protocol",
    ]
    if Fun not in NotImportant:

        if Event == "call":
            Indent[0] += 2
            print("-" * Indent[0] + "> call function", Fun)
        elif Event == "return":
            print("<" + "-" * Indent[0], "exit function", Fun)
            Indent[0] -= 2

    return TraceFunc

# not tested, devel fun only
def dict_mem_usage(Dict, Level=0):
    for Key, Val in Dict.items():
        IsDict = isinstance(Val, dict)
        print(" "*Level, end="")
        if IsDict:
            print(Key, sys.getsizeof(Val), type(Val))
            dict_mem_usage(Val, Level=Level+1)
        else:
            print(Key, sys.getsizeof(Val), type(Val))

def is_list(Obj):
    return isinstance(Obj, list)

def is_str(Obj):
    return isinstance(Obj, str)

def is_dict(Obj):
    return isinstance(Obj, dict)

def is_tuple(Obj):
    return isinstance(Obj, tuple)
