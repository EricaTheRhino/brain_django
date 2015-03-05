# coding: utf-8

import random
import time
latest = get_latest()

if latest['event'] == 'interaction.righteye.face' or latest['event'] == 'interaction.lefteye.face':
	inc_stat('mood', '0.3')
	inc_stat('interest', '0.5')
	eyeside = '';
	if latest['event'] == 'interaction.righteye.face':
		trigger('righteye.lights.blink', {'time':300}, True)
		eyeside = 'right'
	elif latest['event'] == 'interaction.lefteye.face':
		trigger('lefteye.lights.blink', {'time':300}, True)
		eyeside = 'left'
	mqtt_pubevent(latest['event'], latest['params'], 'Hello! Just seen someone on my ' + eyeside + '!');
	play_sound('beep')
