#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_photolog",
    version = "0.0.1",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Photologue is a reusable Django application that provides powerful image management and manipulation functionality as well as a complete photo gallery solution.",
    license = "GPL",
    keywords = "appomatic photologue",
    url = "http://code.google.com/p/django-photologue/",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['django-photologue'],

    packages = find_packages(),
    scripts = [],
    #package_data = {'': ['*.html']},
)
