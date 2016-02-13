# dataset.models
# Models for the multi-file dataset application.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 20:46:36 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: models.py [] benjamin@bengfort.com $

"""
Models for the multi-file dataset application.
"""

##########################################################################
## Imports
##########################################################################

from __future__ import unicode_literals

import os

from django.db import models
from model_utils import Choices
from trinket.utils import nullable
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from django.core.urlresolvers import reverse

##########################################################################
## Helper Models
##########################################################################

class License(TimeStampedModel):
    """
    Contains license boilerplate for datasets.
    """

    title = models.CharField(max_length=128, unique=True, null=False)
    text  = models.TextField(**nullable)

    class Meta:
        db_table = 'license'

    def __unicode__(self):
        return self.title

##########################################################################
## Dataset Collection
##########################################################################

class Dataset(TimeStampedModel):
    """
    A dataset is a container for multiple data files.
    """

    PRIVACY = Choices('private', 'protected', 'public')

    owner   = models.ForeignKey('account.Account', related_name='datasets')
    version = models.PositiveIntegerField(default=1, null=False, blank=True)
    name    = models.SlugField(max_length=60, null=False, allow_unicode=True)
    description = models.CharField(max_length=255, **nullable)
    url     = models.URLField(**nullable)
    privacy = models.CharField(max_length=10, choices=PRIVACY, default=PRIVACY.public)
    license = models.ForeignKey('dataset.License', related_name="+", **nullable)
    readme  = MarkupField(markup_type='markdown', help_text='Edit in Markdown', **nullable)

    class Meta:
        db_table = 'datasets'
        unique_together = ('name', 'owner')
        ordering = ('-created',)
        get_latest_by = 'created'

    def get_absolute_url(self):
        return reverse('dataset:detail', args=(self.owner.name, self.name))

    def __unicode__(self):
        return self.name

##########################################################################
## Data Files
##########################################################################

def dataset_directory_path(instance, filename):
    """
    File will be uploaded to:
    MEDIA_ROOT/datasets/<account>/<dataset>/<filename>
    """
    return os.path.join(
        'datasets',
        instance.dataset.owner.name,
        instance.dataset.name,
        filename
    )


class DataFile(TimeStampedModel):
    """
    A pointer to a version of a file containing data on disk.
    """

    DATATYPE    = Choices('csv', 'json', 'xml')

    uploader    = models.ForeignKey('auth.User', related_name='+')
    dataset     = models.ForeignKey('dataset.Dataset', related_name='files')
    data        = models.FileField(upload_to=dataset_directory_path)
    description = models.CharField(max_length=128, **nullable)
    dimensions  = models.PositiveIntegerField(default=0)
    length      = models.PositiveIntegerField(default=0)
    filesize    = models.PositiveIntegerField(default=0)
    signature   = models.CharField(max_length=44, unique=True, null=False, blank=True)
    datatype    = models.CharField(max_length=4, choices=DATATYPE, default=DATATYPE.csv)
    delimiter   = models.CharField(max_length=1, default=",")
    header      = models.BooleanField(default=True)

    class Meta:
        db_table = "dataset_files"
        ordering = ('-created',)
        get_latest_by = 'created'

    @property
    def name(self):
        """
        Returns the basename of the dataset
        """
        return os.path.basename(self.data.name)

    def read_csv_headers(self):
        """
        Returns the headers of the file
        """
        self.dataset.open('r')
        reader = csv.reader(self.dataset, delimiter=self.delimiter.encode('utf-8'))
        header = reader.next()
        self.dataset.close()
        return header

    def __unicode__(self):
        return self.name


##########################################################################
## Column Schema
##########################################################################

class ColumnSchema(TimeStampedModel):
    """
    Defines the column data types and names for data files.
    """

    # Specifies the various data types available.
    DTYPE     = Choices(
        'str', 'int', 'float', 'double', 'decimal', 'bool', 'date', 'obj',
    )

    datafile  = models.ForeignKey('dataset.DataFile', related_name='columns')
    datatype  = models.CharField(max_length=10, choices=DTYPE, **nullable)
    colindex  = models.PositiveSmallIntegerField(**nullable)
    name      = models.CharField(max_length=60, **nullable)
    formatter = models.CharField(max_length=80, **nullable)
