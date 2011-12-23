#! /usr/bin/python

from setuptools import setup, find_packages
setup(
    name = "appomatic_appadmin",
    version = "0.0.5",

    author = "RedHog (Egil Moeller)",
    author_email = "egil.moller@freecode.no",
    description = "Django admin page to administer appomatic apps",
    license = "GPL",
    keywords = "appomatic django-admin",
    url = "http://github.com/redhog/appomatic_appadmin",
    # long_description =
    # download_url =
    # classifiers =

    install_requires = ['appomatic', 'appomatic_admin'],

    packages = find_packages(),
    scripts = [],
    package_data = {'': ['*.html', '*.js', '*.css']},
    include_package_data=True,
)
