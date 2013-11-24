#!/usr/bin/env python3

import time
from housepy import osc, util, log


score = [   [1.0, 'A'],
            [2.0, 'B'],
            [3.0, 'C'],
            [4.0, 'D']
            ]


score = []
delay = 5
for i in range(300):
# for i in range(10):
    t = delay + (i / 2)
    score.append((t, 'n'))


sender = osc.Sender()
sender.add_target('localhost', 5280)
sender.add_target('192.168.2.2', 5280)
sender.add_target('192.168.2.3', 5280)

data = []
t = util.timestamp(ms=True)
for n in score:
    data.append(str(n[0] + t))
    data.append(n[1])

log.debug(data)

sender.send('/client/cues', data)

