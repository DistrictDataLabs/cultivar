# account.mixins
# Mixins and helpers to access the account from associated models.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 21:11:53 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: mixins.py [] benjamin@bengfort.com $

"""
Mixins and helpers to access the account from associated models.
"""

##########################################################################
## Imports
##########################################################################

from account.models import Account
from django.contrib.contenttypes.models import ContentType


##########################################################################
## Account Mixin
##########################################################################

class AccountMixin(object):
    """
    Make sure that the mixin comes before models.Model! That way if a model
    field called `account` is created, it will be overriden by the model.
    """

    @property
    def account(self):
        """
        Returns the account for the given object, or none if it doesn't exist.
        """
        ctype = ContentType.objects.get_for_model(self.__class__)
        try:
            return Account.objects.get(
                content_type = ctype, owner_id = self.id
            )
        except self.DoesNotExist:
            return None
        
