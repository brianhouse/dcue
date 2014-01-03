#!/usr/bin/env python3

import time, subprocess, platform, sched, threading, queue
from collections import deque
from housepy import osc, util, log, config

def get_t():
    return util.timestamp(ms=True)
scheduler = sched.scheduler(get_t, time.sleep)

class Health(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sender = osc.Sender(config['central'], 23232)
        self.start()        

    def run(self):
        while True:
            self.sender.send("/health", config['name'])
            time.sleep(config['health_rate'])

health = Health()            

class Player(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.queue = queue.Queue()
        self.start()

    def run(self):
        while True:
            sound = self.queue.get()
            try:
                if platform.system() == "Darwin":
                    subprocess.check_call("afplay snd/%s" % sound, shell=True)    
                elif platform.system() == "Linux":
                    bn = "mpg123" if sound[-3:] == "mp3" else "aplay"
                    subprocess.check_call("%s snd/%s" % (bn, sound), shell=True)
            except Exception as e:
                log.error(log.exc(e))

player = Player()

def play(sound):
    player.queue.put(sound)

def message_handler(location, address, data):
    if address != '/client/cues':
        return
    ts = [float(d) for i, d in enumerate(data) if i % 2 == 0]
    ns = [       d for i, d in enumerate(data) if i % 2 == 1]
    for cue in deque(zip(ts, ns)):
        scheduler.enterabs(cue[0], 1, play, (cue[1],))
    scheduler.run()     # blocking, this has to be addressed somehow if new messages come in

osc.Receiver(5280, message_handler, blocking=True)

