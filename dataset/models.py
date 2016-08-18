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
import zipfile
import zlib
import shutil
import random
import string

from django.core.exceptions import ObjectDoesNotExist

from django.db import models
from model_utils import Choices
from trinket.utils import (nullable, memoized)
from markupfield.fields import MarkupField
from model_utils.models import TimeStampedModel
from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile
import csv
import codecs

# from dataset.signals import bundle_version

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
    # version = models.PositiveIntegerField(default=1, null=False, blank=True)
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

    @property
    def version(self):
        return self.versions.latest().version

    def next_version_number(self):
        latest = self.latest_version()
        if latest:
            return latest.version + 1
        else:
            return 1

    def latest_version(self):
        try:
            return self.versions.latest()
        except ObjectDoesNotExist:
            return None

    def latest_file(self):
        version = self.latest_version()
        if version:
            return self.latest_version().files.latest()
        else:
            return None

    def get_api_detail_url(self):
        """
        Returns the API detail endpoint for the object
        """
        return reverse('api:dataset-detail', args=(self.pk,))

    def get_absolute_url(self):
        return reverse('dataset:detail', args=(self.owner.name, self.name))

    def is_starred(self, user_id):
        try:
            self.users_starred.get(user_id=user_id)
            return True
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return self.name


##########################################################################
## Dataset Version
##########################################################################

def dataset_version_directory_path(instance, filename):
    """
    File will be uploaded to:
    MEDIA_ROOT/datasets/<account>/<dataset>/bundles/<name>.zip
    """
    return os.path.join(
        'datasets',
        instance.dataset.owner.name,
        instance.dataset.name,
        'bundles',
        instance.bundle_filename
    )

class DatasetVersion(TimeStampedModel):
    """
    A join model to connect DataFiles to Datasets tied to a version number
    """
    version = models.PositiveIntegerField(null=False, blank=False)
    dataset = models.ForeignKey('dataset.Dataset', related_name='versions')
    bundle_available = models.BooleanField(default=False)
    data = models.FileField(upload_to=dataset_version_directory_path)

    class Meta:
        db_table = "dataset_versions"
        get_latest_by = 'created'
        ordering = ('-created',)

    @property
    def bundle_filename(self):
        """
        Constructs the bundle filename based off of dataset name and version number
        """
        return '{}-{}.zip'.format(
            self.dataset.name,
            self.__str__()
        )

    @memoized
    def temp_directory(self):
        """
        Returns a path to a temporary working directory
        """
        prefix = 'cultivar-'
        length = 12
        name = None

        while not name:
            tmp = prefix + ''.join(random.choice(string.ascii_lowercase)
                                   for i in range(length))
            path = os.path.abspath(os.path.join(os.sep, 'tmp', tmp))
            if not os.path.isdir(path):
                os.mkdir(path)
                return path

    def bundle(self):
        """
        Public method to download files, bundle them, upload the bundle to s3
        and then update the version record accordingly
        """
        try:
            self._download(self.temp_directory)
            self._zip(self.temp_directory)
            self._upload(self.temp_directory)

            self.bundle_available = True
            self.save()
        finally:
            self._clean(self.temp_directory)

    def _clean(self, path):
        """
        Removes the temporary work directory
        """
        shutil.rmtree(path)

    def _zip(self, path):
        """
        Creates zip file, then adds license, readme, and uploaded files
        """
        files = [os.path.join(path, f) for f in os.listdir(path)]
        zf = zipfile.ZipFile(os.path.join(path, self.bundle_filename), mode='w')
        try:
            zf.writestr('readme.md', self.dataset.readme.raw)
            zf.writestr('license.txt', self.dataset.license.text)
            for f in files:
                zf.write(f, compress_type=zipfile.ZIP_DEFLATED, arcname=os.path.basename(f))
        finally:
            zf.close()

    def _upload(self, path):
        """
        Uploads bundle file in given path/directory to S3
        """
        upload_path = dataset_version_directory_path(self, '')
        f = open(os.path.join(path, self.bundle_filename), 'rb')
        ff = ContentFile(f.read())
        self.data.save(upload_path, ff, save=False)

    def _download(self, path):
        """
        Downloads this version's files to the given path
        """
        for f in self.files.all():
            filename = os.path.basename(f.data.name)
            with open(os.path.join(path, filename), 'wb') as fh:
                fh.write(f.data.read())

    def __str__(self):
        return 'v{}'.format(self.version)



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
        instance.version.dataset.owner.name,
        instance.version.dataset.name,
        filename
    )


class DataFile(TimeStampedModel):
    """
    A pointer to a version of a file containing data on disk.
    """

    DATATYPE    = Choices('csv', 'json', 'xml')

    uploader    = models.ForeignKey('auth.User', related_name='+')
    version     = models.ForeignKey('dataset.DatasetVersion', related_name='files')
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


##########################################################################
## Starred Dataset Schema (User-Dataset many-to-many)
##########################################################################


class StarredDataset(TimeStampedModel):
    """
    Model for many-to-many relation between datasets and users through starring.
    """
    user = models.ForeignKey('auth.User', related_name='starred_datasets')
    dataset = models.ForeignKey('dataset.Dataset', related_name='users_starred')

    class Meta:
        unique_together = (('user', 'dataset'),)
