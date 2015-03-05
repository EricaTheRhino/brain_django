#!/usr/bin/python

import datetime
import math
#import thread
import TLC5940
from multiprocessing import Process, Queue, Manager
import time

def millis():
   dt = datetime.datetime.now()
   ms = (dt.second) * 1000 + dt.microsecond / 1000.0
   return ms


######################################
# led functions
######################################

def breathe(period, maxbrightness, minbrightness=0, offset=0,  *other, **kwargs):
	rate=2*math.pi/period
	brightness=maxbrightness-minbrightness
	return int((brightness*(math.sin(float(millis()*rate)-offset)+1)/2)+minbrightness)


def blink(period,ontime,offset,brightness, *other, **kwargs):
	blinkprogress = (int(millis())-offset) % period 
	if blinkprogress >= ontime:
		return 0
	else:
		return brightness

def hueblend(period,offset,brightness,colour, *other, **kwargs):
	# colour acts as angle offset

	if colour == 1:
		coloffset = 0
	elif colour == 2:
		coloffset = 120
	elif colour == 3:
		coloffset = 240


	progress = (int(millis())+offset) % period 
	deg = (float(progress) / float(period) * float(360) + float(coloffset))%360
	#print deg

	# create blends
	if deg < 60:
		val=brightness
	elif ((deg >= 60) and (deg < 120)):
		val=brightness - (((deg - 60) * brightness)/60) #drops
	elif ((deg >= 120) and (deg < 240)):
		val=0
	elif ((deg >= 240) and (deg < 300)):
		val=((deg - 240) * brightness)/60 # rises
	elif (deg >= 300):
		val=brightness

	return int(val)


def off(*other, **kwargs):
	return 0

def constant(value, *other, **kwargs):
	return value 

###################################
# led mode mixers
###################################


	
def pulse(mode0,mode0settings,mode1,mode1settings,pulsesettings,ledid, *other):
	endtime = pulsesettings[0]
	now=millis()
	if now >= endtime: 
		instance.clearmixer(ledid,0)
		return mode0(*mode0settings)
	else:
		return mode1(*mode1settings)

def modeblend(mode0,mode0settings,mode1,mode1settings,blendsettings,ledid, *other):
	starttime = blendsettings[0]
	endtime = blendsettings[1]

	now=millis()
	if now <= starttime:
		return mode0(*mode0settings)
	else:
		if now >= endtime:
			instance.clearmixer(ledid,1)
			return mode1(*mode1settings)
		else:
			progress=(now-starttime)/(endtime-starttime)
			outgoing=(1-progress)*mode0(*mode0settings)
			incoming=progress*mode1(*mode1settings)
			return int(outgoing+incoming)

###################################
# mixer mode helpers
###################################

def setmixer(ledid,newmode,newmodesettings,mixer,mixersettings):
	oldmode=mode[ledid]
	oldsettings=settings[ledid]
	mode[ledid]=mixer
	settings[ledid]=(oldmode,oldsettings,newmode,(newmodesettings),(mixersettings),ledid)

def setmodemixer(data,mixer,mixersettings):
	for i in range(len(settings)):
		setmixer(i,data[0][i],data[1][i],mixer,mixersettings)

def clearmixer(ledid,new):
	if new==1:
		mode[ledid]=settings[ledid][2]
		settings[ledid]=settings[ledid][3]
	else:
		mode[ledid]=settings[ledid][0]
		settings[ledid]=settings[ledid][1]


###################################
# led processing commands
###################################


def ledcontroler( count):

	brightness = [0]*16*count
	mode = [off]*16*count
	settings = [(0,)]*16*count

	PIPE = "/tmp/hornpipe"
	try:
		os.unlink(PIPE)
	except OSError, e:
		if e.errno != errno.ENOENT:
			raise
	os.mkfifo(PIPE)
	os.chmod(PIPE, 0666)
	io = os.open(PIPE, os.O_RDONLY)
	f = os.fdopen(io)

	while True:
		(mode, settings) = pickle.load(f)
		for i in range(len(settings)):
			brightness[i]=mode[i](*(settings[i]))
		TLC5940.setTLCvalue(TLC5940.buildvalue(brightness,TLC5940.regPWM),TLC5940.regPWM)


controller.ledcontroler(3)

if __name__ == "__main__":
	# run a simple test of breathe animation
	
	print "test where out of date and have been removed"
