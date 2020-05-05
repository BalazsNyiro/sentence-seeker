# -*- coding: utf-8 -*-
import os, gzip, shutil, subprocess

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
def dict_key_insert_if_necessary(Dict, Key, Default):
    if Key not in Dict:
        Dict[Key] = Default

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
        file_write(Prg, Fname=Path, Content=ContentDefault, LogCreate=LogCreate)
        Created = True
        Msg = f"file create if necessary - created: {Path}"

    if LogCreate:
        log(Prg, Msg)

    return Created

# FIXME?
# you can't use this version on windows because utf8 conversion error.
# now I read the whole text and split it to lines in file_index_create func
def file_read_lines(Fname, Strip=False):
    with open(Fname, 'r') as F:
        if Strip:
            return [L.strip() for L in F.readlines()]
        else:
            return F.readlines()

# Tested with the life
# of course somehow I have to test it, it's a magic :-)
def utf8_conversion_with_warning(Bytes, FileName):
    try:
        Content = str(Bytes, 'utf-8')
    except:
        print(f"WARNING: one or more char not convertable to utf-8 in: {FileName}")
        Content = str(Bytes, 'utf-8', 'ignore')  # errors can be ignored
    return Content

# Tested, Prg is important for log, or maybe we should skip logging?
def file_read_all(Prg, Fname="", Gzipped=False): # if you want read binary, write "rb"
    if os.path.isfile(Fname):
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
            with open(Fname, 'rb') as f:
                ContentBytes = f.read()
                Content = utf8_conversion_with_warning(ContentBytes, Fname)
                log(Prg, f"file_read_all - text: {Fname}")
                return True, Content

    return False, ""

# Tested
def file_del(Path):
    if os.path.isfile(Path):
        os.remove(Path)
        return True
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
def files_collect_from_dir(DirRoot, Recursive=True):
    FilesAbsPath = []
    for DirPath, DirNames, FileNames in os.walk(DirRoot):
        FilesAbsPath += [os.path.join(DirPath, File) for File in FileNames]
        
        # https://stackoverflow.com/questions/4117588/non-recursive-os-walk
        if not Recursive:
            break

    return FilesAbsPath

# tested manually
def print_dev(Prg, *args):
    if Prg["PrintForDeveloper"]:
        print(*args)

# Tested with usage in tests...
def log(Prg, Msg, Caller="-"):
    print_dev(Prg, "\nLog received:", Msg)
    # from func log calls don't use Logging again
    Msg = str(Msg)
    if Prg["TestExecution"]:
        Msg = "Testing... " + Msg
    file_write(Prg, Fname=Prg["FileLog"], Content=Msg + "\n", Mode="a", LogCreate=False)


