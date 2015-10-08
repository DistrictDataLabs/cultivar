#!/usr/bin/env python
# manage.py
# Django default management commands, with some special sauce.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 14:22:54 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: manage.py [] benjamin@bengfort.com $

"""
Django default management commands, with some special sauce.
"""

##########################################################################
## Imports
##########################################################################

import os
import sys
import dotenv

##########################################################################
## Main Method
##########################################################################

if __name__ == "__main__":
    ## Manage Django Environment
    if os.path.exists('.env'):
        dotenv.read_dotenv()

    ## Set the default settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trinket.settings.production")

    ## Execute Django utility
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
