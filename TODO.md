
client listens for a cue
on cue, it plays a sequence


need health report mechanism


need to be able to cancel events



we should be at python 3.3 on the pis, sched is threadsafe in 3.3
http://www.raspberrypi.org/phpBB3/viewtopic.php?t=49023&p=382172


there is drift, but it seems to correct with new messages
so can send in chunks

drift very well might be caused with the playback? so thread that
no, still happens. why?

could have multiple schedulers, but potential thread issues with 3.2

could it be timestamp? no, no improvement with time.time.


hmm. could send in realtime, but then we have network latency issues.


is it getting worse the longer the pis run?
how fast does ntp update?
do we need an external clock?


ok, and one guy missed a cue. hmm.

//


conclusions -- will need more communication to ensure cues happen and are healthy
need to send cues in short chunks, which seem to work ok

drift is just the lameless of time.sleep, I guess.





