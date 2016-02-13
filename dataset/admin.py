# dataset.admin
# Administrative utilities for Dataset models.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 21:44:48 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Administrative utilities for Dataset models.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from dataset.models import Dataset
from dataset.models import License

##########################################################################
## Register Admin
##########################################################################

admin.site.register(Dataset)
admin.site.register(License)
