#!/usr/bin/python
# simple test of PIR pin

# This sets up django env

import sys
import os
fpid = os.fork()
if fpid != 0:
	sys.exit(0)


proj_path = '/home/pi/ecsrhino/brain/'
prev_sys_path = list(sys.path)
sys.path.insert(0, proj_path + 'venv/lib/python2.7/site-packages')
# re-order sys.path so that new directories are at the front
new_sys_path = []
for item in list(sys.path):
  if item not in prev_sys_path:
    new_sys_path.append(item)
    sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.insert(0,'/home/pi/ecsrhino/')
sys.path.insert(0,'/home/pi/ecsrhino/brain/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'brain.settings'
from django.conf import settings
# Now the main program

from processor import tasks
import RPi.GPIO as GPIO
import time
import requests
import os
import random
####################
#pin definitions
####################

# chin
Apin = 24
Bpin = 25

# chip
Chipcenterpin=22
Chipoutsidepin=23

#pir

pirpin=27

GPIO.setmode(GPIO.BCM)
GPIO.setup(Apin,GPIO.IN)
GPIO.setup(Bpin,GPIO.IN)
GPIO.setup(Chipcenterpin,GPIO.IN)
GPIO.setup(Chipoutsidepin,GPIO.IN)
GPIO.setup(pirpin,GPIO.IN)

Acur=0
Bcur=0
Chipcentercur=0
Chipoutsidecur=0
pircur=0

last_chip = 0
last_chin = 0
last_pir = 0

CHIP_MAX = 3
CHIN_MAX = 3
PIR_MAX = 3 

def play_sound(name):
	f = os.open('/tmp/soundpipe', os.O_WRONLY)
	os.write(f, name+"\n")
	os.close(f)

print "Ready"

while True:

	A=GPIO.input(Apin)
	B=GPIO.input(Bpin)
	Chipcenter=GPIO.input(Chipcenterpin)
	Chipoutside=GPIO.input(Chipoutsidepin)
	pir=GPIO.input(pirpin)

	if( A != Acur ):
		Acur=A
		if A == 1:
			play_sound(random.choice(['Rhinoceros3', 'Rhinoceros2']))
			curr = time.clock()
			if curr - last_chin > CHIN_MAX:
				tasks.trigger_event.apply_async(args=['interaction.chin.press', {'button':1, 'state':A}])
				last_chin = curr
	if( B != Bcur ):
		Bcur=B
		if B == 1:
			play_sound(random.choice(['Rhinoceros3', 'Rhinoceros2']))
			curr = time.clock()
			if curr - last_chin > CHIN_MAX:
				tasks.trigger_event.apply_async(args=['interaction.chin.press', {'button':2, 'state':B}])
				last_chin = curr
	if( Chipcenter != Chipcentercur ):
		Chipcentercur=Chipcenter
		if Chipcenter == 1:
			play_sound(random.choice(['Rhinoceros3', 'Rhinoceros2']))
			curr = time.clock()
			if curr - last_chip > CHIP_MAX:
				tasks.trigger_event.apply_async(args=['interaction.chip.press', {'button':'center', 'state':Chipcenter}])
				last_chip = curr
	if( Chipoutside != Chipoutsidecur ):
		Chipoutsidecur=Chipoutside
		if Chipoutside == 1:
			play_sound(random.choice(['Rhinoceros3', 'Rhinoceros2']))
			curr = time.clock()
			if curr - last_chip > CHIP_MAX:
				tasks.trigger_event.apply_async(args=['interaction.chip.press', {'button':'outside', 'state':Chipoutside}])
				last_chip = curr
	if ( pir != pircur):
		pircur=pir
		if pir == 0:
			curr = time.clock()
			if curr - last_pir > PIR_MAX:
				tasks.trigger_event.apply_async(args=['interaction.pir.detect', {'state':pir}])
				last_pir = curr
	time.sleep(0.1)

