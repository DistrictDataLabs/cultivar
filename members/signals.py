# members.signals
# Signals management for the Members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 10:43:03 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals management for the Members app.
"""

##########################################################################
## Imports
##########################################################################

import hashlib

from django.dispatch import receiver
from django.db.models.signals import post_save

from account.models import Account
from members.models import Profile
from django.contrib.auth.models import User

##########################################################################
## User Post-Save Signals
##########################################################################

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object for the user if it doesn't exist, or updates
    it with new information from the User (e.g. the gravatar).
    """
    ## Compute the email hash
    email = instance.email.lower()
    digest = hashlib.md5(email.encode('utf-8')).hexdigest()

    if created:
        Profile.objects.create(user=instance, email_hash=digest)
    else:
        instance.profile.email_hash = digest
        instance.profile.save()


@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    """
    Creates and associates an Account with an User on create.
    """
    if created:
        Account.objects.create(owner=instance)
    else:
        instance.profile.account.save()
