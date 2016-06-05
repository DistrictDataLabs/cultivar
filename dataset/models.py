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
import csv
import codecs

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

    def __str__(self):
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

    def latest_file(self):
        return self.files.latest()

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:dataset-detail', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('dataset:detail', args=(self.owner.name, self.name))

    def __str__(self):
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
        ordering = ('data',)
        get_latest_by = 'modified'

    @property
    def name(self):
        """
        Returns the basename of the dataset
        """
        if self.data:
            return os.path.basename(self.data.name)
        return ""

    def read_csv_headers(self):
        """
        Method that reads first line of datafile to retrieve array of column names (header)
        Also counts amount of lines in csv file
        Returns tuple (header, amount_of_lines) for csv file
        Returns None for non-csv file (TODO)
        NOTE: Why can't we close this file without errors?
        """
        self.data.open('rb')
        if self.datatype == self.DATATYPE.csv:
            # FieldFile produces stream of bytes, csv expects stream of string
            # decode first line into string (replacing non-utf-8 chars with escaped values)
            first_line_decoded = codecs.iterdecode(self.data, encoding='utf-8', errors='replace')
            reader = csv.reader(first_line_decoded, delimiter=self.delimiter)
            header = next(reader)
            length = sum(1 for row in reader)  # might be a bit slow
            # No close method allowed?
            return header, length
        return None  # ?? what to return for not a csv

    def __str__(self):
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
