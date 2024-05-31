from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter, SearchFilter
from .models import UserProfile
from .serializers import UserProfileSerializer
from .pagination import UserListPagination

# Create your views here.

class UsersList(ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = UserListPagination
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = '__all__'
    search_fields = ('first_name', 'last_name')