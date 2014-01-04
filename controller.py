#!/usr/bin/env python3

import time, threading
from housepy import osc, util, log, config

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
        syncbox = cls.get(data[0], ip)
        syncbox.alive = True

    @classmethod
    def send(cls, score):
        data = []
        t = util.timestamp(ms=True)
        for cue in score:
            log.debug(cue)
            data.append(str(cue[0] + t))
            data.append(cue[1])
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


def message_handler(ip, address, data):
    if address == '/health':
        Syncbox.message(ip, address, data)
    elif address == '/trigger':
        if data[0] == 'stop':
            Syncbox.stop()
        else:
            Syncbox.send((data,))
    else:
        log.error("Unknown message %s from %s" % (address, location))

osc.Receiver(23232, message_handler, blocking=True)
