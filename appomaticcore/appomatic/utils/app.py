import pkg_resources
import pip.util
import appomatic.utils.topsort
import appomatic.utils.forrest
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

def get_dir_apps(dirname, prefix=''):
    if os.path.isdir(dirname):
        source =  "dir" + os.path.abspath(dirname)
        # Filter on __app__.py existence as an optimization....
        return ({'NAME': prefix + name, 'SOURCE': source}
                for name in os.listdir(dirname)
                if os.path.exists(os.path.join(dirname, name, '__app__.py')))
    return []

def load_app(app):
    try:
        mod = __import__(app['NAME'])
        for partname in app['NAME'].split('.')[1:]:
            mod = getattr(mod, partname)
        app['PATH'] = os.path.dirname(mod.__file__)
        with open(os.path.join(app['PATH'], '__app__.py')) as f:
            app['INSTALLED_APPS'] = [app['NAME']]
            exec f in app
            app['PARTS'] = []
            if app.get('HAS_PARTS', False):
                app['PARTS'] = load_apps(get_dir_apps(app['PATH'], app['NAME'] + "."))
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
        if not app.get('POST', []) and not app.get('PRE', []):
            yield (app['NAME'], ":" + app['NAME']) # Include apps with no dependency info

def parent_child_list_handle_start_end(lst):
    lst = list(lst)
    def find_extension(lst, name):
        trees = appomatic.utils.forrest.find_trees(lst)
        if name in trees:
            for root, nodes in trees.iteritems():
                if root == name:
                    continue
                for node in nodes:
                    yield (node, name)
    def inverse(lst):
        return [(child, parent) for (parent, child) in lst]
    return lst + list(find_extension(lst, '__end__')) + inverse(find_extension(inverse(lst), '__start__'))

def sort_apps(apps):
    apps_by_name = {}

    def recurse(apps):
        for app in apps:
            apps_by_name[app['NAME']] = app
            recurse(app['PARTS'])
    recurse(apps)

    return [apps_by_name[name]
            for name in appomatic.utils.topsort.topsort(parent_child_list_handle_start_end(apps_to_parent_child_list(apps_by_name.itervalues())))
            if name in apps_by_name]

def load_apps(apps):
    return [loaded_app
            for loaded_app in (appomatic.utils.app.load_app(app)
                               for app in apps)
            if loaded_app]
