
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

could it be timestamp?

could try time.time()