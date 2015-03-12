#!/var/www/brain/venv/bin/python
# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

import json
import random

import sys
import os
fpid = os.fork()
if fpid != 0:
	sys.exit(0)

from settings import settings as twitter_settings

proj_path = '/var/www/brain/'
prev_sys_path = list(sys.path)
sys.path.insert(0, proj_path + 'venv/lib/python2.7/site-packages')
# re-order sys.path so that new directories are at the front
new_sys_path = []
for item in list(sys.path):
  if item not in prev_sys_path:
    new_sys_path.append(item)
    sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.insert(0,'/var/www/')
sys.path.insert(0,'/var/www/brain/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'brain.settings'
from django.conf import settings
from processor import tasks

follow_replies = ['Thanks for following!', 'Nice to meet you!', 'Delighted to make your acquaintance!']
api = None

def send_event(name, params):
    try:
	print "Trigger event",name
	tasks.trigger_event.apply_async(args=[name, params])
    except Exception, e:
	print "Error!!!", e

class StdOutListener(StreamListener):
	def on_data(self, data):
            tweet = json.loads(data)
	    if 'event' in tweet:
		if tweet['event'] == 'follow':
		    api.update_status('@'+tweet['source']['screen_name']+' '+random.choice(follow_replies))
		    send_event('twitter.follow', {})
	    elif 'text' in tweet and tweet['in_reply_to_screen_name'] == 'EricaTheRhino':
		send_event('twitter.mention', {})
		text = tweet['text'].lower()
		colours = ["blue", "red", "green", "christmas", "ice", "aqua", "pink"]
		for colour in colours:
		    if colour in text:
			send_event('twitter.colour', {'colour':colour})
			break
		return True

	def on_error(self, status):
		print status

print "Starting up..."
l = StdOutListener()
auth = OAuthHandler(twitter_settings['CONSUMER_KEY'], twitter_settings['CONSUMER_SECRET'])
auth.set_access_token(twitter_settings['OAUTH_TOKEN'], twitter_settings['OAUTH_SECRET'])
api = tweepy.API(auth)
stream = Stream(auth, l)
stream.userstream()
