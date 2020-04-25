# -*- coding: utf-8 -*-
import time, psutil

# save stat info with Msg
def save(Prg, Msg):
    Stat = {  "Time": time.time(),
               "Msg": Msg,
            "Memory": psutil.virtual_memory()}
    Prg["Statistics"].append(Stat)
