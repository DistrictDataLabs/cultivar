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

import urllib

from django.db import models
from trinket.utils import nullable
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from model_utils import Choices
from django.conf import settings

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
    email_hash    = models.CharField(max_length=32, editable=False, **nullable)
    billing_email = models.EmailField(null=False, help_text='Billing Email (private)')
    description   = models.CharField(max_length=255, **nullable)
    url           = models.URLField(**nullable)
    team          = models.ManyToManyField('auth.User', through='organization.Role', related_name='organizations')

    @property
    def gravatar(self):
        return self.get_gravatar_url()

    @property
    def gravatar_icon(self):
        return self.get_gravatar_url(size=settings.GRAVATAR_ICON_SIZE)

    def get_gravatar_url(self, size=None, default=None):
        """
        Comptues the gravatar url from an email address
        """
        size    = size or settings.GRAVATAR_DEFAULT_SIZE
        default = default or settings.GRAVATAR_DEFAULT_IMAGE
        params  = urllib.urlencode({'d': default, 's': str(size)})

        return "http://www.gravatar.com/avatar/{}?{}".format(
            self.email_hash, params
        )

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
