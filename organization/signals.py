# organization.signals
# Signals management for the Organization app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 10 21:52:52 2016 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals management for the Organization app.
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from django.dispatch import receiver
from django.db.models.signals import pre_save

from organization.models import Organization
from django.contrib.auth.models import User

##########################################################################
## User Signals
##########################################################################

@receiver(pre_save, sender=Organization)
def update_organization_gravatar(sender, instance, **kwargs):
    """
    Upates the organization's email hash from the gravatar email field.
    """
    if instance.gravatar_email.strip():
        ## Compute the email hash
        digest = hashlib.md5(instance.gravatar_email.lower()).hexdigest()
        instance.email_hash = digest
    else:
        instance.gravatar_email = None
        instance.email_hash = None
