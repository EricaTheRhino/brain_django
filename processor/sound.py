import os

def play_sound(name):
	f = os.open('/tmp/soundpipe', os.O_WRONLY)
	os.write(f, name+"\n")
	os.close(f)

def play_qr_sound(text, default_sound):
	if text == "cricket":
		play_sound("cricket")
	elif text == "football":
		play_sound("football")
	elif text == "formula1":
		play_sound("formula1")
	elif text == "skiing":
		play_sound("skiing")
	elif text == "tennis":
		play_sound("tennis")
	else:
		play_sound(default_sound)

	
