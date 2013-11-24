#!/usr/bin/env python3

import time
from collections import deque
from housepy import osc, util, log

cues = []

def message_handler(location, address, data):
    global cues
    if address != '/client/cues':
        return
    ts = [float(d) for i, d in enumerate(data) if i % 2 == 0]
    ns = [       d for i, d in enumerate(data) if i % 2 == 1]
    cues = deque(zip(ts, ns))
    log.debug(cues)
osc.Receiver(5280, message_handler)


while True:
    t = util.timestamp(ms=True)
    while len(cues) and cues[0][0] < t:
        cue = cues.popleft()
        log.info("Executing %s" % cue[1])
    time.sleep(0.001)

