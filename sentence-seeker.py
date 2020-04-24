#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(DirPrgParent, "src"))

import config, util_test
##########################################################

Prg = config.PrgConfigCreate()
config.DirsFilesConfigCreate(Prg)

import test_util, test_util_json

test_util.run_all_tests(Prg)
test_util_json.run_all_tests(Prg)
util_test.result_all(Prg)
