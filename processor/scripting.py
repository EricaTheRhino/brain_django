import celery
import redis
import requests
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from processor.models import Component, Tweet
import time
from decimal import *
import logging
import random
import mosquitto
from twython import Twython
logger = logging.getLogger(__name__)

r = redis.StrictRedis(host='localhost', port=6379, db=0)
getcontext().prec = 2
MAX_STAT = Decimal('6.0')
MIN_STAT = Decimal('0.0')
TWEET_RATE = 60*60 # 1 hour
MAX_TWEETS = 10 # 10 per day

# MQTT Stuff
global mqtt
mqtt = mosquitto.Mosquitto("brain")
	
def flush():
	r.flushdb()
	return True

def get_mood_matrix():
	return {
		'e':['asleep','sleepy','tired','awake','alert','active','hyperactive'],
		'f':['starving','hungry','peckish','satisfied','full','well_fed','stuffed'],
		'i':['very_bored','bored','curious','interested','fascinated','enthused','very_interested'],
		'm':['teary','unhappy','sad','content','happy','very_happy','overjoyed']
	}


def key_to_eng(key):
	trans = {
		'very_happy': 'Very Happy',
		'very_interested': 'Very Interested',
		'very_bored': 'Very Bored',
		'well_fed': 'Well Fed'
	}
	if key in trans:
		return trans[key]
	else:
		return key.title()

def get_mood_stats():
	vals = {
		'e':int(round(get_stat('energy'))),
		'f':int(round(get_stat('fullness'))),
		'i':int(round(get_stat('interest'))),
		'm':int(round(get_stat('mood'))),
	}

	return vals

def get_mood_atoms():
	matrix = get_mood_matrix()
	vals = get_mood_stats()
	e = vals['e']
	f = vals['f']
	i = vals['i']
	m = vals['m']

	atoms = []
	for x in ['e', 'f', 'i', 'm']:
		atoms.append(matrix[x][vals[x]])

	return atoms

def get_mood_map():
	matrix = get_mood_matrix()
	vals = get_mood_stats()

	e = vals['e']
	f = vals['f']
	i = vals['i']
	m = vals['m']

	result = {}
	for x in ['e', 'f', 'i', 'm']:
		result[x] = {'val':vals[x], 'text':key_to_eng(matrix[x][vals[x]]), 'mood':matrix[x][vals[x]], 'percent':round(vals[x]/Decimal('6.0')*100)}
	return result


def get_latest():
	short_term = get_short_term()
	latest = short_term[0]
	return latest

def get_prev(event):
	for ev in get_short_term()[1:]:
		if ev['event'] == event:
			return ev
	return None

def get_delta(event, curr=None):
	if curr == None:
		curr = time.time()
	last_ts = r.hget('last_trigger', event)
	if last_ts != None:
		return curr - float(last_ts)
	else:
		return 0

def get_in_last(t, event=None):
	events = []
	curr = time.time()
	for ev in get_short_term():
		if event == None or ev['event'] == event:
			d = curr - ev['created']
			if d < t:
				events.append(ev)
	return events

def get_short_term():
	memory = r.lrange('short_term', 0, -1)
	short_term = []
	for memory_json in memory:
		memory_obj = simplejson.loads(memory_json)
		short_term.append(memory_obj)
	return short_term

def get_long_term():
	long_term = {}
	for key in r.hkeys('long_term'):
		long_term[key] = r.hget('long_term', key)
	return long_term

def inc_stat(key, delta='1'):
	delta = Decimal(delta)
	val = Decimal(get_stat(key))
	if (val+delta) <= MAX_STAT:
		val = set_stat(key, val+delta)
	else:
		val = set_stat(key, MAX_STAT)
	return Decimal(val)

def dec_stat(key, delta='1'):
	delta = Decimal(delta)
	val = Decimal(get_stat(key))
	if (val-delta) > MIN_STAT:
		val = set_stat(key, val-delta)
	else:
		val = set_stat(key, MIN_STAT)
	return Decimal(val)

def set_stat(key, value):
	v = Decimal(value)
	r.hset('stats', key, v)
	mqtt_pubstat(key, v)
	return v

def mqtt_connect():
	mqtt.connect("localhost")
    
def mqtt_disconnect():
	mqtt.disconnect()

def mqtt_pubstat(key,value):
	keys = {'energy':'e','fullness':'f','interest':'i','mood':'m'}
	if keys.has_key(key):
		matrix = get_mood_matrix()
		val = int(round(value))
		x = keys[key]
		d = {key:{'val':value, 'text':key_to_eng(matrix[x][val]), 'mood':matrix[x][val], 'percent':round(value/Decimal('6.0')*100)}}
		mqtt_connect()
		mqtt.publish('erica/stats',simplejson.dumps(d))
		mqtt_disconnect()

def mqtt_pubevent(event,params,text):
	d = {'event':event, 'text':text, 'params': params}
	mqtt_connect()
	mqtt.publish('erica/event',simplejson.dumps(d))
	mqtt_disconnect()

def mqtt_puballstats():
	matrix = get_mood_matrix()
	vals = get_mood_stats()

	keys = {'energy':'e','fullness':'f','interest':'i','mood':'m'}
	
	result = {}
	for key in keys:
		x = keys[key]
		result[key] = {'val':vals[x], 'text':key_to_eng(matrix[x][vals[x]]), 'mood':matrix[x][vals[x]], 'percent':round(vals[x]/Decimal('6.0')*100)}

	#print all stats as retained topic
	mqtt_connect()
	mqtt.publish('erica/stats',simplejson.dumps(result), 0, True)
	mqtt_disconnect()


def get_mood():
	return r.hget('stats', 'moodkey')

def set_mood(value):
	r.hset('stats', 'moodkey', value) 

def get_moods():
	return r.lget('moods')

def set_moods(moods):
	r.delete('moods')
	for idx, mood in enumerate(moods):
		r.lpush('moods', mood)

def get_stat(key):
	val = r.hget('stats', key)
	if not val:
		return Decimal(0.0)
	else:
		return Decimal(val)

def log(message):
	r.lpush('log', message)
	r.ltrim('log', 0, 9)

def trigger(cmd, data, async=False):
	# Locate the component
	pieces = cmd.split('.')
	if len(pieces) == 1:
		logger.info("Invalid command "+cmd)
		return False
	try:
		component = Component.objects.get(name=pieces[0])
	except ObjectDoesNotExist:
		logger.info("Component does not exist: "+pieces[0])
		return False

	d = {'command':cmd, 'data':data}
	logger.info("Task: "+str(d))
	json = simplejson.dumps(d)
	if async:
		print "Send async task to", component.url
		celery.execute.send_task("tasks.async_post", [component.url, json])
	else:
		print "Send sync task to ", component.url
		print "JSON: ", json
		requests.post(url=component.url, data=json)
	
	return True

def tweet(key):
	# Twitter limits:
	# * Only tweet MAX_TWEET times per day
	# * Have a gap of at least TWEET_RATE between tweets

	r = redis.StrictRedis(host='localhost', port=6379, db=0)
	if not r.exists('last_tweet'):
		r.set('last_tweet', 0)
		
	last_tweet = int(r.get('last_tweet'))
	
	now = int(time.time())

	# Ensure we're onto our next tweet 'slot'.
	if now > last_tweet + TWEET_RATE:
		# Make sure we haven't already tweeted this tweet today.
		if not r.sismember("tweets", key):
			tweets = r.smembers("tweets")
			# Make sure we haven't reached our tweet limit.
			if len(tweets) < MAX_TWEETS:
				r.sadd("tweets", key)
				r.set('last_tweet', now)

				# Grab a tweet from the DB
				tweets = Tweet.objects.filter(key=key)
				count = tweets.count()
				tweet = tweets[random.randint(0, count-1)]

				# Actually perform the tweet here.
				print "Tweet "+tweet.content
				twitter = Twython(settings.APP_KEY, settings.APP_SECRET, settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)
				twitter.update_status(status=tweet.content)
