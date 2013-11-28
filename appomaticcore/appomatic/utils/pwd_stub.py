class PwEntry(object):
    def __init__(self, **kw):
        for key, value in kw.iteritems():
            setattr(self, key, value)

    def __getitem__(self, name):
        return getattr(self, name)

dummy = PwEntry(pw_name="dummy",
                pw_passwd="!",
                pw_uid=0,
                pw_gid=0,
                pw_gecos="",
                pw_dir='/',
                pw_shell="")

def getpwuid(uid):
    return dummy

def getpwnam(name):
    return dummy

def getpwall():
    return []
