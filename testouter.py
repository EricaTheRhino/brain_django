# simple test of PIR pin

# This sets up django env

import sys
import os

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

from processor import views
import RPi.GPIO as GPIO
import time
import requests
import json
import threading
####################
#pin definitions
####################

# chin
Apin = 24
Bpin = 25

# chip
Chipcenterpin=22
Chipoutsidepin=23

GPIO.setmode(GPIO.BCM)
GPIO.setup(Chipoutsidepin,GPIO.IN)

Chipoutsidecur=0
def trigger(ev, args):
	thr = threading.Thread(target=views.handle_event, args=[ev, args])
	thr.start()

print "Ready"
while True:
	Chipoutside=GPIO.input(Chipoutsidepin)

	if( Chipoutside != Chipoutsidecur ):
		print("Chipoutside="+str(Chipoutside))
		Chipoutsidecur=Chipoutside
		trigger('interaction.chip', {'button':'outside', 'state':Chipoutside})
	time.sleep(0.1)

