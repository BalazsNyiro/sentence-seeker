# -*- coding: utf-8 -*-
import os

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

    return Msg

def log(Prg, Msg):
    print("Log:", Msg)



