# coffer.signals
# Signals for handling coffer models and other app details.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Oct 11 17:05:26 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals for handling coffer models and other app details.
"""

##########################################################################
## Imports
##########################################################################

import base64
import hashlib
import unicodecsv as csv

from coffer.models import Dataset
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver

##########################################################################
## Dataset Signals
##########################################################################

@receiver(pre_save, sender=Dataset)
def dataset_file_compute(sender, instance, **kwargs):
    """
    Computes the filesize and SHA1 signature of the dataset. For CSV files
    this also computes the length and dimensions.

    TODO: Make this a lot better.
    NOTE: Why can't we close this file without errors?
    """
    sha = hashlib.sha256()
    instance.dataset.open('rb')
    if instance.dataset.multiple_chunks():
        for chunk in instance.dataset.chunks():
            sha.update(chunk)
    else:
        sha.update(instance.dataset.read())

    if instance.datatype == instance.DATATYPE.csv:
        reader = csv.reader(instance.dataset, delimiter=instance.delimiter.encode('utf-8'))
        header = reader.next()
        instance.dimensions = len(header)
        instance.length = sum(1 for row in reader)

    if not instance.title:
        instance.title = instance.filename

    instance.signature = base64.b64encode(sha.digest())
    instance.filesize  = instance.dataset.size

    # No close method allowed?


@receiver(pre_delete, sender=Dataset)
def dataset_delete(sender, instance, **kwargs):
    """
    Deletes the dataset in S3 when dataset record is deleted.
    """
    instance.dataset.delete(False)
