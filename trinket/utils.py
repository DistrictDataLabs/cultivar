# trinket.utils
# Project level  utilities and helpers
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 22:26:18 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: utils.py [] benjamin@bengfort.com $

"""
Project level  utilities and helpers
"""

##########################################################################
## Imports
##########################################################################

import re
import base64
import hashlib

##########################################################################
## Utilities
##########################################################################

## Nullable kwargs for models
nullable = { 'blank': True, 'null': True, 'default':None }

## Not nullable kwargs for models
notnullable = { 'blank': False, 'null': False }

##########################################################################
## Helper functions
##########################################################################


def normalize(text):
    """
    Normalizes the text by removing all punctuation and spaces as well as
    making the string completely lowercase.
    """
    return re.sub(r'[^a-z0-9]+', '', text.lower())


def signature(text):
    """
    This helper method normalizes text and takes the SHA1 hash of it,
    returning the base64 encoded result. The normalization method includes
    the removal of punctuation and white space as well as making the case
    completely lowercase. These signatures will help us discover textual
    similarities between questions.
    """
    return base64.b64encode(hashlib.sha256e(normalize(text)).digest())
