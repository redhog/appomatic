from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from models import TaggedList
from django.utils.translation import ugettext as _
import cms.models
import tagging.models

class CMSTaggedListPlugin(CMSPluginBase):
    model = TaggedList
    name = _("Article list by tag")
    render_template = "cms_tagging/tagged_list.html"

    def render(self, context, instance, placeholder):
        context.update({
            'object':instance,
            'tagged_pages': tagging.models.TaggedItem.objects.get_union_by_model(cms.models.Page, instance.tags),
            'placeholder':placeholder
        })
        return context

plugin_pool.register_plugin(CMSTaggedListPlugin)
