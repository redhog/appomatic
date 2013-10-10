import os.path

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, "uploads")
if not os.path.exists(CKEDITOR_UPLOAD_PATH): os.makedirs(CKEDITOR_UPLOAD_PATH)

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Full': [
            ['Styles', 'Format', 'Bold', 'Italic', 'Underline', 'Strike', 'TextColor', 'BGColor'],
            ['Link', 'Unlink', '-', 'Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Source', 'SpellChecker', 'Undo', 'Redo'],
            ],
        'toolbar': 'Full',
        'height': 291,
        'width': 835,
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
    },
    'small': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', 'Format', 'Bold', 'Italic', '-', 'Link', 'Unlink']
            ],
        'toolbar': 'Basic',
        'height': 150,
        'width': 400,
        'filebrowserWindowWidth': 940,
        'filebrowserWindowHeight': 725,
'removePlugins': 'elementspath,wordcount',
'resize_enabled': False
    },

}
