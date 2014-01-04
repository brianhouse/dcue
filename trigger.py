#!/usr/bin/env python3

from housepy import osc

# cue = [[5.0, 'train.mp3']]
cue = 'stop'

osc.Sender(23232).send('/trigger', cue)