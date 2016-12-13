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

from dataset.models import DataFile
from django.db.models.signals import pre_delete, pre_save, post_save
from django.dispatch.dispatcher import receiver
from django.dispatch import Signal

from dataset.tasks import bundle_dataset_version

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

##########################################################################
## DatasetVersion Signals
##########################################################################

bundle_version = Signal(providing_args=["instance"])

@receiver(bundle_version)
def dataset_version_bundle_enqueue(sender, instance, **kwargs):
    logger.warn("Task Enqueue Request: dataset_version_bundle_enqueue, {}".format(
        instance.id
    ))
    bundle_dataset_version.delay(instance.id)

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

    """
    sha = hashlib.sha256()
    instance.data.open('rb')
    if instance.data.multiple_chunks():
        for chunk in instance.data.chunks():
            sha.update(chunk)
    else:
        sha.update(instance.data.read())

    if instance.datatype == instance.DATATYPE.csv:
        header, length = instance.read_csv_headers()
        instance.dimensions = len(header)
        instance.length = length

    instance.signature = base64.b64encode(sha.digest())
    instance.filesize  = instance.data.size


@receiver(pre_delete, sender=DataFile)
def datafile_delete(sender, instance, **kwargs):
    """
    Deletes the file in S3 when datafile record is deleted.
    """
    instance.data.delete(False)
