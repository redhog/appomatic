#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_django_cms",
    version = "0.0.1",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Get the pony powered CMS With Frontend-Editing",
    license = "GPL",
    keywords = "appomatic django-cms",
    url = "https://www.django-cms.org",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['django==1.3.1', 'django-cms'],

    packages = find_packages(),
    scripts = [],
    package_data = {'': ['*.html']},
)
