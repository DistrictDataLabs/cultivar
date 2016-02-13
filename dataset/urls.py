# dataset.urls
# Routing for the dataset app
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 23:33:10 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
Routing for the dataset app
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import url

from dataset.views import *

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = (
    url(r'^create/$', DatasetCreateView.as_view(), name='create'),
    url(r'^datasets/$', DatasetListView.as_view(), name='listing'),
    url(r'^datasets/(?P<pk>\d+)/$', DatasetDetailView.as_view(), name='detail'),
)
