"""Urls."""

from django.urls import path

from .views import (ListTaskView,
                    CreateTaskView,
                    UpdateTaskView,
                    DeleteTaskView,
                    TaskView)


urlpatterns = [
    path('', ListTaskView.as_view(), name='tasks'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', DeleteTaskView.as_view(), name='delete_task'),
    path('<int:pk>/', TaskView.as_view(), name='task')
]
