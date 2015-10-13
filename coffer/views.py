# coffer.views
# Views and interaction logic for the coffer app.
#
# Author:   Benjamin Bengfort <bbengfort@districtdatalabs.com>
# Created:  Thu Oct 08 21:46:26 2015 -0400
#
# Copyright (C) 2015 District Data Labs
# For license information, see LICENSE.txt
#
# ID: views.py [] benjamin@bengfort.com $

"""
Views and interaction logic for the coffer app.
"""

##########################################################################
## Imports
##########################################################################

from django.db import IntegrityError
from braces.views import LoginRequiredMixin
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView

from coffer.models import Dataset
from coffer.forms import DatasetUploadForm

##########################################################################
## HTML/Web Views
##########################################################################

class DatasetUploadView(LoginRequiredMixin, FormView):

    template_name = "site/upload.html"
    form_class = DatasetUploadForm
    success_url = "/upload"


    def get_form_kwargs(self):
        """
        Add the request to the kwargs
        """
        kwargs = super(DatasetUploadView, self).get_form_kwargs()
        kwargs['request'] = self.request
        print kwargs
        return kwargs

    def form_valid(self, form):
        try:
            form.save()
            return super(DatasetUploadView, self).form_valid(form)
        except IntegrityError:
            form.add_error(None, "Duplicate file detected! Cannot upload the same file twice.")
            return super(DatasetUploadView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        """
        Add ten most recent uploads to context
        """
        context = super(DatasetUploadView, self).get_context_data(**kwargs)
        context['upload_history'] = Dataset.objects.order_by('-created')[:10]
        return context


class DatasetDetailView(LoginRequiredMixin, DetailView):

    template_name = "site/dataset.html"
    model = Dataset
