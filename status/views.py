from django.shortcuts import render, redirect, resolve_url
from django.http import HttpResponse
from django.views import View
from django.views.generic.list import ListView
from django.contrib import messages
from django.utils.translation import gettext

from task_manager import http_status
from user.decorators import required_login

from .selectors import (get_all_status,
                        get_status_by_pk)
from .services import (create_status,
                       update_status,
                       delete_status)
from .forms import StatusForm
from .models import Status


class StatusView(ListView):
    """List of users view."""

    model = Status
    template_name = 'statuses.html'


    @required_login
    def get(self, request, *args, **kwargs):
        return super().get(self, request, *args, **kwargs)


class CreateStatusView(View):

    @required_login
    def get(self, request, *args, **kwargs):
        return render(request=request,
                      template_name='create_status.html',
                      context={'form': StatusForm},
                      status=http_status.HTTP_200_OK)

    @required_login
    def post(self, request, *args, **kwargs):
        form = create_status(request.POST)
        if form.is_valid():
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Status was created'))
            return redirect(resolve_url('statuses'))
        return render(request=request,
                      template_name='create_status.html',
                      context={'form': form},
                      status=http_status.HTTP_400_BAD_REQUEST)


class UpdateStatusView(View):

    @required_login
    def get(self, request, pk, *args, **kwargs):
        status = get_status_by_pk(pk)
        form = StatusForm(instance=status)
        return render(request=request,
                      template_name='edit_status.html',
                      context={'form': form,
                               'status_pk': pk},
                      status=http_status.HTTP_200_OK)

    @required_login
    def post(self, request, pk, *args, **kwargs):
        form = update_status(request.POST, pk)
        if form.is_valid():
            messages.add_message(request=request,
                                 level=messages.SUCCESS,
                                 message=gettext('Status was updated'))
            return redirect(resolve_url('update_status', pk=pk))
        return render(request=request,
                      template_name='edit_status.html',
                      context={'form': form,
                               'status_pk': 'pk'},
                      status=http_status.HTTP_200_OK)


class DeleteStatusView(View):

    @required_login
    def get(self, request, pk, *args, **kwargs):
        status = get_status_by_pk(pk)
        return render(request=request,
                      template_name='delete_status.html',
                      context={'status': status},
                      status=http_status.HTTP_200_OK)

    @required_login
    def post(self, request, pk, *args, **kwargs):
        delete_status(pk)
        messages.add_message(request=request,
                             level=messages.SUCCESS,
                             message=gettext('Status was deleted'))
        return redirect(resolve_url('statuses'))
