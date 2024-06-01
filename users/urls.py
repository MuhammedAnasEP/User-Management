from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users', views.UsersListView.as_view(), name='users-list'),
    path('users/<int:id>', views.UserDetailsView.as_view(), name='user-details'),
]
