import os

from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

from django.utils.translation import ugettext


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # return HttpResponse(ugettext("Hello"))
        return render(request, 'index.html', context={'env': os.getenv('ENV')})
