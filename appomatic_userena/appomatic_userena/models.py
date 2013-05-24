from django.utils.translation import ugettext as _
import userena.models
import django.contrib.auth.models
import django.db.models

class Profile(userena.models.UserenaBaseProfile):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        unique=True,
        verbose_name=_('user'),
        related_name='profile')
