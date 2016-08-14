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
from dataset.models import Dataset, DataFile, DatasetVersion


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
        dataset = Dataset.objects.create(**self.cleaned_data)
        import pdb; pdb.set_trace()
        return dataset


##########################################################################
## Upload Form
##########################################################################

DATASET_ERROR_MSGS = {
    "required": "Please select a file to upload.",
    "invalid": "The dataset you provided is invalid, please select another.",
    "missing": "The dataset you specified is missing, please select another.",
    "empty": "The uploaded dataset is empty, cannot upload.",
    "max_length": "The dataset is too big, please limit datasets to a GB.",
}


class DataFileUploadForm(forms.Form):
    """
    Post a CSV dataset and manage its description via this form.
    """

    datafile = forms.FileField(required=True, error_messages=DATASET_ERROR_MSGS)
    dataset  = forms.IntegerField(required=True, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(DataFileUploadForm, self).__init__(*args, **kwargs)

    def clean_dataset(self):
        """
        Collect the dataset object from the cleaned data.
        """
        try:
            return Dataset.objects.get(pk=self.cleaned_data['dataset'])
        except Dataset.DoesNotExist:
            raise forms.ValidationError(
                "Dataset with id '{}' does not exist!"
            )

    def save(self):
        """
        Associate the file with the dataset and upload to S3.
        """
        dataset = self.cleaned_data['dataset']
        files = []
        if dataset.latest_version():
            files = dataset.latest_version().files.all()

        version = DatasetVersion.objects.create(
            version=dataset.next_version_number(),
            dataset=dataset,
        )
        version.files = files

        return DataFile.objects.create(
            version=version,
            uploader=self.request.user,
            data=self.cleaned_data['datafile']
        )
