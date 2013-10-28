import django.shortcuts
import django.template
import appomatic_appadmin.utils.app
import appomatic_appadmin.utils.reload
import django.contrib.messages
import django.http
import os.path
import tempfile
import threading
import json
import time
import appomatic_appadmin.utils.action
import urllib
from django.conf import settings

def apps_by_source(apps):
    res = {}
    for app in apps:
        if app['SOURCE'] not in res:
            res[app['SOURCE']] = []
        res[app['SOURCE']].append(app)
    return res

def index(request):
    
    return django.shortcuts.render_to_response(
        'appomatic_appadmin/index.html',
        {"installed_apps": apps_by_source(settings.APPOMATIC_APPS),


         },
        context_instance=django.template.RequestContext(request))

def add(request):
    query = request.REQUEST.get('q', '')

    installed_app_names = [app['NAME'] for app in settings.APPOMATIC_APPS]
    found_apps = [app for app in appomatic_appadmin.utils.app.search_pip_apps(query)
                  if app['name'] not in installed_app_names]

    return django.shortcuts.render_to_response(
        'appomatic_appadmin/add.html',
        {"q": query, "found_apps": found_apps},
        context_instance=django.template.RequestContext(request))
        
def details(request, app_name):
    deps = appomatic_appadmin.utils.app.get_dependant(app_name)
    appomatic_deps = []
    appomatic_reqs = []
    temp =[]
    for i in deps:
        if i.startswith('appomatic'):
            appomatic_deps += [i]
        else:
            temp += [i]
    deps = temp

    temp = []
    reqs = appomatic_appadmin.utils.app.get_requirements(app_name)
    for i in reqs:
        if i.startswith('appomatic'):
            appomatic_reqs += [i]
        else:
            temp += [i]
    reqs = temp
    
    return django.shortcuts.render_to_response('appomatic_appadmin/details.html',
                    {'app_name' : app_name, 'reqs': reqs, 'deps': deps , 'appomatic_deps': appomatic_deps, 'appomatic_reqs': appomatic_reqs},
                    context_instance = django.template.RequestContext(request)
                    )


def action(request):
    class Actions(object):
        def __init__(self, lst):
            self.lst = lst

        def _urlencode(self, **q):
            data = []
            for name, value in q.items():
                if isinstance(value, (tuple, list)):
                    for part in value:
                        data.append((name, part))
                else:
                    data.append((name, value))
            return urllib.urlencode(data)

        def uninstall_selected(self, out):
            temp = []
            for i in self.lst:
                temp += appomatic_appadmin.utils.app.get_dependant(i)
            
            self.lst += temp 
            self.lst = list(set(self.lst))   
            total = len(self.lst) + 1
            for idx, name in enumerate(self.lst):
                out.write(json.dumps({"done": idx / total, "status": "Uninstalling " + name}) + "\n")
                out.flush()
                appomatic_appadmin.utils.app.uninstall_pip_apps(name)
            out.write(json.dumps({"done": 1, "status": "Restarting server", "delay": 3000}) + "\n")
            out.flush()
            appomatic_appadmin.utils.reload.reload()

        def install_selected(self, out):
            total = len(self.lst) + 1
            for idx, name in enumerate(self.lst):
                out.write(json.dumps({"done": 0.5 * idx / total, "status": "Installing " + name}) + "\n")
                out.flush()
                appomatic_appadmin.utils.app.install_pip_apps(name)
            out.write(json.dumps({"done": 0.5, "status": "Restarting server", "delay": 3000, "next": django.core.urlresolvers.reverse("appomatic_appadmin.views.action") + "?" + self._urlencode(action="install_selected_syncdb", lst=self.lst)}) + "\n")
            out.flush()
            appomatic_appadmin.utils.reload.reload()

        def install_selected_syncdb(self, out):
            out.write(json.dumps({"done": 0.5, "status": "Syning database"}) + "\n")
            out.flush()
            appomatic_appadmin.utils.action.SyncDb(out, k=0.5, m=0.5)
            out.write(json.dumps({"done": 1, "status": "Done"}) + "\n")
            out.flush()

        def reload(self, out):
            out.write(json.dumps({"done": 1, "status": "Restarting server", 'delay': 3000}) + "\n")
            out.flush()
            appomatic_appadmin.utils.reload.reload()

    return django.http.HttpResponse(json.dumps({"pid": progressable(getattr(Actions(request.REQUEST.getlist('_selected_action')),
                                                                            request.REQUEST.get('action', '')))}), content_type="text/json")

PROGRESS_PREFIX="appomatic_appadmin_progress_"

def progress(request, pid):
    # Make sure no one tricks us by adding .. and stuff in the name
    assert '/' not in pid and '.' not in pid
    path = os.path.join(tempfile.gettempdir(), PROGRESS_PREFIX + pid)
    if not os.path.exists(path):
        output = [json.dumps({"done": 1, "status": "Done"})]
    else:
        with open(path) as f:
            output = [line[:-1] for line in f]
    return django.http.HttpResponse("[" + ',\n'.join(output) + "]", content_type="text/json")

def progressable(fn, *arg, **kw):
    fd, path = tempfile.mkstemp(prefix=PROGRESS_PREFIX)
    f = os.fdopen(fd, "w")
    f.write(json.dumps({"done": 0, "status": ""}) + "\n")
    f.flush()
    def wrapper():
        try:
            fn(f, *arg, **kw)
        except Exception, e:
            f.write(json.dumps({"done": 1, "status": str(e), "delay": 10000}) + "\n")

    threading.Thread(target=wrapper).start()
    return os.path.split(path)[1][len(PROGRESS_PREFIX):]

def progress_display(request, pid):
    return django.shortcuts.render_to_response('appomatic_appadmin/progress_display.html',
                    {"pid": pid, "next": request.GET.get("next", request.META.get('HTTP_REFERER', None)), "description": request.GET.get("description", "")},
                    context_instance = django.template.RequestContext(request)
                    )
