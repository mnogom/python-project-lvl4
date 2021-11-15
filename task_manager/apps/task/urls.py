"""Urls."""

from django.urls import path

from .views import (ListTaskView,
                    CreateTaskView,
                    UpdateTaskView,
                    DeleteTaskView,
                    TaskView)


app_name = 'task'
urlpatterns = [
    path('', ListTaskView.as_view(), name='list'),
    path('create/', CreateTaskView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete'),
    path('<int:pk>/', TaskView.as_view(), name='sample')
]
