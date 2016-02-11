# members.models
# Models that store information about faculty and students.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:24:48 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models that store information about faculty and students.
"""

##########################################################################
## Imports
##########################################################################

import urllib

from django.db import models
from django.conf import settings
from trinket.utils import nullable
from model_utils.models import TimeStampedModel
from markupfield.fields import MarkupField
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

##########################################################################
## User Profile Model for DDL Members
##########################################################################

class Profile(TimeStampedModel):
    """
    Stores extra information about a user or DDL member.
    """

    user         = models.OneToOneField('auth.User', editable=False)
    email_hash   = models.CharField(max_length=32, editable=False)
    organization = models.CharField(max_length=255, **nullable)
    location     = models.CharField(max_length=255, **nullable)
    biography    = MarkupField(markup_type='markdown', help_text='Edit in Markdown', **nullable)
    twitter      = models.CharField(max_length=100, **nullable)
    linkedin     = models.URLField(**nullable)

    class Meta:
        db_table = 'member_profiles'

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def full_email(self):
        email = u"{} <{}>".format(self.full_name, self.user.email)
        return email.strip()

    @property
    def gravatar(self):
        return self.get_gravatar_url()

    @property
    def gravatar_icon(self):
        return self.get_gravatar_url(size=settings.GRAVATAR_ICON_SIZE)

    @property
    def gravatar_badge(self):
        return self.get_gravatar_url(size=64)

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

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:user-detail', args=(self.user.pk,))

    def get_absolute_url(self):
        """
        Returns the detail view url for the object
        """
        return reverse('member-detail', args=(self.user.username,))

    def __unicode__(self):
        return self.full_email


##########################################################################
## Account Information (either Member or Organization)
##########################################################################

class Account(TimeStampedModel):
    """
    An account can be either an organization or a member, and is used to link
    datasets, billing information, etc. Uses Content Types to perform the
    multiple model relationship.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,  limit_choices_to = {"model__in": ("organization", "user")}, )
    owner_id     = models.PositiveIntegerField()
    owner        = GenericForeignKey('content_type', 'owner_id')

    def __unicode__(self):
        if self.content_type.model == 'organization':
            return self.owner.orgname
        elif self.content_type.model == 'user':
            return self.owner.username
        else:
            raise TypeError(
                'Unknown model for an account: {!r}'.format(self.content_type.model)
            )
