#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_cmsplugin_phlog",
    version = "0.0.2",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Integrates django-cms and Photologue",
    license = "GPL",
    keywords = "appomatic django-cms photologue",
    url = "https://github.com/benliles/cmsplugin-phlog",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['appomatic-django-cms', 'appomatic_photolog', 'cmsplugin-phlog'],

    packages = find_packages(),
    scripts = [],
    #package_data = {'': ['*.html']},
)
