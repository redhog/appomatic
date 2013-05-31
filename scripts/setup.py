#! /usr/bin/python

from setuptools.command import easy_install
from setuptools import setup, find_packages
import shutil
import os.path
import sys
import hashlib

PKG_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_NAME = os.path.basename(PKG_DIR)

# Update *this* script if we can
SRC = os.path.join(PKG_DIR, '../scripts/setup.py')
if os.path.exists(SRC):
    # Check file hashes to see if they are the same.
    hashes = {}
    with open(__file__) as f:
        hashes['us'] = hashlib.md5(f.read())
    with open(SRC) as f:
        hashes['them'] = hashlib.md5(f.read())

    # We have an old version, update.
    if hashes['us'].digest() != hashes['them'].digest():
        print 'Warning: setup.py is outdated, md5 hashes differ:', hashes['us'].hexdigest(), '!=', hashes['them'].hexdigest()
        print 'Replacing setup.py with fresh version from appomatic/scripts.'
        print
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

if info['name'] != 'appomaticcore':
    info['install_requires'] = list(info.get('install_requires', [])) + ['appomaticcore==%s' % info['version']]

setup(**info)
