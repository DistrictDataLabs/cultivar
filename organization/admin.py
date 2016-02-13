# organization.admin
# CMS (Admin) stuff for organizations in Trinket.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Wed Feb 10 21:34:22 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
CMS (Admin) stuff for organizations in Trinket.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from organization.models import Organization, Role
from account.models import Account

##########################################################################
## Inline Adminstration
##########################################################################

class AccountInline(GenericStackedInline):
    """
    Inline administration descriptor for account object
    """

    model = Account
    max_num = 1
    can_delete = False
    ct_fk_field = 'owner_id'
    verbose_name_plural = 'account'


class OrganizationAdmin(admin.ModelAdmin):
    """
    Define new Organization admin
    """

    inlines = (AccountInline,)

##########################################################################
## Register Admin
##########################################################################

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role)
