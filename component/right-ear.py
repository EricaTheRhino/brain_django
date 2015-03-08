#!/usr/bin/python

import cherrypy
import simplejson
import requests
from component import *
import RPi.GPIO as GPIO
import time
from threading import Thread
from ear import *

right = {
	'dir':18,
	'step':17,
	'on':4,
	'home':24,
	'homeoffset':300,
	'homeoffsetdir':1,
	'dirval':0,
	'homeold':0,
	'onold':0,
}

class RightEarComponent(RhinoComponent):

	@cherrypy.expose
	def commands(self):
		global right		
	 	body = simplejson.loads(cherrypy.request.body.read())
		data = body['data']
		rate = 0
		if 'speed' in data:
			rate = data['speed']
		speed = rate * (MAX_SPEED - MIN_SPEED) + MIN_SPEED 

		if body['command'] == 'rightear.servo.rotate':
			right = rotate(right, data['angle'], speed)
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'rightear.servo.waggle':
			right = waggle(right, data['angle'], speed)
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'rightear.servo.home':
			right = homeear(right, speed)
			return simplejson.dumps({'result':'success'})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'rightear',
	'host':'mech.ericatherhino.local',
	'port': 8010
}

init(right)
c = RightEarComponent()
c.setup(config)
