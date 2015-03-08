#!/usr/bin/python

import cherrypy
import simplejson
import requests
from component import *

class LeftEyeComponent(RhinoComponent):


	@cherrypy.expose
	def commands(self):
		EYE_URL = 'http://left-eye.ericatherhino.local:8182/'
	 	body = simplejson.loads(cherrypy.request.body.read())
		data = body['data']

		if body['command'] == 'lefteye.lights.blink':
			requests.post(EYE_URL+'lights/blink', data={'time':data['time']})
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'lefteye.lights.level':
			requests.post(EYE_URL+'lights/level', data={'level':data['level']})
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'lefteye.servo.direction':
			requests.post(EYE_URL+'servo/direction', data={'dir':data['dir']})
			return simplejson.dumps({'result':'success'})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'lefteye',
	'host':'left-eye.ericatherhino.local',
	'port': 8000
}

c = LeftEyeComponent()
c.setup(config)

