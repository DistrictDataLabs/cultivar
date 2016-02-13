# members.urls
# URLs for routing the members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 23:30:10 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: urls.py [] benjamin@bengfort.com $

"""
URLs for routing the members app.
"""

##########################################################################
## Imports
##########################################################################

from django.conf.urls import url
from members.views import *

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = (
    url(r'^members/$', MemberListView.as_view(), name='list'),
    url(r'^(?P<slug>[\w-]+)/$', MemberView.as_view(), name='detail'),
)
