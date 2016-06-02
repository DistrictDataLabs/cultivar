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
from django.db.models.signals import pre_save, post_save

from account.models import Account
from organization.models import Organization
from django.contrib.auth.models import User


##########################################################################
## Organization Pre-Save Signals
##########################################################################

@receiver(pre_save, sender=Organization)
def update_organization_gravatar(sender, instance, **kwargs):
    """
    Upates the organization's email hash from the gravatar email field.
    """
    ## Compute the email hash
    instance.gravatar_email = instance.gravatar_email.strip().lower()
    digest = hashlib.md5(instance.gravatar_email.encode(encoding='utf-8')).hexdigest()
    instance.email_hash = digest


##########################################################################
## Organization Post-Save  Signals
##########################################################################

@receiver(post_save, sender=Organization)
def create_organization_account(sender, instance, created, **kwargs):
    """
    Creates and associates an Account with an Organization on create.
    """
    if created:
        Account.objects.create(owner=instance)
    else:
        instance.account.save()
