# dataset.signals
# Signals for handling dataset models and other app details.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 20:45:43 2016 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals for handling dataset models and other app details.
"""

##########################################################################
## Imports
##########################################################################

from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver
