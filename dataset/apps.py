# dataset.apps
# Describes the Dataset application to Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 20:44:11 2016 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Describes the Dataset application to Django
"""

##########################################################################
## Imports
##########################################################################

from __future__ import unicode_literals

from django.apps import AppConfig

##########################################################################
## Dataset Config
##########################################################################

class DatasetConfig(AppConfig):

    name = 'dataset'
    verbose_name = 'Dataset Storage'

    def ready(self):
        import dataset.signals
