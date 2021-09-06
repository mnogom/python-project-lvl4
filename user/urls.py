"""Urls."""

from django.urls import path

from .views import (ListUsersView,
                    CreateUserView,
                    UpdateUserView,
                    DeleteUserView,
                    LoginUserView,
                    LogoutUserView,
                    UserView)


urlpatterns = [
    path('users/', ListUsersView.as_view(), name='users'),
    path('users/create/', CreateUserView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', UpdateUserView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', DeleteUserView.as_view(), name='delete_user'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('users/<int:pk>/', UserView.as_view(), name='user'),
]
