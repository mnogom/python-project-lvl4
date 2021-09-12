"""Views."""

import os

from django.views import View
from django.shortcuts import render


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', context={'env': os.getenv('ENV')})
