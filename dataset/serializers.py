# dataset.serializers
# Serializers for API dataset interaction.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Tue Apr 12 13:28:14 2016 -0400
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: serializers.py [] benjamin@bengfort.com $

"""
Serializers for API dataset interaction.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import serializers
from dataset.models import Dataset, StarredDataset


##########################################################################
## Dataset Serializers
##########################################################################

class DatasetSerializer(serializers.HyperlinkedModelSerializer):

    api_url = serializers.HyperlinkedIdentityField(
                view_name='api:dataset-detail'
                )

    owner   = serializers.StringRelatedField(many=False)
    license = serializers.StringRelatedField(many=False)

    class Meta:
        model  = Dataset
        fields = (
            'api_url', 'owner', 'version', 'name', 'description',
            'url', 'privacy', 'license', 'readme',
        )


class StarredDatasetSerializer(serializers.ModelSerializer):
    """
    Serializes the StarredDataset object
    """
    class Meta:
        model  = StarredDataset
        fields = ('user', 'dataset')