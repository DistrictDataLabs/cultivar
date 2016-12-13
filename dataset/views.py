# dataset.views
# Views for the dataset application.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Fri Feb 12 23:48:52 2016 -0500
#
# Copyright (C) 2016 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views for the dataset application.
"""

##########################################################################
## Imports
##########################################################################
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from dataset.models import Dataset, StarredDataset
from dataset.forms import CreateDatasetForm
from dataset.forms import DataFileUploadForm

from rest_framework import viewsets
from dataset.serializers import DatasetSerializer, StarredDatasetSerializer

##########################################################################
## HTML/Web Views
##########################################################################
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, \
    HTTP_500_INTERNAL_SERVER_ERROR


class DatasetCreateView(LoginRequiredMixin, CreateView):

    template_name = "dataset/create.html"
    form_class    = CreateDatasetForm


    def get_form_kwargs(self):
        """
        Add the request to the kwargs
        """
        kwargs = super(DatasetCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        try:
            return super(DatasetCreateView, self).form_valid(form)
        except IntegrityError:
            form.add_error(None, "A dataset with this name already exists, please choose another.")
            return super(DatasetCreateView, self).form_invalid(form)

    def get_success_url(self):
        """
        Navigate to the newly created object
        """
        return self.object.get_absolute_url()


class DataFileUploadView(LoginRequiredMixin, FormView):

    template_name = 'dataset/upload.html'
    form_class = DataFileUploadForm

    def get_form_kwargs(self):
        """
        Add the request to the kwargs
        """
        kwargs = super(DataFileUploadView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """
        If there is an IntegrityError, then returns form invalid.
        """
        try:
            self.object = form.save()
            return super(DataFileUploadView, self).form_valid(form)
        except IntegrityError:
            form.add_error(None, "Duplicate file detected! Cannot upload the same file twice.")
            return super(DataFileUploadView, self).form_invalid(form)

    def get_success_url(self):
        """
        Returns the user back to the dataset view.
        """
        return self.object.version.dataset.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(DataFileUploadView, self).get_context_data(**kwargs)
        if hasattr(self, 'object'):
            context['dataset'] = self.object
        else:
            context['dataset'] = Dataset.objects.get(
                owner__name = self.kwargs.get('account'),
                name = self.kwargs.get('slug'),
            )

        return context


class DatasetListView(LoginRequiredMixin, ListView):

    model         = Dataset
    template_name = "dataset/list.html"
    paginate_by   = 25
    context_object_name = "datasets"

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        context['num_datasets']   = Dataset.objects.count()
        if context['num_datasets'] > 0:
            context['latest_dataset'] = Dataset.objects.latest().created
        return context


class DatasetDetailView(LoginRequiredMixin, DetailView):

    template_name = "dataset/detail/files.html"
    context_object_name = "dataset"
    model = Dataset
    slug_field = "name"
    panel_name = "files"

    def get_queryset(self):
        """
        Returns a dataset based on username/dataset_name arguments.
        """
        return self.model.objects.filter(
            owner__name = self.kwargs.get('account', None),
        )

    def get_context_data(self, **kwargs):
        context = super(DatasetDetailView, self).get_context_data(**kwargs)
        context['panel_name'] = self.panel_name
        context['dataset_is_starred'] = context['dataset'].is_starred(self.request.user.id)
        return context


class DatasetSchemaView(DatasetDetailView):

    template_name = "dataset/detail/schema.html"
    panel_name = "schema"


class DatasetExploreView(DatasetDetailView):

    template_name = "dataset/detail/explore.html"
    panel_name = "explore"


class DatasetSettingsView(DatasetDetailView):

    template_name = "dataset/detail/settings.html"
    panel_name = "settings"


##########################################################################
## JSON/API Views
##########################################################################

class DatasetViewSet(viewsets.ModelViewSet):

    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class StarredDatasetsViewSet(viewsets.ModelViewSet):

    serializer_class = StarredDatasetSerializer
    model = StarredDataset

    def get_queryset(self):
        """
        Returns datasets starred by current user.
        """
        queryset = self.model.objects.all()
        try:
            user_id = self.request.user.id
            return queryset.filter(user_id=user_id)
        except AttributeError:
            return []  # empty result for not logged in users

    def create(self, request, **kwargs):
        """
        Star some dataset for current user.
        """
        dataset_id = request.data['dataset_id']
        user_id = request.user.id

        serialized_data = self.serializer_class(data={
          'dataset': dataset_id,
          'user': user_id
        })

        if serialized_data.is_valid():
            self.serializer_class.save(serialized_data)
            return Response({'status': 'starred status created'}, status=HTTP_201_CREATED)
        return Response({'errors': serialized_data.errors}, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        """
        Delete star for some dataset set by user.
        """
        try:
            dataset_starred = self.model.objects.all().get(dataset_id=pk, user_id=request.user.id)
            dataset_starred.delete()
            return Response({'status': 'starred status deleted'}, status=HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'status': 'starred status to delete not found'}, status=HTTP_404_NOT_FOUND)
        except MultipleObjectsReturned:  # couldn't be multiple b/c of complex PK in model, means something went wrong
            return Response(status=HTTP_500_INTERNAL_SERVER_ERROR)
