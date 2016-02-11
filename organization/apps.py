# organization.apps
# Describes the Organization application for Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Jan 29 21:41:25 2016 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Describes the Organization application for Django
"""

##########################################################################
## Imports
##########################################################################

from __future__ import unicode_literals

from django.apps import AppConfig

##########################################################################
## Organization Config
##########################################################################

class OrganizationConfig(AppConfig):
    name = 'organization'
