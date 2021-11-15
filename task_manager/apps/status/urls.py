"""Urls."""

from django.urls import path

from .views import (ListStatusView,
                    CreateStatusView,
                    UpdateStatusView,
                    DeleteStatusView)


app_name = 'status'
urlpatterns = [
    path('', ListStatusView.as_view(), name='list'),
    path('create/', CreateStatusView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateStatusView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteStatusView.as_view(), name='delete'),
]
