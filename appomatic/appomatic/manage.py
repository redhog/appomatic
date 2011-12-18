#!/usr/bin/env python
from django.core.management import execute_manager
import os.path

os.chdir(os.path.dirname(__file__))
import settings

def main():
    execute_manager(settings)

if __name__ == "__main__":
    main()

