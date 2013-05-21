from django.conf.urls import patterns, include

urlpatterns = patterns(
    '',
    (r'^accounts/', include('userena.urls'))
)
