#!/usr/bin/env python3

import time, threading, natsort
from housepy import osc, util, log, config

osc.verbose = False

class Syncbox:

    boxes = []
    sender = osc.Sender()

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.alive = True
        self.status = "ready"
        self.t = util.timestamp(ms=True)
        Syncbox.sender.add_target(self.ip, 5280)

    @classmethod
    def find(cls, name, ip):
        for syncbox in cls.boxes:
            if syncbox.name == name:
                if syncbox.ip != ip:
                    syncbox.ip = ip
                syncbox.t = time.time()
                return syncbox
        syncbox = Syncbox(name, ip)
        cls.boxes.append(syncbox)
        cls.boxes = natsort.natsorted(cls.boxes, key=lambda box: box.name)
        cls.boxes.reverse()
        return syncbox

    @classmethod
    def on_message(cls, ip, address, data):
        try:
            syncbox = cls.find(data[0], ip)            
            syncbox.alive = True
            syncbox.status = data[1]
        except Exception as e:
            log.error(log.exc(e))

    @classmethod
    def send(cls, score):
        data = []
        t = util.timestamp(ms=True)
        for cue in score:
            log.info("Sending %s" % (cue,))
            data.append(str(cue[0] + t))
            data.append(cue[1])
        cls.sender.send('/cue', score)

    @classmethod
    def stop(cls):
        log.info("Sending stop")
        cls.sender.send('/stop')

    def __repr__(self):
        if self.alive:
            return "%s(%s)" % (self.name, self.status)
        else:
            return "%s(%f)*" % (self.name, time.time() - self.t)    # sometimes this will end up showing a smaller delay than health_rate


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
        Syncbox.on_message(ip, address, data)
    elif address == '/trigger':
        if data[0] == 'stop':
            Syncbox.stop()
        else:
            Syncbox.send((data,))
    else:
        log.error("Unknown message %s from %s" % (address, location))

osc.Receiver(23232, message_handler, blocking=True)
