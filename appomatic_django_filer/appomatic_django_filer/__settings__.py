THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
) + get_app_config_list('THUMBNAIL_PROCESSORS')

FILER_STATICMEDIA_PREFIX = STATIC_URL + "/filer/"
