# trinket.urls
# Application url definition and routers.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 14:28:14 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
Application url definition and routers.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from rest_framework import routers
from django.conf.urls import include, url

from django.views.generic import TemplateView

from trinket.views import *
from coffer.views import *

##########################################################################
## Endpoint Discovery
##########################################################################

## API
router = routers.DefaultRouter()
router.register(r'status', HeartbeatViewSet, "status")

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = [
    # Admin URLs
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Application URLs
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^terms/$', TemplateView.as_view(template_name='site/legal/terms.html'), name='terms'),
    url(r'^privacy/$', TemplateView.as_view(template_name='site/legal/privacy.html'), name='privacy'),
    url(r'^upload/$', DatasetUploadView.as_view(), name='upload'),
    url(r'^dataset/(?P<pk>\d+)/$', DatasetDetailView.as_view(), name='dataset-detail'),

    # Authentication URLs
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('^accounts/', include('django.contrib.auth.urls')),

    ## REST API Urls
    url(r'^api/', include(router.urls, namespace="api")),
]
