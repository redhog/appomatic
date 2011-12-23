import django.shortcuts
import django.template
import settings
import appomatic_appadmin.utils.app
import appomatic_appadmin.utils.reload
import django.contrib.messages
import django.http
import os.path
import tempfile
import threading
import json
import time

def apps_by_source(apps):
    res = {}
    for app in apps:
        if app['SOURCE'] not in res:
            res[app['SOURCE']] = []
        res[app['SOURCE']].append(app)
    return res

def index(request):
    action = request.REQUEST.get('action', '')

    if action == 'uninstall_selected':
        for name in appomatic_appadmin.utils.app.uninstall_pip_apps(
            *request.REQUEST.getlist('_selected_action')):
            django.contrib.messages.add_message(request, django.contrib.messages.INFO, 'Successfully uninstalled %s' % (name,))
        appomatic_appadmin.utils.reload.reload(2)

    return django.shortcuts.render_to_response(
        'appomatic_appadmin/index.html',
        {"installed_apps": apps_by_source(settings.APPOMATIC_APPS),


         },
        context_instance=django.template.RequestContext(request))

def add(request):
    action = request.REQUEST.get('action', '')
    query = request.REQUEST.get('q', '')

    if action == 'install_selected':
        for name in appomatic_appadmin.utils.app.install_pip_apps(
            *request.REQUEST.getlist('_selected_action')):
            django.contrib.messages.add_message(request, django.contrib.messages.INFO, 'Successfully installed %s' % (name,))
        appomatic_appadmin.utils.reload.reload(2)

    installed_app_names = [app['NAME'] for app in settings.APPOMATIC_APPS]
    found_apps = [app for app in appomatic_appadmin.utils.app.search_pip_apps(query)
                  if app['name'] not in installed_app_names]

    return django.shortcuts.render_to_response(
        'appomatic_appadmin/add.html',
        {"q": query, "found_apps": found_apps},
        context_instance=django.template.RequestContext(request))


def action(request):
    action = request.REQUEST.get('action', '')
    lst = request.REQUEST.getlist('_selected_action')
    if action == 'uninstall_selected':
        def fn(out):
            total = len(lst) + 1
            for idx, name in enumerate(lst):
                out.write(json.dumps({"percent_done": int(100.0 * idx / total), "status": "Uninstalling " + name}) + "\n")
                out.flush()
                appomatic_appadmin.utils.app.uninstall_pip_apps(name)

    elif action == 'install_selected':
        def fn(out):
            total = len(lst) + 1
            for idx, name in enumerate(lst):
                out.write(json.dumps({"percent_done": int(100.0 * idx / total), "status": "Installing " + name}) + "\n")
                out.flush()
                appomatic_appadmin.utils.app.install_pip_apps(name)

    return django.http.HttpResponse(json.dumps({"pid": progressable(fn, reload=True)}), content_type="text/json")

PROGRESS_PREFIX="appomatic_appadmin_progress_"

def progress(request, pid):
    # Make sure no one tricks us by adding .. and stuff in the name
    assert '/' not in pid and '.' not in pid
    path = os.path.join(tempfile.gettempdir(), PROGRESS_PREFIX + pid)
    if not os.path.exists(path):
        output = [json.dumps({"percent_done": 100, "status": "Done"})]
    else:
        with open(path) as f:
            output = [line[:-1] for line in f]
    return django.http.HttpResponse("[" + ',\n'.join(output) + "]", content_type="text/json")

def progressable(fn, reload = False, *arg, **kw):
    fd, path = tempfile.mkstemp(prefix=PROGRESS_PREFIX)
    f = os.fdopen(fd, "w")
    f.write(json.dumps({"percent_done": 0, "status": ""}) + "\n")
    f.flush()
    def wrapper():
        fn(f, *arg, **kw)
        if reload:
            f.write(json.dumps({"percent_done": 99, "status": "Restarting server"}) + "\n")
            f.flush()
            # Let the client fetch the status before we unlink the file
            time.sleep(2)
        os.unlink(path)
        if reload:
            appomatic_appadmin.utils.reload.reload()
    threading.Thread(target=wrapper).start()
    return os.path.split(path)[1][len(PROGRESS_PREFIX):]
