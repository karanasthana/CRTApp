#!/usr/bin/env python

import sys
sys.path.append('/home/pi/Downloads/CRTApp')

import main

try:
    main()
except:
    print "DON'T CLOSE"
