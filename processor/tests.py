"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import simplejson

class EventTest(TestCase):
	def test_send_event(self):
		self.client.post('/events/', simplejson.dumps({'event':'vision.scanned_item', 'params':{'item':'leaf'}}), content_type='text/json')
		self.client.post('/events/', simplejson.dumps({'event':'vision.scanned_item', 'params':{'item':'cake'}}), content_type='text/json')
		self.client.post('/events/', simplejson.dumps({'event':'vision.motion', 'params':{'position':'left'}}), content_type='text/json')

class ComponentTest(TestCase):
	def test_register(self):
		self.client.post('/register/', simplejson.dumps({'url':'http://foo.com/', 'name':'test'}), content_type='text/json')