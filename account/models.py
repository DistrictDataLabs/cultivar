# account.models
# Database models for the Account application (billing, etc.)
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 21:09:14 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Database models for the Account application (billing, etc.)
"""

##########################################################################
## Imports
##########################################################################


from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


##########################################################################
## Account Information (either Member or Organization)
##########################################################################


class Account(TimeStampedModel):
    """
    An account can be either an organization or a member, and is used to link
    datasets, billing information, etc. Uses Content Types to perform the
    multiple model relationship.

    Note: Account should have a one to one relationship with either a user or
    an organization, and should be created when the organization is created.
    """

    content_type  = models.ForeignKey(ContentType, on_delete=models.CASCADE,  limit_choices_to = {"model__in": ("organization", "user")}, )
    owner_id      = models.PositiveIntegerField()
    owner         = GenericForeignKey('content_type', 'owner_id')
    billing_email = models.EmailField(null=True, help_text='Billing Email (private)')

    class Meta:
        unique_together = ('content_type', 'owner_id')
        db_table = 'trinket_account'

    def __unicode__(self):
        if self.content_type.model == 'organization':
            return self.owner.orgname
        elif self.content_type.model == 'user':
            return self.owner.username
        else:
            raise TypeError(
                'Unknown model for an account: {!r}'.format(self.content_type.model)
            )
