#!/usr/bin/env python3

import sys
from housepy import osc

try:
    track = sys.argv[1]
except IndexError:
    print("[track]")
    exit()

cue = [[25.0, track]]

osc.Sender(23232).send('/trigger', cue)