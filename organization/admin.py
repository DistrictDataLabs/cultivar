# organization.admin
# CMS (Admin) stuff for organizations in Trinket.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 10 21:34:22 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
CMS (Admin) stuff for organizations in Trinket.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from organization.models import Organization, Role


##########################################################################
## Register Admin
##########################################################################

admin.site.register(Organization)
admin.site.register(Role)
