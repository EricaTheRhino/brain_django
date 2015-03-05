#!/usr/bin/python

import cherrypy
import simplejson
from component import *
import rhinolights
import PITLC5940.LED as LED

class HornComponent(RhinoComponent):


	def __init__(self):
		self.controller = rhinolights.initiliserhinoleds(rhinolights.HORN)
		#self.controller.setconfig(*rhinolights.neutral())
		self.controller.setconfig(*rhinolights.blends(xrate=0.1,yrate=0.5))
		self.current = "off"
		RhinoComponent.__init__(self)

	@cherrypy.expose
	def commands(self):
	 	body = simplejson.loads(cherrypy.request.body.read())
		print "Hi there"
		print body
		if body['command'] == 'horn.colours':
			data = body['data']
			theme = data['theme'] # e.g. 'fire'
			time = data['time'] # in ms
			if not 'rate' in data:
				rate = 0.5
			else:
				rate = data['rate'] # activity value 0-6
			# Call function here to do magic.
			if True:#not theme == self.current:
				self.current = theme
				if theme == 'fire':
					rhinolights.solid(self.controller,R=3000)
				elif theme == 'ice':
					rhinolights.solid(self.controller,B=3000)
				elif theme == 'grass':
					rhinolights.solid(self.controller,G=3000)
				elif theme == 'hues':
					rhinolights.hues(self.controller,rate)
					#self.controller.setmode(rhinolights.verticialblends())						
			return simplejson.dumps({'result':'success', 'body':body})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'horn',
	'host':'localhost',
	'port': 8003
}


c = HornComponent()
c.setup(config)
