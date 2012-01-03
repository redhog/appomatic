# Mostly extracted from pip.commands.search

import xmlrpclib
import pip.download
import distutils.version
import os.path
import pip.req
import pip.locations
import pip.index

import pkg_resources as resources
import appomatic
def compare_versions(version1, version2):
    try:
        return cmp(distutils.version.StrictVersion(version1), distutils.version.StrictVersion(version2))
    # in case of abnormal version number, fall back to distutils.version.LooseVersion
    except ValueError:
        return cmp(distutils.version.LooseVersion(version1), distutils.version.LooseVersion(version2))


def highest_version(versions):
    return reduce((lambda v1, v2: compare_versions(v1, v2) == 1 and v1 or v2), versions)

def transform_hits(hits):
    """
    The list from pypi is really a list of versions. We want a list of
    packages with the list of versions stored inline. This converts the
    list from pypi into one we can use.
    """
    packages = {}
    for hit in hits:
        name = hit['name']
        summary = hit['summary']
        version = hit['version']
        score = hit['_pypi_ordering']

        if name not in packages.keys():
            packages[name] = {'name': name, 'summary': summary, 'versions': [version], 'score': score}
        else:
            packages[name]['versions'].append(version)

            # if this is the highest version, replace summary and score
            if version == highest_version(packages[name]['versions']):
                packages[name]['summary'] = summary
                packages[name]['score'] = score

    # each record has a unique name now, so we will convert the dict into a list sorted by score
    package_list = sorted(packages.values(), lambda x, y: cmp(y['score'], x['score']))
    return package_list

def search_pip_apps(query = '', prefix = 'appomatic_', index_url = 'http://pypi.python.org/pypi'):
    if not query: query = "appomatic"
    def mangle(package):
        package['NAME'] = package['name']
        package['DESCRIPTION'] = package['summary']
        package['SOURCE'] = "http://pypi.python.org/pypi/" + package['name']
        return package
    pypi = xmlrpclib.ServerProxy(index_url, pip.download.xmlrpclib_transport)
    return (mangle(package) for package in  transform_hits(pypi.search({'name': query, 'summary': query}, 'or'))
            if package['name'].startswith(prefix))

def install_pip_apps(*apps):
    if not apps: return

    requirement_set = pip.req.RequirementSet(
        build_dir = os.path.abspath(pip.locations.build_prefix),
        src_dir = os.path.abspath(pip.locations.src_prefix),
        download_dir = None,
        download_cache = None,
        upgrade = False,
        ignore_installed = False,
        ignore_dependencies = False)

    for name in apps:
        requirement_set.add_requirement(
            pip.req.InstallRequirement.from_line(name, None))

    assert requirement_set.has_requirements

    requirement_set.prepare_files(
        pip.index.PackageFinder(find_links=[],
                                index_urls=['http://pypi.python.org/simple/'],
                                use_mirrors=False,
                                mirrors=[]),
        force_root_egg_info=False, bundle=False)
    requirement_set.install([], [])

    return (req.name for req in
            requirement_set.successfully_installed)


def uninstall_pip_apps(*apps):
    if not apps: return
    result = []
    result += apps
    requirement_set = pip.req.RequirementSet(
        build_dir = None,
        src_dir = None,
        download_dir = None)
    for name in apps:
        dependants = get_dependant(name)
        result += dependants
        if requirement_set.requirements.keys().count(name.replace('_','-')) == 0 :
            requirement_set.add_requirement(
                pip.req.InstallRequirement.from_line(name))
        for i in  dependants:
            if requirement_set.requirements.keys().count(i.replace('_','-')) == 0 :
                requirement_set.add_requirement(
                    pip.req.InstallRequirement.from_line(i))
    
    requirement_set.uninstall(auto_confirm=True)
    
    result = list(set(result))
    return result
    
def get_dependants_list():
    installed_apps = list(appomatic.utils.app.get_pip_apps())
    apps = []
    dependencies = {}
    
    for i in installed_apps:
        apps.append(i['NAME'])
        dependencies[i['NAME']] = []
    
    
    for i in apps:
        reqs = resources.get_distribution(i).requires()
        for req in reqs:
            if (dependencies.keys().count(req.key.replace("-","_")) == 0):
                dependencies[req.key.replace("-","_")] = []
            dependencies[req.key.replace("-","_")].append(i)
    
    return dependencies

def get_requirements(app_name):
    try:
        tmp = resources.get_distribution(app_name).requires()
    except:
        return []
    res = []
    for i in tmp :
        res.append(i.key.replace("-","_"))
    
    return res


def get_apps():
    res = []
    for i in list(appomatic.utils.app.get_pip_apps()):
        res.append(i['NAME'])
    return res

def get_dependant(name):
    deps = get_dependants_list()
    try:
        tmp = deps[name]
    except:
        return []
    res = tmp
    for i in tmp :
        tmp1 = get_dependant(i)
        res += tmp1
    res = list(set(res))
    return res
