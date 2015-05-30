# This sets up django env

import sys
import os

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
from processor import views
print "Start"
views.handle_event('interaction.pir.detect', {'state':0})
