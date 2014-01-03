#!/usr/bin/env python3

import time, subprocess, platform, threading, queue
from collections import deque
from housepy import osc, util, log, config

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
        self.process = None
        self.start()

    def run(self):
        while True:
            sound = self.queue.get()
            try:
                if platform.system() == "Darwin":
                    bn = "afplay"
                elif platform.system() == "Linux":
                    bn = "mpg123" if sound[-3:] == "mp3" else "aplay"
                self.process = subprocess.Popen([bn, 'snd/%s' % sound])
            except Exception as e:
                log.error(log.exc(e))

    def stop(self):
        # this is not strictly thread-safe, is it?
        try:
            self.process.terminate()
        except Exception as e:
            log.error(log.exc(e))

player = Player()


timers = []
def message_handler(ip, address, data):
    if address == '/cue':
        try:
            ts = [float(d) for i, d in enumerate(data) if i % 2 == 0]
            ns = [       d for i, d in enumerate(data) if i % 2 == 1]
            for cue in deque(zip(ts, ns)):
                timer = threading.Timer(cue[0], player.queue.put, (cue[1],)).start()
                timers.append(timer)
        except Exception as e:
            log.error(log.exc(e))
    elif address == '/stop':
        player.stop()
        for timer in timers:
            timer.cancel()
    else:
        log.error("Unknown comand (%s)" % address)
        return

osc.Receiver(5280, message_handler, blocking=True)

