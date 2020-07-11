#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file starts sentence-seeker without
# python console with tkinter gui by default

import os, sys

DirPrgParent = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DirPrgParent)

__import__("sentence-seeker")
