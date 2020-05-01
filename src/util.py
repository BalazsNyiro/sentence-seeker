# -*- coding: utf-8 -*-
import os, gzip, shutil


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

def file_read_lines(Fname, Strip=False):
    with open(Fname, 'r') as F:
        if Strip:
            return [L.strip() for L in F.readlines()]
        else:
            return F.readlines()

# Tested, Prg is important for log, or maybe we should skip logging?
def file_read_all(Prg, Fname="", Mode="r", Gzipped=False): # if you want read binary, write "rb"
    if os.path.isfile(Fname):
        if Gzipped:
            with gzip.open(Fname, 'rb') as f:
                try:
                    log(Prg, f"file_read_all - gzip read start: {Fname}")
                    ContentBytes = f.read()
                    log(Prg, f"file_read_all - gzip utf-8 conv BEGIN {Fname}")
                    # Content = str(ContentBytes, 'utf-8', 'ignore')  # errors can be ignored
                    Content = str(ContentBytes, 'utf-8')  # return with "" in this case
                    log(Prg, f"file_read_all - gzip utf-8 conv END {Fname}")
                    log(Prg, f"file_read_all - gzip utf-8 ok    {Fname}")
                    return True, Content
                except:
                    log(Prg, f"file_read_all - gzip read error or convert to unicode error: {Fname}")
                    return False, "gzip read error"
        else:
            with open(Fname, Mode) as f:
                Content = f.read()
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


