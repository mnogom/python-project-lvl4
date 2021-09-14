"""Views."""

import os

from django.views import View
from django.shortcuts import render


class HomeView(View):
    """Home (index) view."""

    def get(self, request, *args, **kwargs):
        """Method GET."""

        return render(request, 'index.html', context={'env': os.getenv('ENV')})
