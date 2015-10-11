# coffer.models
# Models for dataset management and collection.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 21:45:27 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for dataset management and collection.
"""

##########################################################################
## Imports
##########################################################################

from django.db import models
from model_utils import Choices
from model_utils.models import TimeStampedModel
from trinket.utils import nullable, notnullable

##########################################################################
## Models
##########################################################################

class Dataset(TimeStampedModel):
    """
    A record of a dataset uploaded to the data lake for visual analysis.
    """

    DATATYPE   = Choices('csv', 'json', 'xml')

    uploader   = models.ForeignKey('auth.User', related_name='datasets')
    dataset    = models.FileField(upload_to='datasets')
    dimensions = models.PositiveIntegerField(default=0)
    length     = models.PositiveIntegerField(default=0)
    filesize   = models.PositiveIntegerField(default=0)
    signature  = models.CharField(max_length=44, unique=True, null=False, blank=True)
    datatype   = models.CharField(max_length=4, choices=DATATYPE, default=DATATYPE.csv)
    delimiter  = models.CharField(max_length=1, default=",")

    class Meta:
        db_table = "datasets"
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return "{} dataset with {} rows and {} dimensions, uploaded by {}".format(
            self.datatype, self.length, self.dimensions, self.uploader
        )
