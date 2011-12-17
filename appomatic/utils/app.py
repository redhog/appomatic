import pkg_resources
import pip.util
import appomatic.utils.topsort
import os.path

def get_pip_apps(prefix = ''):
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
            yield name

def get_app(name):
    try:
        mod = __import__(name)
        path = os.path.dirname(mod.__file__)
        with open(os.path.join(path, '__app__.py')) as f:
            res = {'NAME': name, 'INSTALLED_APPS': [name], 'PATH': path}
            exec f in res
            return res
    except Exception, e:
        print "Error loading app %s: %s" % (name, e)
        return None

def apps_to_parent_child_list(apps):
    for app in apps:
        for child in app.get('POST', []):
            yield (app['NAME'], child)
        for parent in app.get('PRE', []):
            yield (parent, app['NAME'])

def sort_apps(apps):
    apps_by_name = dict((app['NAME'], app) for app in apps)
    return [apps_by_name[name]
            for name in appomatic.utils.topsort.topsort(apps_to_parent_child_list(apps_by_name.itervalues()))]

def get_apps(names):
    return sort_apps(app
                     for app in (appomatic.utils.app.get_app(name)
                                 for name in names)
                     if app)
