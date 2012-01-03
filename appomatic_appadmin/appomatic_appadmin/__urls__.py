from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^admin/appomatic_appadmin/application/?$', 'appomatic_appadmin.views.index'),
    (r'^admin/appomatic_appadmin/application/add/?$', 'appomatic_appadmin.views.add'),
    (r'^admin/appomatic_appadmin/application/action/?$', 'appomatic_appadmin.views.action'),
    (r'^admin/appomatic_appadmin/application/progress/(?P<pid>.*)/?$', 'appomatic_appadmin.views.progress'),
    (r'^admin/appomatic_appadmin/application/(?P<app_name>\w+)/$', 'appomatic_appadmin.views.details'),
)
