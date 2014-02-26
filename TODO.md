8:

2014-02-25 16:19:40,536 |INFO| OSC send (1): /health ['sb-8', 'loaded'] <osc.py:71>
[module.c:142] error: Failed to open module jack: file not found
[module.c:142] error: Failed to open module portaudio: file not found
[pulse.c:84] error: Failed to open pulse audio output: Connection refused
[module.c:142] error: Failed to open module nas: file not found
[module.c:142] error: Failed to open module openal: file not found
[audio.c:180] error: Unable to find a working output module in this list: alsa,oss,jack,portaudio,pulse,nas,openal
[audio.c:532] error: Failed to open audio output module
[mpg123.c:897] error: Failed to initialize output, goodbye.
2014-02-25 16:19:45,549 |INFO| OSC send (1): /health ['sb-8', 'playing'] <osc.py:71>
2014-02-25 16:19:50,562 |INFO| OSC send (1): /health ['sb-8', 'playing'] <osc.py:71>


///


loaded doesnt clear with stop

we want the queue to always empty when it gets something new

should sort the names

why does alive sometimes not work with <5?
