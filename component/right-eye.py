#!/usr/bin/python

import cherrypy
import simplejson
import requests
from component import *

class RightEyeComponent(RhinoComponent):


	@cherrypy.expose
	def commands(self):
		EYE_URL = 'http://right-eye.ericatherhino.local:8182/'
	 	body = simplejson.loads(cherrypy.request.body.read())
		data = body['data']

		if body['command'] == 'righteye.lights.blink':
			requests.post(EYE_URL+'lights/blink', data={'time':data['time']})
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'righteye.lights.level':
			requests.post(EYE_URL+'lights/level', data={'level':data['level']})
			return simplejson.dumps({'result':'success'})
		elif body['command'] == 'righteye.servo.direction':
			requests.post(EYE_URL+'servo/direction', data={'dir':data['dir']})
			return simplejson.dumps({'result':'success'})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'righteye',
	'host':'right-eye.ericatherhino.local',
	'port': 8000
}

c = RightEyeComponent()
c.setup(config)

