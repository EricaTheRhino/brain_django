import os
import sys
import site

proj_path = '/home/pi/ecsrhino/brain/'

prev_sys_path = list(sys.path)
site.addsitedir(proj_path + 'venv/lib/python2.7/site-packages')

# re-order sys.path so that new directories are at the front
new_sys_path = []
for item in list(sys.path):
  if item not in prev_sys_path:
    new_sys_path.append(item)
    sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.insert(0,'/home/pi/ecsrhino/')
sys.path.insert(0,'/home/pi/ecsrhino/brain/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'brain.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import djcelery
djcelery.setup_loader()

