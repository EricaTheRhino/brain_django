import cherrypy
import simplejson
import requests
from time import sleep
from cherrypy.process.plugins import Daemonizer
import os
d = Daemonizer(cherrypy.engine)
d.subscribe()
cherrypy.engine.autoreload.unsubscribe()
BRAIN_URL = 'http://brain.ericatherhino.local'

class RhinoComponent(object):

	@cherrypy.expose
	def index(self):
		return "<html><body><h1>Rhino Component: "+self.config['name']+"</h1></body></html>"

	def setup(self, config):
		self.config = config
		cherrypy.server.socket_port = self.config['port']
		cherrypy.server.socket_host = self.config['host']
		self.url = 'http://'+self.config['host']+':'+str(self.config['port'])
		connected = False
		while True:
			try:
				r = requests.post(url=BRAIN_URL+'/register/', data=simplejson.dumps({'url':self.url+'/commands', 'name':self.config['name']}))
				break
			except:
				print "Can't connect to brain. Retrying."
				sleep(3)
				continue

		cherrypy.quickstart(self)
