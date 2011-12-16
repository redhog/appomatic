#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic",
    version = "0.0.1",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Appomatic is a userfriendly Django environment with automatic plugin (app) management based on pip.",
    license = "GPL",
    keywords = "appomatic django apps pip",
    url = "http://github.com/redhog/appomatic",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['django==1.3.1'],

    packages = find_packages(),
    scripts = [],
    package_data = {'': ['*.txt']},
)
