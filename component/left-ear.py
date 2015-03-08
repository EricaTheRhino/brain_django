#!/usr/bin/python

import cherrypy
import simplejson
import requests
from component import *
import RPi.GPIO as GPIO
import time
from threading import Thread
from ear import *

left = {
	'dir':22,
	'step':27,
	'on':4,
	'home':23,
	'homeoffset':100,
	'homeoffsetdir':1,
	'dirval':0,
	'homeold':0,
	'onold':0,
}

class LeftEarComponent(RhinoComponent):

	@cherrypy.expose
	def commands(self):
		global left		
	 	body = simplejson.loads(cherrypy.request.body.read())
		data = body['data']
		rate = 0
		if 'speed' in data:
			rate = data['speed']
		speed = rate * (MAX_SPEED - MIN_SPEED) + MIN_SPEED 

		if body['command'] == 'leftear.servo.rotate':
			left = rotate(left, data['angle'], speed)
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'leftear.servo.waggle':
			left = waggle(left, data['angle'], speed)
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'leftear.servo.home':
			left = homeear(left, speed)
			return simplejson.dumps({'result':'success'})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'leftear',
	'host':'mech.ericatherhino.local',
	'port': 8000
}

init(left)
c = LeftEarComponent()
c.setup(config)

