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

from members.models import Profile, Account

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


class UserAdmin(UserAdmin):
    """
    Define new User admin
    """

    inlines = (ProfileInline, )


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
admin.site.register(Account)
