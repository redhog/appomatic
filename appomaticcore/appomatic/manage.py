#!/usr/bin/env python

import django
import os.path
import sys

if sys.argv[1] not in ('makemessages', 'compilemessages'):
    os.chdir(os.path.dirname(__file__))

import settings

def main():

    if django.VERSION[0] >= 1 and django.VERSION[1] >= 5:

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appomatic.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.management import execute_manager
        execute_manager(settings)

if __name__ == "__main__":
    main()
