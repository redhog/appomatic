# -*- coding: utf-8 -*-
import os
import os.path
import sys
import itertools

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

def get_app(name):
    try:
        with open(os.path.join(PROJECT_DIR, 'apps', name, '__app__.py')) as f:
            res = {'NAME': name, 'INSTALLED_APPS': [name]}
            exec f in res
            return res
    except Exception, e:
        print "Error loading app %s: %s" % (name, e)
        return None
def app_cmp(a, b):
    if (   a['NAME'] in b.get('POST', [])
        or b['NAME'] in a.get('PRE', [])):
        return 1
    elif (   b['NAME'] in a.get('POST', [])
          or a['NAME'] in b.get('PRE', [])):
        return -1
    return 0
LOCAL_APPS = [app
              for app in (get_app(name)
                          for name in os.listdir(os.path.join(PROJECT_DIR, 'apps')))
              if app]
LOCAL_APPS.sort(app_cmp)
def get_app_config_list(config_name):
    return tuple(value
                 for value in itertools.chain.from_iterable(app.get(config_name, [])
                                                            for app in LOCAL_APPS))



DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'mycms.db'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'gig3(ofdyzr_g*lj-%uzh&k3ct2_y1cgh4h5321*xf8fnybd%k'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
) + get_app_config_list('MIDDLEWARE_CLASSES')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
) + get_app_config_list('TEMPLATE_CONTEXT_PROCESSORS')

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.comments',
) + get_app_config_list('INSTALLED_APPS')

for app in LOCAL_APPS:
    p = os.path.join(PROJECT_DIR, 'apps', app['NAME'], '__settings__.py')
    if os.path.exists(p):
        with open(p) as f:
            exec f
