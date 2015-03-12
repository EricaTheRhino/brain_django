# simple test of PIR pin

# This sets up django env

import sys
import os

proj_path = '/var/www/brain/'
prev_sys_path = list(sys.path)
sys.path.insert(0, proj_path + 'venv/lib/python2.7/site-packages')
# re-order sys.path so that new directories are at the front
new_sys_path = []
for item in list(sys.path):
  if item not in prev_sys_path:
    new_sys_path.append(item)
    sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.insert(0,'/var/www/')
sys.path.insert(0,'/var/www/brain/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'brain.settings'
from django.conf import settings
# Now the main program

from processor import tasks
import RPi.GPIO as GPIO
import time
import requests
import json
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
GPIO.setup(Apin,GPIO.IN)
GPIO.setup(Bpin,GPIO.IN)
GPIO.setup(Chipcenterpin,GPIO.IN)
GPIO.setup(Chipoutsidepin,GPIO.IN)

Acur=0
Bcur=0
Chipcentercur=0
Chipoutsidecur=0

print "Ready"
while True:

	A=GPIO.input(Apin)
	B=GPIO.input(Bpin)
	Chipcenter=GPIO.input(Chipcenterpin)
	Chipoutside=GPIO.input(Chipoutsidepin)

	if( A != Acur ):
		print("A="+str(A))
		Acur=A
		tasks.trigger_event.apply_async(args=['interaction.chin', {'button':1, 'state':A}])
	if( B != Bcur ):
		print("B="+str(B))
		Bcur=B
		tasks.trigger_event.apply_async(args=['interaction.chin', {'button':2, 'state':B}])
	if( Chipcenter != Chipcentercur ):
		print("Chipcenter="+str(Chipcenter))
		Chipcentercur=Chipcenter
		tasks.trigger_event.apply_async(args=['interaction.chip', {'button':'center', 'state':Chipcenter}])
	if( Chipoutside != Chipoutsidecur ):
		print("Chipoutside="+str(Chipoutside))
		Chipoutsidecur=Chipoutside
		tasks.trigger_event.apply_async(args=['interaction.chip', {'button':'outside', 'state':Chipoutside}])
	time.sleep(0.1)

