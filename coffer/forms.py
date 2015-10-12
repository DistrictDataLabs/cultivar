# coffer.forms
# HTML Forms for interacting with the Coffer app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Mon Oct 12 05:35:57 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: forms.py [] benjamin@bengfort.com $

"""
HTML Forms for interacting with the Coffer app.
"""

##########################################################################
## Imports
##########################################################################

from django import forms
from coffer.models import Dataset

##########################################################################
## Upload Form
##########################################################################

class DatasetUploadForm(forms.Form):
    """
    Post a CSV dataset and manage its description via this form.
    """

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DatasetUploadForm, self).__init__(*args, **kwargs)
