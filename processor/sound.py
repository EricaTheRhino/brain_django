import os

def play_sound(name):
	f = os.open('/tmp/soundpipe', os.O_WRONLY)
	os.write(f, name+"\n")
	os.close(f)
