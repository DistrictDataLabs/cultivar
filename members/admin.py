# members.admin
# Administrative interface for members in Trinket.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:24:11 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: admin.py [] benjamin@bengfort.com $

"""
Administrative interface for members in Trinket.
"""

##########################################################################
## Imports
##########################################################################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import GenericStackedInline

from members.models import Profile
from account.models import Account

##########################################################################
## Inline Adminstration
##########################################################################

class ProfileInline(admin.StackedInline):
    """
    Inline administration descriptor for profile object
    """

    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class AccountInline(GenericStackedInline):
    """
    Inline administration descriptor for account object
    """

    model = Account
    max_num = 1
    can_delete = False
    ct_fk_field = 'owner_id'
    verbose_name_plural = 'account'


class UserAdmin(UserAdmin):
    """
    Define new User admin
    """

    inlines = (ProfileInline, AccountInline)


class ProfileAdmin(admin.ModelAdmin):
    """
    Editing profiles without editing the user field.
    """

    readonly_fields = ('user', )
    fields = ('user', 'organization', 'location', 'biography')


##########################################################################
## Register Admin
##########################################################################

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
