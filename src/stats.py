# -*- coding: utf-8 -*-
import time#, psutil
# psutil is not available
# TODO: detect: psutil is available or not, and use it only if its available
# save stat info with Msg
# in compiled python 3.82 it's not available
def time_save(Prg, Msg):
    Time = time.time()
    Stat = {  "Time": Time,
               "Msg": Msg,
            "Memory": "psutil.virtual_memory()"}
    Prg["Statistics"]["Memory"].append(Stat)
    return Time
