#!/usr/bin/env python3


while True:
    time.sleep(

            try:
                command = "arecord -D plughw:1,0 -d 30 -f S16_LE -c1 -r11025 -t wav audio_tmp/%s.wav" % t  # 30s of mono 11k PCM
                log.info("%s" % command)
                subprocess.check_call(command, shell=True)    
            except Exception as e:
                log.error(log.exc(e))
                time.sleep(1)
                continue
        

class Driver(object):

    def __init__(self):
        self.voices = []
        self.grain = 0.01   # hundredths are nailed by Granu, w/o load. ms are ignored.
        self.t = 0.0
        self.previous_t = 0.0
        self.callbacks = []
        self.running = True

    def start(self, skip=0):
        start_t = time.time() - skip
        last_cue = -1
        while self.running:
            self.t = time.time() - start_t
            if int(self.t) // 15 != last_cue:
                last_cue = int(self.t) // 15
                log.info("/////////////// [%s] %d:%f ///////////////" % (last_cue, self.t // 60.0, self.t % 60.0))                        
            controller.perform_callbacks()
            self._perform_callbacks()
            if not self.running:
                break
            delta_t = self.t - self.previous_t
            for voice in self.voices:
                voice.update(delta_t)
            self.previous_t = self.t                
            time.sleep(self.grain)