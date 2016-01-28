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

from members.models import Profile
from django.contrib.auth.models import User

##########################################################################
## User Signals
##########################################################################

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile object for the user if it doesn't exist, or updates
    it with new information from the User (e.g. the gravatar).
    """
    ## Compute the email hash
    digest = hashlib.md5(instance.email.lower()).hexdigest()

    if created:
        Profile.objects.create(user=instance, email_hash=digest)
    else:
        instance.profile.email_hash = digest
        instance.profile.save()
