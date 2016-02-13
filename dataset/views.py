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

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from dataset.models import Dataset
from dataset.forms import CreateDatasetForm

##########################################################################
## HTML/Web Views
##########################################################################

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

    def get_success_url(self):
        """
        Navigate to the newly created object
        """
        return self.object.get_absolute_url()

class DatasetListView(LoginRequiredMixin, ListView):

    model         = Dataset
    template_name = "dataset/list.html"
    paginate_by   = 25
    context_object_name = "datasets"

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        context['num_datasets']   = Dataset.objects.count()
        context['latest_dataset'] = Dataset.objects.latest().created
        return context


class DatasetDetailView(LoginRequiredMixin, DetailView):

    template_name = "dataset/detail.html"
    context_object_name = "dataset"
    model = Dataset
