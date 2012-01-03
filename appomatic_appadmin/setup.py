#! /usr/bin/python

from setuptools.command import easy_install
from setuptools import setup, find_packages
import shutil
import os.path
import sys

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_NAME = os.path.basename(PKG_DIR)

# Update *this* script if we can
SRC = os.path.join(PKG_DIR, '../scripts/setup.py')
if os.path.exists(SRC) and os.stat(SRC).st_mtime != os.stat(__file__).st_mtime:
    print os.stat(SRC).st_mtime, " != ", os.stat(__file__).st_mtime
    os.remove(__file__)
    shutil.copy2(SRC, __file__)
    with open(__file__) as f:
        exec f
    sys.exit(0)

# Make it possible to overide script wrapping
old_is_python_script = easy_install.is_python_script
def is_python_script(script_text, filename):
    if 'SETUPTOOLS_DO_NOT_WRAP' in script_text:
        return False
    return old_is_python_script(script_text, filename)
easy_install.is_python_script = is_python_script

if os.path.exists(os.path.join(PKG_DIR, '../INFO')):
    with open(os.path.join(PKG_DIR, '../INFO')) as f:
        data = f.read()
    with open(os.path.join(PKG_DIR, 'INFO')) as f:
        data += f.read()
    with open(os.path.join(PKG_DIR, '__info__.py'), "w") as f:
        f.write(data)

if os.path.exists(os.path.join(PKG_DIR, '../scripts/manifest.in.template')):
    shutil.copyfile(os.path.join(PKG_DIR, '../scripts/manifest.in.template'),
                    os.path.join(PKG_DIR, 'MANIFEST.in'))

def load_info(path):
    info = {}
    with open(path) as f:
        exec f in info
    for name in globals().keys():
        if name in info:
            del info[name]
    return info

info = {
    "packages": find_packages(),
    "scripts": [],
    "package_data": {'': ['*.txt', '*.css', '*.html', '*.js']},
    "include_package_data": True,
}
info.update(load_info(os.path.join(PKG_DIR, '__info__.py')))
setup(**info)
