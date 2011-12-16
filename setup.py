#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_cms_tagging",
    version = "0.0.1",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Adds tagging support to django-cms",
    license = "GPL",
    keywords = "appomatic django-tagging django-cms",
    url = "http://github.com/redhog/appomatic_cms_tagging",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['django==1.3.1'],

    packages = find_packages(),
    scripts = [],
    package_data = {'': ['*.html']},
)
