#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys

DirTools = os.path.dirname(os.path.realpath(__file__))
DirPrgParent = os.path.join(DirTools, "..")

sys.path.append(os.path.join(DirPrgParent, "src"))

import config
##########################################################

Prg = config.prg_config_create()

# use argparse to detect options

# use json lib to manage book db

# receive file name/html address/web site dirname as input
# first, simple case: file name
# if gzipped, extract it
# save it into Documents dir
# insert book infos into db



