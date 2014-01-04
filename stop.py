#!/usr/bin/env python3

from housepy import osc

cue = 'stop'

osc.Sender(23232).send('/trigger', cue)