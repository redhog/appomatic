import django.conf.urls

urlpatterns = django.conf.urls.patterns('',
    (r'^ckeditor/', django.conf.urls.include('ckeditor.urls'))
)
