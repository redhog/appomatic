import os
import sys

activate_this = '/home/test/myprofile/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Just make sure print statements won't crash the thing...
sys.stdout = open("/dev/null", "a")

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
  #change to 'prod' in production
  os.environ['APP_ENVIR'] = 'test'
  return _application(environ, start_response)
