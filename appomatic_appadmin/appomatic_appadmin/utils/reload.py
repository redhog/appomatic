import sys
import os
import time
import threading
import django.utils.autoreload

force_reload = False

old_code_changed = django.utils.autoreload.code_changed
def code_changed():
    return force_reload or old_code_changed()
django.utils.autoreload.code_changed = code_changed

def reload(timeout = None):
    #print "============================{REALOAD}============================"
    #import traceback
    #traceback.print_stack()

    if "RUN_MAIN" in os.environ:
        # We're running under the normal dev server with the auto-reloader enabled
        def reload():
            global force_reload
            force_reload = True
    # Handle other cases, like fcgi here
    else:
        raise Exception("Unable to reload the web server. Please restart it manually.")

    if timeout is None:
        reload()
    else:
        class Thread(threading.Thread):
            def run(self, *arg, **kw):
                if timeout:
                    time.sleep(timeout)
                reload()
        Thread().start()
