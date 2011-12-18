CMS_TEMPLATES = (
    ('example.html', 'Example Template'),
)+ get_app_config_list('CMS_TEMPLATES')
CMS_APPLICATIONS_URLS = get_app_config_list('CMS_APPLICATIONS_URLS')
CMS_NAVIGATION_EXTENDERS = get_app_config_list('CMS_NAVIGATION_EXTENDERS')
