# -*- coding: utf-8 -*-
import os, gzip

# Tested
def dir_delete_if_exist(Prg, Path, Print=False):
    if os.path.isdir(Path):
        Msg = f"Dir exists, delete it: {Path}"
        os.rmdir(Path)
    else:
        Msg = f"Dir doesn't exist: {Path}"

    if Print: print(Msg)
    log(Prg, Msg)

# Tested
def dir_create_if_necessary(Prg, Path, LogCreate=True):
    if os.path.isdir(Path):
        Msg = f"not created: dir exists, {Path}"

    elif os.path.isfile(Path):
        Msg = f"not created: it was a filename, {Path}"

    else:
        os.mkdir(Path)
        Msg = f"dir created, it was necessary: {Path}"

    if LogCreate:
        log(Prg, Msg)

    print("\ndir create if necessary Ret:", Msg)
    return Msg

# Tested with usage in tests...
def log(Prg, Msg, Caller="-"):
    print("\nLog received:", Msg)
    # from func log calls don't use Logging again
    Msg = str(Msg)
    if Prg["TestExecution"]:
        Msg = "Testing... " + Msg
    file_write(Prg, Fname=Prg["FileLog"], Content=Msg + "\n", Mode="a", Log=False)
    print("Log:", Msg)

# Tested
def file_read_all(Prg, Fname="", Mode="r", Gzipped=False): # if you want read binary, write "rb"
    if os.path.isfile(Fname):
        if Gzipped:
            with gzip.open(Fname, 'rb') as f:
                Content = f.read()
                log(Prg, f"file_read_all - gzipped: {Fname}")
                return True, Content
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
def file_write(Prg, Fname="", Content="", Mode="w", Gzipped=False, CompressLevel=9, Log=True):
    if not Fname:
        Msg = "file write error: fname is unknown util:file_write"
        if Log:
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
        if Log:
            log(Prg, f"File written: {Fname}")
        return True
    except:
        log(Prg, f"File write error: {Fname}")

    return False



