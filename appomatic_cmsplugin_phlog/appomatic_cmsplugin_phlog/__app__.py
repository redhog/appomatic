INSTALLED_APPS = ['cmsplugin_phlog']
PRE = ['appwrapper_photolog', 'appwrapper_cms']
CMS_APPLICATIONS_URLS = (
    ('cmsplugin_phlog.urls', 'Photologue app'),
)
CMS_NAVIGATION_EXTENDERS = (
    ('cmsplugin_phlog.menu.get_nodes', 'Photologue app Navigation'),
)
