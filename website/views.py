from django.template import RequestContext
from django.shortcuts import render_to_response
from processor.models import RhinoScript, Component
from processor.scripting import get_mood_map, trigger, get_short_term, get_stat, get_in_last
from utils import mood_to_text
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import hashlib
import sys
import os


from processor.sound import *
import requests
from django.utils import simplejson

import logging
logger = logging.getLogger(__name__)

def home(request):
	redirect = request.GET.get('redirect', False)
#	lines = ["Touch my mouth to feed me!", "Look in my eyes and let me see you!", "Tickle my cheek to cheer me up!", 'Send me a tweet at @EricaTheRhino', "Check out my horn to see how I'm feeling!", '<img src="/static/img/qr.png"></img>&nbsp;<p>Show me a QR code and see what I can do!</p>']
	lines = ['<img src="/static/img/rounder.png" class="qr" width="200px" /><img src="static/img/smaller.png" class="qr" width="200px" /><img src="static/img/harder.png" class="qr" width="200px" /><img src="/static/img/colder.png" class="qr" width="200px" /><img src ="/static/img/faster.png" class="qr" width="200px" />&nbsp;<p>Try showing me some of these QR codes and see what my reaction is!</p>']

	return render_to_response('website/index.html', {'lines':lines}, context_instance=RequestContext(request))

def mood(request):
	mood_map = get_mood_map()
	return render_to_response('website/mood.html', {'mood_map':mood_map}, context_instance=RequestContext(request))

def mood_json(request):
        mood_map = get_mood_map()
	return HttpResponse(simplejson.dumps(mood_map, encoding='latin-1'), mimetype='application/json')

def volume(request):
        volume = os.popen("/usr/local/sbin/erica/volume_control get").read().strip()
	return HttpResponse(volume, mimetype='text/plain')

def volume_down(request):
	volume = os.popen("/usr/local/sbin/erica/volume_control down").read().strip()
        return HttpResponse(volume, mimetype='text/plain')
	
def volume_up(request):
	volume = os.popen("/usr/local/sbin/erica/volume_control up").read().strip()
        return HttpResponse(volume, mimetype='text/plain')

def credits(request):
	return render_to_response('website/credits.html', context_instance=RequestContext(request))

def touchscreen(request):
	return render_to_response('website/touchscreen.html', context_instance=RequestContext(request))

def success(request):
	return render_to_response('website/success.html', context_instance=RequestContext(request))

def ncsi(request):
	return render_to_response('website/ncsi.txt', context_instance=RequestContext(request))

def latest_events_json(request):
	events = get_short_term()
	events_hash = ""
	for i,e in enumerate(events):
		events_hash = events_hash + e['event']
	events_with_hash = {
		'hash': str(hashlib.md5(events_hash).hexdigest()),
		'events': events,
	}
	return HttpResponse(simplejson.dumps(events_with_hash, encoding='latin-1'), mimetype='application/json')

def fullness_message(request):
	fullness = get_stat('fullness')
	fullness_msg = ''
	if (fullness > 5):
		fullness_msg = 'Getting a quite full now (Definitely stop feeding me soon or I will embarrass myself)'
	elif (fullness > 4):
		fullness_msg = 'Getting a little full now (You should stop feeding me soon)'
	else:
		fullness_msg = 'Yum!'
	
	return HttpResponse(fullness_msg, mimetype='text/plain')

def tickle_message(request):
	tickles = get_in_last(300, 'interaction.chip.press')
	tickle_msg = ''
	if (len(tickles) > 10):
		tickle_msg = 'I have been tickled too much now :('
	else:
		tickle_msg = 'that tickles!'
	return HttpResponse(tickle_msg, mimetype='text/plain')

@login_required
@csrf_exempt
def trigger_cmd(request):
	params = simplejson.loads(request.POST.get('params'))
	trigger(params['command'], params['data'])
	return HttpResponse(simplejson.dumps({'result':'success'}), mimetype='application/json')

@login_required
@csrf_exempt
def get_eye_data(request):
	rlev_url ='http://right-eye:8182/lights/level'
	rdir_url ='http://right-eye:8182/servo/direction'
	llev_url ='http://left-eye:8182/lights/level'
	ldir_url ='http://left-eye:8182/servo/direction'

	# rlev_url = 'http://degas.ecs.soton.ac.uk/~jsh2/erica/get.php?eye=right&path=lights/level'
	# rdir_url = 'http://degas.ecs.soton.ac.uk/~jsh2/erica/get.php?eye=right&path=servo/direction'
	# llev_url = 'http://degas.ecs.soton.ac.uk/~jsh2/erica/get.php?eye=left&path=lights/level'
	# ldir_url = 'http://degas.ecs.soton.ac.uk/~jsh2/erica/get.php?eye=left&path=servo/direction'

	rlev = simplejson.loads(requests.get(rlev_url).text)
	llev = simplejson.loads(requests.get(llev_url).text)
	rdir = simplejson.loads(requests.get(rdir_url).text)
	ldir = simplejson.loads(requests.get(ldir_url).text)

	return HttpResponse(simplejson.dumps({
		'left':
			{
			'level':llev['level'], 
			'direction':ldir['dir']
			}, 
		'right':
			{'level':rlev['level'], 
			'direction':rdir['dir']
			}
		}), mimetype='application/json')

def get_eye_image(request, eye):
	res = requests.get("http://"+eye+"-eye:8182/image/current").content
	return HttpResponse(res, mimetype='image/jpeg')

@login_required
def panel(request):
	rhinoscripts = RhinoScript.objects.all().order_by('order')
	components = Component.objects.all().order_by('name')
	return render_to_response('website/panel.html', 
		{'rhinoscripts':rhinoscripts, 'components':components},
		context_instance=RequestContext(request))

@login_required
def board(request):
	components = Component.objects.all().order_by('name')
	return render_to_response('website/board.html', {'components':components},
		context_instance=RequestContext(request))

@login_required
@csrf_exempt
def play(request):
	play_sound(request.POST.get('name'))
	return HttpResponse(simplejson.dumps({'result':'success'}), mimetype='application/json')
