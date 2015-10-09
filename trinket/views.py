# trinket.views
# Default application views for the system.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 14:30:37 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Default application views for the system.
"""

##########################################################################
## Imports
##########################################################################

import trinket

from datetime import datetime
from django.views.generic import TemplateView

from rest_framework import viewsets
from rest_framework.response import Response

##########################################################################
## Views
##########################################################################


class HomePageView(TemplateView):

    template_name = "site/home.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        return context

##########################################################################
## API Views for this application
##########################################################################


class HeartbeatViewSet(viewsets.ViewSet):
    """
    Endpoint for heartbeat checking, including the status and version.
    """

    def list(self, request):
        return Response({
            "status": "ok",
            "version": trinket.get_version(),
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        })
