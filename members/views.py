# members.views
# Views for the members app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Sat Aug 22 09:25:37 2015 -0500
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the members app.
"""

##########################################################################
## Imports
##########################################################################


from members.permissions import IsAdminOrSelf
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from members.serializers import UserSerializer, PasswordSerializer

##########################################################################
## Views
##########################################################################


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A simple template view to display a member's profile.
    """

    template_name = "site/profile.html"

    def get_context_data(self, **kwargs):
        """
        Adds contextual information to the profile view.
        """
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user'] = self.request.user

        return context


class MemberListView(LoginRequiredMixin, ListView):
    """
    Listing and ordering of DDL members.
    """

    model = User
    template_name = "members/member_list.html"
    context_object_name = "member_list"
    paginate_by = 50

    def get_queryset(self):
        queryset = super(MemberListView, self).get_queryset()
        queryset = queryset.order_by('last_name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        context['member_count'] = User.objects.count()
        context['member_latest'] = User.objects.order_by('-date_joined')[0].date_joined

        return context


class MemberView(LoginRequiredMixin, DetailView):
    """
    A detail view of a user and their DDL participation. This view is very
    similar to a profile view except that it does not include the admin or
    personal aspects of the profile.
    """

    model = User
    template_name = "members/member_detail.html"
    context_object_name = 'member'
    slug_field  = "username"


##########################################################################
## API HTTP/JSON Views
##########################################################################


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @detail_route(methods=['post'], permission_classes=[IsAdminOrSelf])
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
