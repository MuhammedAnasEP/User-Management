from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer
from .pagination import UserListPagination

# Create your views here.

class UsersListView(ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = UserListPagination
    filter_backends = (OrderingFilter, SearchFilter)
    ordering_fields = '__all__'
    search_fields = ('first_name', 'last_name')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(APIView):

    def get(self, request, id):
        try:
            user = UserProfile.objects.get(id = id)
        except:
            content = {'status':f'User with id {id} not availvable.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user, many=False)
        return Response(serializer.data)
    
    def put(self, request, id):
        pass

    def delete(self, request, id):
        pass
    


        
        

    