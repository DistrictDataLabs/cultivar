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

import os
import unicodecsv as csv

from django.db import models
from model_utils import Choices
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from trinket.utils import nullable, notnullable
from django.core.urlresolvers import reverse

##########################################################################
## Models
##########################################################################

class Dataset(TimeStampedModel):
    """
    A record of a dataset uploaded to the data lake for visual analysis.
    """

    DATATYPE    = Choices('csv', 'json', 'xml')

    uploader    = models.ForeignKey('auth.User', related_name='datasets')
    dataset     = models.FileField(upload_to='datasets')
    title       = models.CharField(max_length=128, **nullable)
    description = MarkupField(markup_type='markdown', **nullable)
    dimensions  = models.PositiveIntegerField(default=0)
    length      = models.PositiveIntegerField(default=0)
    filesize    = models.PositiveIntegerField(default=0)
    signature   = models.CharField(max_length=44, unique=True, null=False, blank=True)
    datatype    = models.CharField(max_length=4, choices=DATATYPE, default=DATATYPE.csv)
    delimiter   = models.CharField(max_length=1, default=",")

    class Meta:
        db_table = "datasets"
        ordering = ('-created',)
        get_latest_by = 'created'

    @property
    def filename(self):
        """
        Returns the basename of the dataset
        """
        return os.path.basename(self.dataset.name)

    def headers(self):
        """
        Returns the headers of the file
        """
        self.dataset.open('r')
        reader = csv.reader(self.dataset, delimiter=self.delimiter.encode('utf-8'))
        header = reader.next()
        self.dataset.close()
        return header

    def preview(self, rows=20):
        """
        Returns the first n rows of the file.
        """
        self.dataset.open('r')
        reader = csv.reader(self.dataset, delimiter=self.delimiter.encode('utf-8'))
        header = reader.next()
        for idx, row in enumerate(reader):
            if idx >= rows:
                break
            yield row
        self.dataset.close()

    def get_absolute_url(self):
        """
        Return the absolute URL of the model
        """
        return reverse('dataset-detail', args=(str(self.id),))

    def __unicode__(self):
        return "{} - {} dataset with {} rows and {} dimensions, uploaded by {}".format(
            self.filename, self.datatype, self.length, self.dimensions, self.uploader
        )
