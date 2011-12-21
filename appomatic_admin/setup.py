#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_admin",
    version = "0.0.5",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Enables the django site admin",
    license = "GPL",
    keywords = "appomatic admin",
    url = "http://www.djangoproject.com",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = [],

    packages = find_packages(),
    scripts = [],
    #package_data = {'': ['*.html']},
)
