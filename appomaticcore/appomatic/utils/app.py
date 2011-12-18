import pkg_resources
import pip.util
import appomatic.utils.topsort
import os
import os.path

def get_pip_apps(prefix = 'appomatic_'):
    # This is mostly copied from pip.commands.freeze
    dependency_links = []
    for dist in pkg_resources.working_set:
        if dist.has_metadata('dependency_links.txt'):
            dependency_links.extend(dist.get_metadata_lines('dependency_links.txt'))
    installations = {}
    for dist in pip.util.get_installed_distributions(local_only=True):
        req = pip.FrozenRequirement.from_dist(dist, dependency_links, find_tags=False)
        installations[req.name] = req
    for installation in sorted(installations.values(), key=lambda x: x.name):
        name = installation.name.replace("-", "_")
        if name.startswith(prefix):
            yield {'NAME': name, 'SOURCE': 'pip/local'}

def get_dir_apps(dirname):
    if os.path.isdir(dirname):
        return ({'NAME': name, 'SOURCE': 'dir' + os.path.abspath(dirname)} for name in os.listdir(dirname))
    return []

def load_app(app):
    try:
        mod = __import__(app['NAME'])
        app['PATH'] = os.path.dirname(mod.__file__)
        with open(os.path.join(app['PATH'], '__app__.py')) as f:
            app['INSTALLED_APPS'] = [app['NAME']]
            exec f in app
            return app
    except Exception, e:
        print "Error loading app %s: %s" % (app['NAME'], e)
        return None

def apps_to_parent_child_list(apps):
    for app in apps:
        for child in app.get('POST', []):
            yield (app['NAME'], child)
        for parent in app.get('PRE', []):
            yield (parent, app['NAME'])
        yield (app['NAME'], None) # Include apps with no dependency info

def sort_apps(apps):
    apps_by_name = dict((app['NAME'], app) for app in apps)
    return [apps_by_name[name]
            for name in appomatic.utils.topsort.topsort(apps_to_parent_child_list(apps_by_name.itervalues()))
            if name in apps_by_name]

def load_apps(apps):
    return sort_apps(loaded_app
                     for loaded_app in (appomatic.utils.app.load_app(app)
                                        for app in apps)
                     if loaded_app)
