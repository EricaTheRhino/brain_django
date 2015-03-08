#!/usr/bin/python
import subprocess
import cherrypy
import simplejson
import os
import logging
from component import *
#import rhinolights
#import PITLC5940.LED as LED

dir = str(os.path.dirname(os.path.realpath(__file__)))
logging.basicConfig(filename=dir + "/logs/lights.log", level=logging.DEBUG)

class LightsComponent(RhinoComponent):

	def __init__(self):
		#self.controller = rhinolights.initiliserhinoleds(rhinolights.BODY)
		#rhinolights.breathing(self.controller,rhinolights.BODY)
		#self.p = subprocess.Popen(['python', dir + '/light_runner2.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
		self.current = "off"
		RhinoComponent.__init__(self)


	@cherrypy.expose
	def commands(self):
	 	body = simplejson.loads(cherrypy.request.body.read())
		if body['command'] == 'lights.colours':
			data = body['data']
			theme = data['theme'] # e.g. 'fire'
			themebits = theme.split('.')
			if ( self.current != theme or themebits[1] == "random" ):
				self.current = theme
				logging.debug("THEME: "+theme)
				#self.p.stdin.write(theme+"\n")
				subprocess.call(['/bin/bash', dir + '/set_theme.bash', themebits[0], themebits[1]])
			return simplejson.dumps({'result':'success', 'body':body})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'lights',
	'host':'mech.ericatherhino.local',
	'port': 8003
}



c = LightsComponent()
c.setup(config)


