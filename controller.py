#!/usr/bin/env python3

import time, threading
from housepy import osc, util, log, config

# naming scheme for syncboxes via physical location?


class Syncbox:

    boxes = []
    sender = osc.Sender()

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.alive = True
        self.t = util.timestamp(ms=True)
        Syncbox.sender.add_target(self.ip, 5280)

    @classmethod
    def get(cls, name, ip):
        for syncbox in cls.boxes:
            if syncbox.name == name:
                syncbox.t = time.time()
                return syncbox
        syncbox = Syncbox(name, ip)
        cls.boxes.append(syncbox)
        cls.boxes.sort(key=lambda box: box.name)
        return syncbox

    @classmethod
    def message(cls, ip, address, data):
        if address == "/health":
            syncbox = cls.get(data[0], ip)
            syncbox.alive = True
        else:
            log.error("Unknown message %s from %s" % (address, location))

    @classmethod
    def send(cls, score):
        data = []
        t = util.timestamp(ms=True)
        for n in score:
            data.append(str(n[0] + t))
            data.append(n[1])
        log.debug(data)        
        cls.sender.send('/cue', score)

    @classmethod
    def stop(cls):
        cls.sender.send('/stop')

    def __repr__(self):
        if self.alive:
            return "%s(%s)" % (self.name, self.alive)
        else:
            return "%s(%f)*" % (self.name, time.time() - self.t)


class Expiry(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            t = util.timestamp(ms=True)
            for syncbox in Syncbox.boxes:
                if t - syncbox.t > config['health_rate']:
                    syncbox.alive = False
            time.sleep(config['health_rate'])                    
Expiry()


class Monitor(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            log.info(Syncbox.boxes)
            time.sleep(config['health_rate'])
Monitor()


osc.Receiver(23232, Syncbox.message)


time.sleep(2)

score = [ [1.0, 'train.mp3'] ]

Syncbox.send(score)

time.sleep(5)

Syncbox.stop()


while True:
    time.sleep(1)