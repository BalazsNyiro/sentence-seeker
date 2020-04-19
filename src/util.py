# -*- coding: utf-8 -*-
import os

# here don't
def dir_create_if_necessary(Prg, Path, LogCreate=True):
    if not os.path.isdir(Path):
        os.mkdir(Path)
        if LogCreate:
            log(Prg, f"Dir {Path} Created, it was necessary")

def log(Prg, Msg):
    print("Log:", Msg)


