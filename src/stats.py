# -*- coding: utf-8 -*-
import time#, psutil
# psutil is not availa
# TODO: detect: psutil is available or not, and use it only if its available
# save stat info with Msg
# in compiled python 3.82 it's not available
def save(Prg, Msg):
    Stat = {  "Time": time.time(),
               "Msg": Msg,
            "Memory": "psutil.virtual_memory()"}
    Prg["Statistics"].append(Stat)
