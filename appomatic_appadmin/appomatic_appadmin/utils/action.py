import os
import re 
import json
import sys
import django.core.management

class OutLineFilter(object):
    class __metaclass__(type):
        def __new__(cls, name, bases, dct):
            filters = {}
            for base in bases:
                filters.update(getattr(base, 'filters', {}))
            for key, value in dct.iteritems():
                if hasattr(value, "filter_pattern"):
                    filters[key] = re.compile(value.filter_pattern)
            dct["filters"] = filters
            return type.__new__(cls, name, bases, dct)

    def __init__(self, file):
        self.file = file
        self.last_line = ''
    
    @classmethod
    def filter(cls, pattern):
        def filter(fn):
            fn.filter_pattern = pattern
            return fn
        return filter

    def close(self):
        self.file.close()

    def flush(self):
        self.file.flush()

    def write(self, str):
        self.last_line += str
        if '\n' in self.last_line:
            lines = self.last_line.split('\n')
            self.last_line = lines[-1]
            for line in lines[:-1]:
                self.write_line(line + '\n')

    def writelines(self, sequence):
        self.write(sequence[0])
        for line in sequence[1:]:
            self.write_line(line)

    def write_line(self, line):
        self.file.write(self.filter_line(line))
        self.file.flush()

    def filter_line(self, line):
        for key, value in self.filters.iteritems():
            if value.match(line[:-1]):
                line = getattr(self, key)(line)
        return line

class OutProgressFilterBase(OutLineFilter):
    def __init__(self, file, k = 1, m = 0):
        OutLineFilter.__init__(self, file)
        self.k = k
        self.m = m
        self.done = 0

    @OutLineFilter.filter(".*")
    def out(self, line):
        return json.dumps({"done": self.k * self.done + self.m, "status":line[:-1]}) + '\n'

    @classmethod
    def progress(cls, filter, progress):
        @OutLineFilter.filter(filter)
        def fn(self, line):
            self.done += progress
            return line
        return fn

    @classmethod
    def progress_to(cls, filter, progress_to):
        @OutLineFilter.filter(filter)
        def fn(self, line):
            self.done = progress_to
            return line
        return fn

class OutProgressFilter(OutProgressFilterBase):
    exc_filter = OutProgressFilterBase.progress_to(r'Exception:.*', 1)

class Action(object):
    def __init__(self, file, k = 1, m = 0, *arg, **kw):
        self.out = self.Filter(file, k, m)
        self.do_fork_and_run(*arg, **kw)

    def do_fork_and_run(self, *arg, **kw):
        pid = os.fork()
        if pid == 0:
            sys.stderr = sys.stdout = self.out
            try:
                self.action(*arg, **kw)
            except:
                import traceback
                traceback.print_exc()
            sys.exit(0)
        else:
            pid, status = os.waitpid(pid, 0)
            return status

    Filter = OutLineFilter

    def action(self):
        pass

class SyncDb(Action):
    class Filter(OutProgressFilter):
        x1 = OutProgressFilter.progress_to(r'Creating tables ...', 0)
        x2 = OutProgressFilter.progress(r'Processing .* model', 0.01)
        x3 = OutProgressFilter.progress_to(r"Installing custom SQL \.\.\.", 0.3)
        x4 = OutProgressFilter.progress(r"Installing custom SQL for .* model", 0.01)
        x5 = OutProgressFilter.progress_to(r"Installing indexes \.\.\.", 0.6)
        x6 = OutProgressFilter.progress(r"Installing index for .* model", 0.01)
        x7 = OutProgressFilter.progress_to(r'Running migrations \.\.\.', 1.0)
        x8 = OutProgressFilter.progress(r'Running migrations for .*', 0.01)
 
    def action(self):
        has_south = 'migrate' in django.core.management.get_commands()
        if has_south:
            self.out.k *= 0.5
        django.core.management.call_command('syncdb', interactive=False)
        if has_south:
            print "Running migrations ..."
            django.core.management.call_command('migrate')
