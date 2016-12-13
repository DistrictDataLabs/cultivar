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
from dataset.models import DatasetVersion
from dataset.models import DataFile
from dataset.models import License


##########################################################################
## Inline Adminstration
##########################################################################

class DataFilesInline(admin.StackedInline):
    """
    Inline administration descriptor for account object
    """

    model = DataFile
    extra = 1
    verbose_name_plural = 'files'


class DatasetVersionsInline(admin.StackedInline):
    """
    Inline administration descriptor
    """

    model = DatasetVersion
    extra = 1
    verbose_name_plural = 'versions'


class DatasetAdmin(admin.ModelAdmin):
    """
    Defines the administration for a dataset in the CMS.
    """

    # inlines = (DataFilesInline,)
    versions = (DatasetVersionsInline,)

##########################################################################
## Register Admin
##########################################################################

admin.site.register(Dataset, DatasetAdmin)
admin.site.register(License)
