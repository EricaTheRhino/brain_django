#!/usr/bin/python

import os
import pygame.mixer
import sys
import time
import errno

fpid = os.fork()
if fpid != 0:
	sys.exit(0)

PIPE = '/tmp/soundpipe'
print "Initialising"
pygame.mixer.init()


sounds = {
	'Rhinoceros2':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros2.wav'),
	'Rhinoceros3':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros3.ogg'),
	'Rhinoceros4':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros4.wav'),
	'Rhinoceros5':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros5.wav'),
	'Rhinoceros6':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros6.wav'),
	'Rhinoceros7':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros7.wav'),
	'Rhinoceros8':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros8.wav'),
	'Rhinoceros10':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros10.ogg'),
	'Rhinoceros11':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros11.wav'),
	'Rhinoceros12':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros12.ogg'),
	'Rhinoceros13':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros13.wav'),
	'Rhinoceros14':pygame.mixer.Sound('/usr/local/share/erica/sounds/Rhinoceros14.wav'),
	'yawn':pygame.mixer.Sound('/usr/local/share/erica/sounds/yawn.ogg'),
	'fart':pygame.mixer.Sound('/usr/local/share/erica/sounds/fart.wav'),
	'sneeze':pygame.mixer.Sound('/usr/local/share/erica/sounds/sneeze.wav'),
	'snore':pygame.mixer.Sound('/usr/local/share/erica/sounds/snore.ogg'),
	'beep':pygame.mixer.Sound('/usr/local/share/erica/sounds/beep.ogg'),
	'camera':pygame.mixer.Sound('/usr/local/share/erica/sounds/camera.wav'),
	'fanfare':pygame.mixer.Sound('/usr/local/share/erica/sounds/fanfare.wav'),
	'tweet':pygame.mixer.Sound('/usr/local/share/erica/sounds/tweet.ogg'),
	'cricket': pygame.mixer.Sound('/usr/local/share/erica/sounds/cricket.wav'),
	'football':pygame.mixer.Sound('/usr/local/share/erica/sounds/football.wav'),
	'formula1':pygame.mixer.Sound('/usr/local/share/erica/sounds/formula1.wav'),
	'skiing':pygame.mixer.Sound('/usr/local/share/erica/sounds/skiing.wav'),
	'tennis':pygame.mixer.Sound('/usr/local/share/erica/sounds/tennis.wav'),
}

sounds['tweet'].set_volume(1.0)

print "Ready"
try:
	os.unlink(PIPE)
except OSError, e:
	if e.errno != errno.ENOENT:
		raise
os.mkfifo(PIPE)
os.chmod(PIPE, 0666)
io = os.open(PIPE, os.O_RDONLY)
f = os.fdopen(io)

fulltext = ""
while True:
	buffer = f.read(11)
	fulltext = fulltext + buffer
	npos = fulltext.find("\n")
	if npos != -1: 
		sound = fulltext[0:npos]
		fulltext = fulltext[npos+1:]
		if pygame.mixer.get_busy():
			# Drain rest of queue
			f.read()
		elif sound in sounds:
			sounds[sound].play()
	time.sleep(0.5)
