# dataset.tasks
# Celery tasks for dataset models
#
# Author:   Allen Leis <allen.leis@gmail.com>
# Created:  Sun Aug 14 19:40:57 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: tasks.py [] allen.leis@gmail.com $

"""
Celery tasks for dataset models
"""

##########################################################################
# Imports
##########################################################################

import logging

from celery.utils.log import get_task_logger

from trinket.celery import app
from dataset.models import Dataset, DatasetVersion

##########################################################################
# Setup
##########################################################################

logger = get_task_logger(__name__)

##########################################################################
# Tasks
##########################################################################

@app.task(ignore_result=True)
def bundle_dataset_version(version_id):
    version = DatasetVersion.objects.get(pk=version_id)
    logger.info('Bundle Request: Dataset: {}, Version: {}'.format(
        version.dataset.name,
        version.version
    ))
    version.bundle()


##########################################################################
# Execution
##########################################################################

if __name__ == '__main__':
    pass
