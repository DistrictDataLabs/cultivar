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

DATASET_ERROR_MSGS = {
    "required": "Please select a dataset to upload.",
    "invalid": "The dataset you provided is invalid, please select another.",
    "missing": "The dataset you specified is missing, please select another.",
    "empty": "The uploaded dataset is empty, cannot upload.",
    "max_length": "The dataset is too big, please limit datasets to a GB.",
}

class DatasetUploadForm(forms.Form):
    """
    Post a CSV dataset and manage its description via this form.
    """

    dataset = forms.FileField(required=True, error_messages=DATASET_ERROR_MSGS)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DatasetUploadForm, self).__init__(*args, **kwargs)

    def save(self):
        """
        Save the dataset to S3
        """
        return Dataset.objects.create(
            dataset=self.cleaned_data['dataset'], uploader=self.request.user
        )
