#!/usr/bin/env python

import sys
sys.path.append('/home/pi/Downloads/CRTApp')

import CRT

try:
    CRT()
except:
    print "DON'T CLOSE"
