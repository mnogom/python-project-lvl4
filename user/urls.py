"""Urls."""

from django.urls import path

from .views import (ListUsersView,
                    NewUserView,
                    EditUserView,
                    DeleteUserView,
                    LoginView,
                    LogoutView)


urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('users/create/', NewUserView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', EditUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
