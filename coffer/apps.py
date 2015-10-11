# coffer.apps
# Describes the Coffer application to Django
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Oct 11 17:07:54 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: apps.py [] benjamin@bengfort.com $

"""
Describes the Coffer application to Django
"""

##########################################################################
## Imports
##########################################################################

from django.apps import AppConfig

##########################################################################
## Coffer Config
##########################################################################

class CofferConfig(AppConfig):
    name = 'coffer'
    verbose_name = "Dataset Coffer"

    def ready(self):
        import coffer.signals
