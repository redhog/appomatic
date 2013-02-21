from django.conf import settings
import os.path

try:
    # Django < 1.5
    from django.conf.urls.defaults import *
except:
    # Django >= 1.5
    from django.conf.urls import *

urlpatterns = patterns('',
    *(url(r'^', include('%s.__urls__' % (app['NAME'],)))
      for app in settings.APPOMATIC_APP_PARTS
      if os.path.exists(os.path.join(app['PATH'], '__urls__.py')))
)

if settings.DEBUG:
    urlpatterns = urlpatterns + patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    )
