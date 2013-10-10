# -*- coding: utf-8 -*-
import os
import os.path
import sys
import itertools
import appomatic.utils.app

VIRTUALENV_DIR = os.environ['VIRTUAL_ENV']
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

APP_DIR = os.path.join(VIRTUALENV_DIR, "apps")
sys.path.append(APP_DIR)

if os.environ.keys().count("PYTHONPATH") == 0 :
    os.environ["PYTHONPATH"] = ""

def get_app_config_list(config_name):
    return tuple(value
                 for value in itertools.chain.from_iterable(app.get(config_name, [])
                                                            for app in APPOMATIC_APP_PARTS))

APPOMATIC_APPS = appomatic.utils.app.load_apps(
    list(appomatic.utils.app.get_pip_apps())
    + list(appomatic.utils.app.get_dir_apps(APP_DIR)))

APPOMATIC_APP_PARTS = appomatic.utils.app.sort_apps(APPOMATIC_APPS)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VIRTUALENV_DIR, 'appomatic.db'),
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
MEDIA_ROOT = os.path.join(VIRTUALENV_DIR, 'media')
if not os.path.exists(MEDIA_ROOT): os.makedirs(MEDIA_ROOT)

STATIC_ROOT = os.path.join(VIRTUALENV_DIR, 'static')
if not os.path.exists(STATIC_ROOT): os.makedirs(STATIC_ROOT)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

STATICFILES_DIRS = get_app_config_list('STATICFILES_DIRS')

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

import django
if django.VERSION[0] >= 1 and django.VERSION[1] >= 4:
    TEMPLATE_CONTEXT_PROCESSOR_AUTH = 'django.contrib.auth.context_processors.auth'
else:
    TEMPLATE_CONTEXT_PROCESSOR_AUTH = 'django.core.context_processors.auth'

TEMPLATE_CONTEXT_PROCESSORS = (
    TEMPLATE_CONTEXT_PROCESSOR_AUTH,
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
) + get_app_config_list('TEMPLATE_CONTEXT_PROCESSORS')

ROOT_URLCONF = 'appomatic.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
) + get_app_config_list('INSTALLED_APPS')

for part in APPOMATIC_APP_PARTS:
    p = os.path.join(part['PATH'], '__settings__.py')
    if os.path.exists(p):
        with open(p) as f:
            exec f

if DEBUG:
    print "Installed apps: " + ', '.join(app['NAME'] for app in APPOMATIC_APPS)
    print "  Parts: " + ', '.join(part['NAME'] for part in APPOMATIC_APP_PARTS)
