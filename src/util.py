# -*- coding: utf-8 -*-
import os, gzip, shutil, pathlib, urllib.request
import util_json_obj, sys

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

# Tested
def dict_key_insert_if_necessary(Dict: dict, Key: any, Default: any):
    if Key not in Dict:
        Dict[Key] = Default

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
        Msg = f"file create if necessary - not created: it was a filename, {Path}"
    else:
        print("File creation:", Path)
        Created = file_write(Prg, Fname=Path, Content=ContentDefault, LogCreate=LogCreate)
        Msg = f"file create if necessary - created: {Created}  {Path}"
        print(Msg)

    if LogCreate:
        log(Prg, Msg)

    return Created

def filename_extension(Fname):
    return pathlib.Path(Fname).suffix.lower()

def filename_without_extension(Fname):
    Extension = filename_extension(Fname)
    if not Extension:
        return Fname
    return Fname.rsplit(Extension, 1)[0]

# FIXME?
# you can't use this version on windows because utf8 conversion error.
# now I read the whole text and split it to lines in file_index_create func
def file_read_lines_orig(_Prg, Fname, Strip=False):
    with open(Fname, 'r') as F:
        if Strip:
            return [L.strip() for L in F.readlines()]
        else:
            return F.readlines()

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

    if  Lines:
        Lines[-1] = Lines[-1].replace("\n", '') # the last elem can't have \n at end

    return Lines

# no PRG usage
def file_read_all_simple(Fname="",mode="r"): # if you want read binary, write "rb"
    with open(Fname, mode) as f:
        return f.read()

# Tested, Prg is important for log, or maybe we should skip logging?
def file_read_all(Prg, Fname="", Gzipped=False): # if you want read binary, write "rb"
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

                    Content = utf8_conversion_with_warning(ContentBytes, Fname)
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
                with open(Fname, 'rb') as f:
                    ContentBytes = f.read()
                    Content = utf8_conversion_with_warning(ContentBytes, Fname)
                    log(Prg, f"file_read_all - text: {Fname}")
                    return True, Content
            except:
                log(Prg, f"file_read_all - read error, in 'with' block: {Fname}")
                return False, "read error"


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

    file_write(Prg, Fname, Content.encode(), Mode="wb")

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
        with open(Fname, Mode) as f:
            f.write(Content)
        if LogCreate:
            log(Prg, f"File written: {Fname}")
        return True
    except:
        log(Prg, f"File write error: {Fname}")

    return False

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
    if "PrintForDeveloper" in Prg:
        if Prg["PrintForDeveloper"]:
            print(*args)

# Tested with usage in tests...
def log(Prg, Msg, Caller="-"):
    print_dev(Prg, "\nLog received:", Msg)
    # from func log calls don't use Logging again
    Msg = str(Msg)
    if "TestExecution" in Prg:
        if Prg["TestExecution"]:
            Msg = "Testing... " + Msg
    if "FileLog" in Prg:
        file_write(Prg, Fname=Prg["FileLog"], Content=Msg + "\n", Mode="a", LogCreate=False)


def display_groups_matchnum_resultinfo(GroupsObj):
    for MatchNum, ResultInfos in GroupsObj.items():
        for ResultInfo in ResultInfos:
            print(MatchNum, ResultInfo)

# Tested with the life
# of course somehow I have to test it, it's a magic :-)
def utf8_conversion_with_warning(Bytes, Source):
    try:
        Content = str(Bytes, 'utf-8')
    except:
        print(f"WARNING: one or more char not convertable to utf-8 in: {Source}")
        Content = str(Bytes, 'utf-8', 'ignore')  # errors can be ignored
    return Content

def web_get(Url, Binary=False):
    Url = Url.strip()
    print(f"web html get: {Url}, Binary:{Binary}")

    with urllib.request.urlopen(Url) as Response:
        if Binary:
            # https://stackoverflow.com/questions/9419162/download-returned-zip-file-from-url
            return Response.read()
        else:
            # Html = str(Response.read())
            return Response.read().decode('utf-8')

# TODO: test
def web_get_pack_wikipedia(Prg, DirTarget, WikiPagesUse=None):
    if not WikiPagesUse:
        WikiPagesUse = input("\nDo you want to use Wikipedia page pack from Sentence seeker server? (y/n) ").strip()
    if WikiPagesUse.strip().lower() == "y":
        Url = "http://sentence-seeker.net/texts/packs/wikipedia.txt.gz"
        try:
            BinaryFromWeb = web_get("http://sentence-seeker.net/texts/packs/wikipedia.txt.gz", Binary=True)
            Bytes = gzip.decompress(BinaryFromWeb)
            print("Url downloading is finished:", Url)
            Lines = utf8_conversion_with_warning(Bytes, Url)
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
                        FileHtmlFullPath = os.path.join(DirTarget, FileName + ".txt")
                        Written = file_write(Prg, Fname=FileHtmlFullPath, Content="\n".join(LinesDoc))
                        # print("Written:", Written, FileHtmlFullPath)

                        DocObj = {"url": Url,
                                  "source_name": SourceName,
                                  "license": License}
                        # print("DocObj", DocObj)
                        util_json_obj.doc_db_update(Prg, FileHtmlFullPath, DocObj)  # and reload the updated db

                        Url = License = FileName = "-"
                        LinesDoc = []
                else:
                    LinesDoc.append(Line)
        except:
            print("Download problem:", Url)

