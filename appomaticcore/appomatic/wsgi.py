import os
import os.path
import sys

def find_virtualenv(path = __file__):
    while path and path != '/':
        if os.path.exists(os.path.join(path, 'bin/activate_this.py')):
            return path
        path = os.path.dirname(path)
    raise Exception("Unable to find virtualenv (you must have moved wsgi.py outside the virtualenv!).")

virtualenv = find_virtualenv()
activate = os.path.join(virtualenv, 'bin/activate_this.py')
execfile(activate, dict(__file__=activate))
os.environ['VIRTUAL_ENV'] = virtualenv

sys.path[0:0] = [os.path.dirname(__file__)]

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Just make sure print statements won't crash the thing...
sys.stdout = open("/dev/null", "a")

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
  #change to 'prod' in production
  os.environ['APP_ENVIR'] = 'test'
  return _application(environ, start_response)
