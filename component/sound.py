#!/usr/bin/python

import cherrypy
import simplejson
from component import *

class SoundComponent(RhinoComponent):
	def __init__(self):
		self.f = os.open('/tmp/soundpipe', os.O_WRONLY)
		RhinoComponent.__init__(self)

	@cherrypy.expose
	def commands(self):
	 	body = simplejson.loads(cherrypy.request.body.read())
		if body['command'] == 'sound.play':
			data = body['data']
			os.write(self.f, data['name']+"\n")
			return simplejson.dumps({'result':'success', 'body':body})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'sound',
	#'host':'brain.ericatherhino.text',
	'host':'localhost',
	'port': 8001
}

c = SoundComponent()
c.setup(config)

