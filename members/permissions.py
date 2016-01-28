# members.permissions
# Extra permissions for the Django Rest Framework views.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sun Aug 23 07:38:55 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: permissions.py [] benjamin@bengfort.com $

"""
Extra permissions for the Django Rest Framework views.
"""

##########################################################################
## Imports
##########################################################################

from rest_framework import permissions

##########################################################################
## Permissions
##########################################################################

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow only owners of an object to edit.
    Note, this permission assumes there is an `author` attribute on the
    object that maps to an `auth.User` instance.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user

class IsAdminOrSelf(permissions.BasePermission):
    """
    Object-level permission to only allow modifications to a User object
    if the request.user is an administrator or you are modifying your own
    user object.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.user == obj
