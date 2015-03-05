import cherrypy
import simplejson
from component import *

class VideoComponent(RhinoComponent):

	@cherrypy.expose
	def commands(self):
	 	body = simplejson.loads(cherrypy.request.body.read())
		if body['command'] == 'video.something':
			data = body['data']
			return simplejson.dumps({'result':'success', 'body':body})
		else:
			return simplejson.dumps({'result':'failure', 'body':body})

config = {
	'name':'video',
	#'host':'brain.ericatherhino.text',
	'host':'localhost',
	'port': 81
}

c = VideoComponent()
c.setup(config)
