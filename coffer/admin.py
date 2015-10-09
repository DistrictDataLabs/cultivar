# coffer.admin
# Administrative utilities for Coffer models.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 21:44:48 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Administrative utilities for Coffer models.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from coffer.models import Dataset

##########################################################################
## Register Admin
##########################################################################

admin.site.register(Dataset)
