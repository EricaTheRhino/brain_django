#!/usr/bin/python

import cherrypy
import simplejson
import requests
from component import *
import RPi.GPIO as GPIO
import time
from threading import Thread

CIRCLE = 1600
MIN_SPEED = 0.001
MAX_SPEED = 0.0006

def dostep(params, rate=MIN_SPEED):
	GPIO.output(params['step'],GPIO.HIGH)
	time.sleep(rate)
	GPIO.output(params['step'],GPIO.LOW)
	time.sleep(rate)
	params = checkstate(params)
	return params


def homeear(params, rate=MIN_SPEED):
	GPIO.output(params['dir'],0)
	print "DIR=" + str(params['dirval'])
	inhome=GPIO.input(params['home'])
	for i in range(4000):
		params = dostep(params, rate)
		# If in range of magnet then...
		if GPIO.input(params['home']) == 1:
			# If we started non-homed, then move the ear to a starting point(?)
			if inhome == 0:
				GPIO.output(params['dir'],params['homeoffsetdir'])
				for i in range(params['homeoffset']):
					params = dostep(params, rate)
				print "have homed ear"
				return params
		else:
			# No longer in magnet range.
			if inhome == 1:
				inhome=0
	return params


def rotate(params, angle, rate=MIN_SPEED):
	distance = angle * (CIRCLE/360)
	if distance < 0:
		distance = distance*-1
		dir = 1
	else:
		dir = 0
	GPIO.output(params['dir'], dir)
	for j in range(distance):
		params = dostep(params, rate)
	return params
	
def waggle(params, angle, rate=MIN_SPEED):
	distance = angle * (CIRCLE/360)
	params = rotate(params, angle, rate)
	params = rotate(params, -angle, rate)
	return params

def checkstate(params):
	if GPIO.input(params['home']) != params['homeold']:
		params['homeold']=GPIO.input(params['home'])
		print "HOME=" + str(params['homeold'])
	if GPIO.input(params['on']) != params['onold']:
		params['onold']=GPIO.input(params['on'])
		print "ON=" + str(params['onold'])
 	return params

def init(params):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(params['dir'], GPIO.OUT)
	GPIO.setup(params['step'], GPIO.OUT)
	GPIO.setup(params['on'], GPIO.IN)
	GPIO.setup(params['home'], GPIO.IN)
	GPIO.output(params['dir'],GPIO.LOW)
	params = homeear(params, MAX_SPEED)

