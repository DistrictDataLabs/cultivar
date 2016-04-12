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
    url(r'^(?P<account>[\w-]+)/(?P<slug>[\w-]+)/$', DatasetDetailView.as_view(), name='detail'),
    url(r'^(?P<account>[\w-]+)/(?P<slug>[\w-]+)/upload/$', DataFileUploadView.as_view(), name='upload'),
    url(r'^(?P<account>[\w-]+)/(?P<slug>[\w-]+)/schema/$', DatasetSchemaView.as_view(), name='schema'),
    url(r'^(?P<account>[\w-]+)/(?P<slug>[\w-]+)/explore/$', DatasetExploreView.as_view(), name='explore'),
    url(r'^(?P<account>[\w-]+)/(?P<slug>[\w-]+)/settings/$', DatasetSettingsView.as_view(), name='settings'),
)
