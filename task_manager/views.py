import os

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

from django.utils.translation import gettext


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(gettext("Hello"))
        return render(request, 'index.html', context={'env': os.getenv('ENV')})
