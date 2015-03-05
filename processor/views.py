import redis
import time
from django.utils import simplejson
from django.http import HttpResponse
from processor.models import RhinoScript, ComponentForm, Component
from django.core.files import File
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import logging
import hashlib
import glob
logger = logging.getLogger(__name__)
from processor.scripting import *
from processor.sound import *
import random
import time
from pyga.requests import Tracker, Session, Visitor, Event
import celery
import mosquitto

global mqtt

def process_event():
	# First work through the behaviours
	files = glob.glob(settings.ROOT_PATH+'/behaviours/*.py')
	files.sort()
	for filename in files:
		execfile(filename)

def handle_event(event, params):
	if event.startswith('interaction.'):
		celery.execute.send_task("tasks.ga", [event])
	at_time = time.time()
	if event == 'environment.bluetooth.found' or event == 'environment.bluetooth.lost':
		if 'address' in params:
			params['address'] = hashlib.sha1(params['address']+','+'rh1n0t3xt').hexdigest()
	
	memory_obj = {'event':event, 'params':params, 'created':at_time}
	memory_json = simplejson.dumps(memory_obj)

	# First update the various stats in redis.
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	p = r.pipeline()
	p.multi()
	
	# pushes a memory object to the memory list, then trims it down to 10 items.
	p.lpush('short_term', memory_json)
	p.ltrim('short_term', 0, 99)

	# Incrs the count of this item in long-term memory.
	p.hincrby('long_term', event, 1)
	# Store when the event last happened
	p.execute()
	
	#mqtt_connect()
	process_event()
	#mqtt_disconnect()
	
@csrf_exempt
def add_event(request):
	if request.method == 'GET':
		return HttpResponse("Please post to me!")
	elif request.method == 'POST':
		data = simplejson.loads(request.body)
		if not 'event' in data or not 'params' in data:
			return HttpResponse("Invalid parameters (need event and params)")
		handle_event(data['event'], data['params'])
		return HttpResponse(simplejson.dumps({'result':'success'}), mimetype='application/json')

@csrf_exempt
def get_state(request):
	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	memory = r.lrange('short_term', 0, -1)
	short_term = []
	for memory_json in memory:
		memory_obj = simplejson.loads(memory_json)
		short_term.append(memory_obj)

	logs = r.lrange('log', 0, -1)
	messages = []
	for log in logs:
		messages.append(log)

	mood_keys = r.lrange('moods', 0, -1)
	moods = []
	for mood_key in mood_keys:
		moods.append(mood_key)

	long_term = {}
	last_trigger = {}
	for key in r.hkeys('long_term'):
		long_term[key] = r.hget('long_term', key)

	for key in r.hkeys('last_trigger'):
		last_trigger[key] = r.hget('last_trigger', key)

	# Get stats
	stats = {}
	for key in r.hkeys('stats'):
		stats[key] = r.hget('stats', key)
	return HttpResponse(simplejson.dumps({'result':'success', 'messages':messages, 'short_term':short_term, 'long_term':long_term, 'moods':moods,  'last_trigger':last_trigger, 'stats':stats}), mimetype='application/json')

@csrf_exempt
def register_component(request):
	data = simplejson.loads(request.body)
	if not 'url' in data:
		return HttpResponse(simplejson.dumps({'result':'failure', 'reason':'missing_url'}), mimetype='application/json')

	if not 'name' in data:
		return HttpResponse(simplejson.dumps({'result':'failure', 'reason':'missing_name'}), mimetype='application/json')


	# TODO: Check that it validates before deleting old components
	Component.objects.filter(name=data['name']).delete()
	form = ComponentForm({'url':data['url'], 'name':data['name']})
	if form.is_valid():
		new_component = form.save()
		return HttpResponse(simplejson.dumps({'result':'success'}))
	else:
		return HttpResponse(simplejson.dumps({'result':'failure', 'reason':'invalid_data'}), mimetype='application/json')
