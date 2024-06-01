from django.urls import path
from . import views

app_name = 'authe'

urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('refresh-token', views.CookieTokenRefreshView.as_view(), name='refresh-token'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('user', views.UserView.as_view(), name='user'),
]