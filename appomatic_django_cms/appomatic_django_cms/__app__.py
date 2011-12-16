INSTALLED_APPS += ['cms',
                   'menus',
                   'mptt',
                   'south',
                   'cms.plugins.text',
                   'cms.plugins.picture',
                   'cms.plugins.link',
                   'cms.plugins.file',
                   'cms.plugins.snippet',
                   'cms.plugins.googlemap',
                   'sekizai']

MIDDLEWARE_CLASSES = ['cms.middleware.page.CurrentPageMiddleware',
                      'cms.middleware.user.CurrentUserMiddleware',
                      'cms.middleware.toolbar.ToolbarMiddleware']

TEMPLATE_CONTEXT_PROCESSORS = ['cms.context_processors.media',
                               'sekizai.context_processors.sekizai']
