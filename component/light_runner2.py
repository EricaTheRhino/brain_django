#!/usr/bin/python
# -*- coding: utf-8 -*-
from ola.ClientWrapper import ClientWrapper
import time
import array
import random
import sys
import select
import string
import logging
logging.basicConfig(filename='/tmp/light.log', level=logging.DEBUG)

# Global vars
wrapper = None
TICK_INTERVAL = 1000
update = True

# Horn LEDs
horn_index = {}
horn_index['red'] = [33,36,39,42,45,49,52,55,58,61,65,68,71,74,77]
horn_index['blue'] = [34,37,40,43,46,50,53,56,59,62,66,69,72,75,78]
horn_index['green'] = [35,38,41,44,47,51,54,57,60,63,67,70,73,76,79]
horn_leds = horn_index['red']
horn_theme = 'red'

# Body LEDs
left_body_colours = ['r','r','r','r','r','g','g','b','b','b','b','y','y','y','w','w']
left_body_positions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
right_body_colours = ['r','r','r','r','r','g','g','b','b','b','b','y','y','y','w','w']
right_body_positions = [32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17]
body_colours = left_body_colours + right_body_colours
body_positions = left_body_positions + right_body_positions
body_index = { 'red':[], 'green':[], 'blue':[], 'yellow':[], 'white':[] }
for i in range(len(body_positions)):
        if body_colours[i] == 'r':
                body_index['red'].append(body_positions[i]);
        elif body_colours[i] == 'g':
                body_index['green'].append(body_positions[i]);
        elif body_colours[i] == 'b':
                body_index['blue'].append(body_positions[i]);
        elif body_colours[i] == 'y':
                body_index['yellow'].append(body_positions[i]);
        elif body_colours[i] == 'w':
                body_index['white'].append(body_positions[i]);
body_leds = body_index['white'] + body_index['red']
body_theme = 'white_red'


def DmxSent(state):
	if not state.Succeeded():
		wrapper.Stop()

def SendDMXFrame():
	global theme
	global update
	global horn_leds
	global body_leds
	wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
	if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		theme = sys.stdin.readline().strip()
		if theme:
			theme_bits = theme.split('.')
			if theme_bits[0] == 'horn':
				hornTheme(theme_bits[1])
			elif theme_bits[0] == 'body':
				bodyTheme(theme_bits[1])

	if update: 
		leds = horn_leds + body_leds
		data = array.array('B')
		for i in range(1, 512):
			if i in leds:
				data.append(255)
			else:
				data.append(0)
		wrapper.Client().SendDmx(1, data, DmxSent)
		update = False

def hornTheme(sub_theme):
	global update
	global horn_index
	global horn_leds
	global horn_theme
	update_local = True
	leds = []
	sub_themes = [ 'red', 'green', 'blue', 'christmas', 'pink', 'aqua', 'ice' ]
	if sub_theme == 'random':
		new_sub_theme = random.choice(sub_themes)
		while new_sub_theme == horn_theme:
			new_sub_theme = random.choice(sub_themes)
		sub_theme = new_sub_theme
	if sub_theme == 'red':
 	        horn_leds = horn_index['red']
        elif sub_theme == 'green':
                horn_leds = horn_index['green']
        elif sub_theme == 'blue':
                horn_leds = horn_index['blue']
        elif sub_theme == 'christmas':
                horn_leds = horn_index['red'] + horn_index['green']
        elif sub_theme == 'pink':
                horn_leds = horn_index['red'] + horn_index['blue']
        elif sub_theme == 'aqua':
                horn_leds = horn_index['green'] + horn_index['blue']
        elif sub_theme == 'ice':
                horn_leds = horn_index['green'] + horn_index['blue'] + horn_index['red']
        elif sub_theme == 'off':
                horn_leds = []
	else:
		update_local = False
	if update_local:
		horn_theme = sub_theme
	update = update_local

def bodyTheme(sub_theme):
	global update 
	global body_index 
	global body_leds 
	global body_theme
        update = True
	body_theme = sub_theme
	sub_theme_bits = sub_theme.split('_')
	body_leds = []
	for colour in sub_theme_bits:
        	if colour == 'red':
                	body_leds += body_index['red']
        	elif colour == 'green':
                	body_leds += body_index['green']
        	elif colour == 'blue':
                	body_leds += body_index['blue']
        	elif colour == 'yellow':
                	body_leds += body_index['yellow']
        	elif colour == 'white':
                	body_leds += body_index['white']
	

wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
