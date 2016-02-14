# dataset.signals
# Signals for handling dataset models and other app details.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 20:45:43 2016 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: signals.py [] benjamin@bengfort.com $

"""
Signals for handling dataset models and other app details.
"""

##########################################################################
## Imports
##########################################################################

import base64
import hashlib
import unicodecsv as csv

from dataset.models import DataFile
from django.db.models.signals import pre_delete, pre_save
from django.dispatch.dispatcher import receiver

##########################################################################
## DataFile Signals
##########################################################################

@receiver(pre_save, sender=DataFile)
def datafile_file_compute(sender, instance, **kwargs):
    """
    Computes the filesize and SHA1 signature of the dataset. For CSV files
    this also computes the length and dimensions.

    TODO: Switch over to Celery async processing for this
    TODO: Make this a lot better.
    NOTE: Why can't we close this file without errors?
    """
    sha = hashlib.sha256()
    instance.data.open('rb')
    if instance.data.multiple_chunks():
        for chunk in instance.data.chunks():
            sha.update(chunk)
    else:
        sha.update(instance.data.read())

    if instance.datatype == instance.DATATYPE.csv:
        reader = csv.reader(instance.data, delimiter=instance.delimiter.encode('utf-8'))
        header = reader.next()
        instance.dimensions = len(header)
        instance.length = sum(1 for row in reader)

    instance.signature = base64.b64encode(sha.digest())
    instance.filesize  = instance.data.size

    # No close method allowed?


@receiver(pre_delete, sender=DataFile)
def datafile_delete(sender, instance, **kwargs):
    """
    Deletes the file in S3 when datafile record is deleted.
    """
    instance.data.delete(False)
