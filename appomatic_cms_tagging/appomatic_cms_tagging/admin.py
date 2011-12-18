from django.utils.translation import ugettext_lazy as _
import cms.admin.pageadmin

cms.admin.pageadmin.PageAdmin.add_fieldsets += [
    (_('Tags'), {'fields': ['tag_field']}),
]
cms.admin.pageadmin.PageAdmin.fieldsets += [
    (_('Tags'), {'fields': ['tag_field']}),
]
