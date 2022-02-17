"""Views."""

import os

from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

import rollbar


class HomeView(View):
    """Home (index) view."""

    def get(self, request, *args, **kwargs):
        """Method GET to check if rollbar is available."""

        if request.GET.get('rollbar-test'):
            rollbar.report_message(message=f'This is test from '
                                           f'"python-project-lvl4" '
                                           f'with mode "{os.getenv("ENV")}"',
                                   level="info")
            return redirect(reverse_lazy('index'))

        return render(request, 'index.html', context={'env': os.getenv('ENV')})
