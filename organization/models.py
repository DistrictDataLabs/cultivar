# organization.models
# Models for the organization app; some crossover with the members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Jan 29 21:42:44 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the organization app; some crossover with the members app.
"""

##########################################################################
## Imports
##########################################################################

from __future__ import unicode_literals

from django.db import models
from trinket.utils import nullable
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from model_utils import Choices

##########################################################################
## Models
##########################################################################

class Organization(TimeStampedModel):
    """
    Describes a team or an organization of members.
    """

    name          = models.CharField(max_length=255, **nullable)
    orgname       = models.CharField(max_length=255, unique=True, null=False)
    location      = models.CharField(max_length=255, **nullable)
    email         = models.EmailField(help_text='Contact Email (public)', **nullable)
    gravatar_email = models.EmailField(help_text='Gravatar Email (private)', **nullable)
    billing_email = models.EmailField(null=False, help_text='Billing Email (private)')
    description   = models.CharField(max_length=255, **nullable)
    url           = models.URLField(**nullable)
    team          = models.ManyToManyField('auth.User', through='organization.Role', related_name='organizations')

    def __unicode__(self):
        return self.name or self.orgname


class Role(TimeStampedModel):
    """
    Describes the role of a member on an organization or team.
    """

    ROLES         = Choices('owner', 'admin', 'writer', 'reader')
    VISIBILITY    = Choices('public', 'protected', 'private')

    user          = models.ForeignKey('auth.User', related_name='team_roles')
    organization  = models.ForeignKey('organization.Organization', related_name='roles')
    role          = models.CharField(max_length=10, choices=ROLES, default=ROLES.reader)
    visibility    = models.CharField(max_length=10, choices=VISIBILITY, default=VISIBILITY.protected)

    def __unicode__(self):
        return "{} is {} of {} ({})".format(
            self.user.username, self.role, self.organization, self.visibility
        )
