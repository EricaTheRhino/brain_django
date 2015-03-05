#!/usr/bin/python
# -*- coding: utf-8 -*-
from ola.ClientWrapper import ClientWrapper
import time
import array
import random
import sys
import select
import string
import logging
logging.basicConfig(filename='/tmp/light.log', level=logging.DEBUG)
led_id = sys.argv[1]

# Global vars
wrapper = None
TICK_INTERVAL = 1000
update = True

def DmxSent(state):
	if not state.Succeeded():
		wrapper.Stop()

def SendDMXFrame():
	global update
	wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
	if update: 
		data = array.array('B')
		print "turning on leds"
		for i in range(1, 512):
			if i == int(led_id):
				print "LED " + led_id + " being turned on"
				data.append(255)
			else:
				data.append(0)
		wrapper.Client().SendDmx(1, data, DmxSent)
		update = False

wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
