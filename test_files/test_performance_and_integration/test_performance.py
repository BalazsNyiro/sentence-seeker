#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import threading, os, sys
import time

dirname = os.path.dirname
DirPrgParent = dirname(dirname(dirname(os.path.realpath(__file__))))
sys.path.append(os.path.join(DirPrgParent, "src"))

import util

ReqCounter = dict()

ThreadNum = 1
MaxI = 6000
MaxI = 1000000000000000
HostPort = "http://localhost:8000"
HostPort = "http://data.sentence-seeker.net:8000"

# local performance: circa
def thread_function(ThreadName):
    global ReqCounter

    for i in range(1, MaxI):
        ReqCounter[ThreadName] += 1
        TimeStart = time.time()
        Result = util.web_get(f"{HostPort}/seek?words=looks,like,bird", Verbose=False)
        #print(Result)
        TimeDelta = time.time()-TimeStart

        ReqTempo = int(1.0/TimeDelta)
        Info = f"{i} {ThreadName} len: {len(Result)}, Tempo {ReqTempo}, req/sec\n"
        util.file_write(dict(), Fname="test_performance.txt", Content=Info, Mode="a", LogCreate=False)
        print(Info)
        time.sleep(5)

# read this: https://realpython.com/intro-to-python-threading/
if __name__ == "__main__":

    for I in range(0, ThreadNum):
        ThreadName = f"Test {I}"
        ReqCounter[ThreadName] = 0
        threading.Thread(target=thread_function, args=(ThreadName,)).start()

