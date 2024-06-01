from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('users', views.UserProfileListAndCreateView.as_view(), name='users-list'),
    path('users/<int:id>', views.UserProfileDetailsView.as_view(), name='user-details'),
]
