#!/usr/bin/env python
from django.core.management import execute_manager
import os.path
import sys

if sys.argv[1] not in ('makemessages', 'compilemessages'):
    os.chdir(os.path.dirname(__file__))

import settings

def main():
    execute_manager(settings)

if __name__ == "__main__":
    main()

