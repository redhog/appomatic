# -*- coding: utf-8 -*-
from south.db import db
import tagging.fields

class Migration:    
    def forwards(self, orm):
        db.add_column('cms_page', 'tag_field', tagging.fields.TagField(default=''))
        
    def backwards(self, orm):
        db.delete_column('cms_page', 'tag_field')
