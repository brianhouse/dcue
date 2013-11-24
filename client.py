#!/usr/bin/env python3

import time, subprocess, platform
from collections import deque
from housepy import osc, util, log

cues = []

def message_handler(location, address, data):
    global cues # questionably thread-safe
    if address != '/client/cues':
        return
    ts = [float(d) for i, d in enumerate(data) if i % 2 == 0]
    ns = [       d for i, d in enumerate(data) if i % 2 == 1]
    cues = deque(zip(ts, ns))
osc.Receiver(5280, message_handler)



while True:
    t = util.timestamp(ms=True)
    while len(cues) and cues[0][0] < t:
        cue = cues.popleft()
        try:
            if platform.system() == "Darwin":
                subprocess.check_call("afplay left.wav", shell=True)    
            elif platform.system() == "Linux":
                subprocess.check_call("afplay left.wav", shell=True)    
        except Exception as e:
            log.error(log.exc(e))
        log.info("Executing %s" % util.datestring(cue[0], ms=True))
    time.sleep(0.01)

