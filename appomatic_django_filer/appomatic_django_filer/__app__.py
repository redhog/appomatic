INSTALLED_APPS = ["mptt", "easy_thumbnails", "filer"]

# Bug workaround for filer storing static files in /media, not /static
import filer
import os.path
STATICFILES_DIRS = [os.path.join(os.path.dirname(filer.__file__), 'media')]
