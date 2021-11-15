"""Urls."""

from django.urls import path

from .views import (ListUsersView,
                    CreateUserView,
                    UpdateUserView,
                    DeleteUserView,
                    UserView)


app_name = 'user'
urlpatterns = [
    path('', ListUsersView.as_view(), name='list'),
    path('create/', CreateUserView.as_view(), name='create'),
    path('<int:pk>/update/', UpdateUserView.as_view(), name='update'),
    path('<int:pk>/delete/', DeleteUserView.as_view(), name='delete'),
    path('<int:pk>/', UserView.as_view(), name='sample'),
]
