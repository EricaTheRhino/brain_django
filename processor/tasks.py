import celery
from processor.views import handle_event
from celery.utils.log import get_task_logger
import requests
from pyga.requests import Tracker, Event, Session, Visitor
import datetime

logger = get_task_logger(__name__)

@celery.task(name="tasks.trigger_idle")
def trigger_idle():
	handle_event('brain.idle', {})
	return True

@celery.task(name="tasks.trigger_reset")
def trigger_reset():
	handle_event('brain.reset', {})
	return True

@celery.task(name="tasks.trigger_hour")
def trigger_hour():
	h = datetime.datetime.now().hour
	handle_event('brain.hour', {'hour':h})
	return True

@celery.task(name="tasks.async_post")
def async_post(url, json):
	requests.post(url=url, data=json)
	return True

@celery.task(name="tasks.trigger_event")
def trigger_event(event, params):
	handle_event(event, params)
	return True

@celery.task(name="tasks.ga")
def ga(event):

	session = Session()
	visitor = Visitor()
	tracker = Tracker('UA-42388606-1')

	label = event.split(".")[-1]
	category = ".".join(event.split(".")[0:-1])

	event = Event(category, label)
	tracker.track_event(event, session, visitor)
	return True
