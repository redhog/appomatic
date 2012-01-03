import cms.models
import tagging
import tagging.fields
import django.db.models

cms.models.Page.add_to_class('tag_field', tagging.fields.TagField(default=''))
tagging.register(cms.models.Page)


class TaggedList(cms.models.CMSPlugin):
    tag_field = tagging.fields.TagField()

    def copy_relations(self, oldinstance):
        self.tags = oldinstance.tags.all()

tagging.register(TaggedList)
