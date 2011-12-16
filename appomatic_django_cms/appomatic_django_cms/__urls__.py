from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^', include('cms.urls')),
)
