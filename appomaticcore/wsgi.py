# SETUPTOOLS_DO_NOT_WRAP
import os
import os.path
import sys
import logging

# Workaround for Google App Engine (and its dev environment)
if 'PATH' not in os.environ:
    os.environ['PATH'] = ''

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

import appomatic
sys.path[0:0] = [os.path.dirname(appomatic.__file__)]

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'


# Stubs for Google App Engine (and its dev environment)
try:
    import pwd
except:
    import appomatic.utils.pwd_stub
    sys.modules['pwd'] = appomatic.utils.pwd_stub
try:
    import _sysconfigdata_nd
except:
    import appomatic.utils.sysconfig_stub
    sys.modules['sysconfig'] = appomatic.utils.sysconfig_stub

# Just make sure print statements won't crash the thing...
try:
    sys.stdout = open("/dev/null", "a")
except:
    # This will happen on Google App Engine
    import StringIO
    sys.stdout = StringIO.StringIO()


import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
  #change to 'prod' in production
  os.environ['APP_ENVIR'] = 'test'
  return _application(environ, start_response)
