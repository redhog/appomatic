from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
import os.path

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    *(url(r'^', include('%s.__urls__' % (app['NAME'],)))
      for app in settings.LOCAL_APPS
      if os.path.exists(os.path.join(app['PATH'], '__urls__.py')))
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns

