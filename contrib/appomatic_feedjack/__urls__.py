import django.conf.urls

urlpatterns = django.conf.urls.patterns('',
    (r'^feedjack/', django.conf.urls.include('feedjack.urls'))
)
