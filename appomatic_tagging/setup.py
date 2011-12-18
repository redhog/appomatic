#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_tagging",
    version = "0.0.2",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "A generic tagging application for Django projects",
    license = "GPL",
    keywords = "appomatic django-tagging",
    url = "http://code.google.com/p/django-tagging/",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['django-tagging'],

    packages = find_packages(),
    scripts = [],
    #package_data = {'': ['*.html']},
)
