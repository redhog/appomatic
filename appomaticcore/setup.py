#! /usr/bin/python

import setuptools
import setuptools.command.easy_install

old_is_python_script = setuptools.command.easy_install.is_python_script

def is_python_script(script_text, filename):
    if 'SETUPTOOLS_DO_NOT_WRAP' in script_text:
        return False
    return old_is_python_script(script_text, filename)

setuptools.command.easy_install.is_python_script = is_python_script

setuptools.setup(
    name = "appomaticcore",
    version = "0.0.5",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Appomatic is a userfriendly Django environment with automatic plugin (app) management based on pip.",
    license = "GPL",
    keywords = "appomatic django apps pip",
    url = "http://github.com/redhog/appomatic",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['django==1.3.1', 'pip==0.8.1'],

    packages = setuptools.find_packages(),
    scripts = ['wsgi'],
    package_data = {'': ['*.txt']},
    entry_points = {'console_scripts': [
            'appomatic = appomatic.manage:main',
            ]},
)
