#!/usr/bin/python
# -*- coding: utf-8 -*-
from ola.ClientWrapper import ClientWrapper
import array
import sys
import select

theme = 'on'
wrapper = None
loop_count = 0
TICK_INTERVAL = 10

# colours

l_colours = ['r','r','r','r','r','g','g','b','b','b','b','y','y','y','w','w']
l_position = [0, 1, 7, 5, 8, 9, 14, 2, 11, 6, 12, 3, 13, 15, 10, 4] 

# After N ms, LED fades in 
# After N ms, LED fades out
static = True

frames = []
def init_frames():
	for j in range(0, 16):
		led_frames = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		frames.append(led_frames)

def off():
	init_frames()
	for j in range(0, 16):
		frames[j] = [0]

def on():
	init_frames()
	for j in range(0, 16):
		frames[j] = [255]

def twinkle_l_r():
	init_frames()
	for i in range(0, 16):
		led = l_position[i]
		frames[led][(i-1)%16] = 128
		frames[led][i] = 255
		frames[led][(i+1)%16] = 128

def twinkle_r_l():
	init_frames()
	for i in range(0, 16):
		led = l_position[15-i]
		frames[led][(i-1)%16] = 128
		frames[led][i] = 255
		frames[led][(i+1)%16] = 128

def calc_fade_in(x, y, ms):
	ticks = ms / TICK_INTERVAL
	per_frame = (y-x)/ticks
	out = array()
	for i in range(x, y, per_frame):
		out.append(i)
	return out

frame = 0

def update_leds():
	data = array.array('B')
	for i in range(0, 15):
		data.append(frames[i][frame])
	return data

def DmxSent(state):
	if not state.Succeeded():
		wrapper.Stop()

def SendDMXFrame():
	global theme
	global frame
	wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
	changed = False
	if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
		theme = sys.stdin.readline().strip()
		if theme:
			frame = 0
			changed = True
			if theme == 'twinklel':
				twinkle_l_r()
			elif theme == 'twinkler':
				twinkle_r_l()
			elif theme == 'on':
				on()
				wrapper.Client().SendDmx(1, update_leds(), DmxSent)
			elif theme == 'off':
				off()
				wrapper.Client().SendDmx(1, update_leds(), DmxSent)
	if theme != 'on' and theme != 'off':
		data = update_leds()
		frame = frame + 1
		if frame == len(frames[0]):
			frame = 0
		wrapper.Client().SendDmx(1, data, DmxSent)

on()
wrapper = ClientWrapper()
wrapper.AddEvent(TICK_INTERVAL, SendDMXFrame)
wrapper.Run()
