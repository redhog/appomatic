from django.contrib.auth.models import User
from django.contrib import admin

class Application(User):
    class Meta:
        proxy = True

admin.site.register(Application)
