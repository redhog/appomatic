INSTALLED_APPS = ['cmsplugin_phlog']
PRE = ['appomatic_photolog', 'appomatic_django_cms']
CMS_APPLICATIONS_URLS = (
    ('cmsplugin_phlog.urls', 'Photologue app'),
)
CMS_NAVIGATION_EXTENDERS = (
    ('cmsplugin_phlog.menu.get_nodes', 'Photologue app Navigation'),
)
