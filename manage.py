#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    configuration = os.getenv("DJANGO_CONFIGURATION", "Development")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", configuration)

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
