# trinket.settings.testing
# Testing settings to enable testing on Travis
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Sep 12 16:18:38 2014 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: testing.py [] bbengfort@districtdatalabs.com $

"""
Testing settings to enable testing on Travis
"""

##########################################################################
## Imports
##########################################################################

import os
from .base import *

##########################################################################
## Testing Settings
##########################################################################

## Debugging Settings
DEBUG            = True

## Hosts
ALLOWED_HOSTS    = ['localhost', '127.0.0.1']
