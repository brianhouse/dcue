#!/usr/bin/env python3

import time, subprocess, platform, threading, queue, os
from collections import deque
from housepy import osc, util, log, config, process

process.secure_pid(os.path.abspath(os.path.join(os.path.dirname(__file__), "run")))

log.info("--> controller is %s" % config['controller'])

class Health(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.sender = osc.Sender(config['controller'], 23232)
        self.queue = queue.Queue()
        self.start()        

    def run(self):
        loaded = False
        while True:
            status = None
            while True:
                try:
                    status = self.queue.get_nowait()
                    loaded = True if status == 'loaded' else False
                except queue.Empty:
                    break
            if status is None:
                status = "ready" if not loaded else "loaded"                    
            self.sender.send("/health", [config['name'], status])
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
                path = os.path.abspath(os.path.join(os.path.dirname(__file__), "snd", sound))
                self.process = subprocess.Popen([bn, path])
                health.queue.put('playing')
                while True:
                    # log.debug(self.process.poll())
                    if self.process.poll() is None:
                        health.queue.put('playing')
                        time.sleep(config['health_rate'])
                    else:
                        self.process = None
                        break                    
            except Exception as e:                
                log.error(log.exc(e))
                health.queue.put('playing failed')

    def stop(self):
        # this is not strictly thread-safe, is it? could poll and terminate collide?
        try:
            if self.process is not None:
                self.process.terminate()
            health.queue.put('stopped')
        except Exception as e:
            log.error(log.exc(e))
            health.queue.put('stop failed')

player = Player()


timers = []
def message_handler(ip, address, data):
    if address == '/cue':
        for timer in timers:    # clears currently loaded cues
            timer.cancel()
        try:
            ts = [float(d) for i, d in enumerate(data) if i % 2 == 0]
            ns = [       d for i, d in enumerate(data) if i % 2 == 1]
            for cue in deque(zip(ts, ns)):
                timer = threading.Timer(cue[0], player.queue.put, (cue[1],))
                health.queue.put('loaded')
                timers.append(timer)
                timer.start()
        except Exception as e:
            log.error(log.exc(e))
            health.queue.put('failed')
    elif address == '/stop':
        player.stop()
        for timer in timers:
            timer.cancel()
    else:
        log.error("Unknown comand (%s)" % address)
        return

osc.Receiver(5280, message_handler, blocking=True)

