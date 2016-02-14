# account.signals
# Signals to ensure that the account model is managed correctly on save.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Feb 13 15:25:36 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals to ensure that the account model is managed correctly on save.
"""

##########################################################################
## Imports
##########################################################################

from django.dispatch import receiver
from django.db.models.signals import pre_save

from account.models import Account

##########################################################################
## Account Pre-Save Signals
##########################################################################

@receiver(pre_save, sender=Account)
def set_account_name(sender, instance, **kwargs):
    """
    Sets the slug name for the account from the owner.
    e.g. sets the account name as the username or orgname.
    """

    model_name_map = {
        'organization': 'orgname',
        'user': 'username',
    }

    model_name = instance.content_type.model
    if model_name in model_name_map:
        attr = model_name_map[model_name]
        instance.name = getattr(instance.owner, attr)
    else:
        raise TypeError(
            'Unknown owner model for an account: {!r}'.format(model_name)
        )
