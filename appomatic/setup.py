#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic",
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

    install_requires = ['appomaticcore', 'appomatic_appadmin'],

    packages = [],
    scripts = [],
    package_data = {'': ['*.txt']},
)
