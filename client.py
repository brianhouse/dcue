#!/usr/bin/env python3

import time, subprocess, platform, sched
from collections import deque
from housepy import osc, util, log

def get_t():
    return util.timestamp(ms=True)
scheduler = sched.scheduler(get_t, time.sleep)

def play(sound=None):    # should be threaded
    try:
        if platform.system() == "Darwin":
            subprocess.check_call("afplay left.wav", shell=True)    
        elif platform.system() == "Linux":
            subprocess.check_call("aplay left.wav", shell=True)    
    except Exception as e:
        log.error(log.exc(e))

def message_handler(location, address, data):
    if address != '/client/cues':
        return
    ts = [float(d) for i, d in enumerate(data) if i % 2 == 0]
    ns = [       d for i, d in enumerate(data) if i % 2 == 1]
    for cue in deque(zip(ts, ns)):
        scheduler.enterabs(cue[0], 1, play)
    scheduler.run()     # blocking, this has to be addressed somehow if new messages come in

osc.Receiver(5280, message_handler, blocking=True)




