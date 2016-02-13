# dataset.forms
# HTML forms for managing dataset objects directly.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 23:53:25 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: forms.py [] benjamin@bengfort.com $

"""
HTML forms for managing dataset objects directly.
"""

##########################################################################
## Imports
##########################################################################

from django import forms
from dataset.models import Dataset

##########################################################################
## Create Dataset Form
##########################################################################

class CreateDatasetForm(forms.ModelForm):
    """
    A simple mechanism for creating a dataset on the fly.
    """

    class Meta:
        model = Dataset
        fields = ['name', 'description', 'url', 'privacy', 'license',]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateDatasetForm, self).__init__(*args, **kwargs)

    def save(self):
        """
        Save the dataset with the new meta information.
        """
        self.cleaned_data['owner'] = self.request.user.profile.account
        return Dataset.objects.create(**self.cleaned_data)
