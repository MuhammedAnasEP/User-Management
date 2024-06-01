from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from django.shortcuts import get_object_or_404 
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserProfileSerializer
from .pagination import UserListPagination

# Create your views here.

class UserProfileListAndCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = UserProfile.objects.get(id = id)
        except:
            content = {'status':f'User with id {id} not available.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user, many=False)
        return Response(serializer.data)
    
    def put(self, request, id):
        try:
            user = UserProfile.objects.get(id = id)
        except:
            content = {'status':f'User with id {id} not available.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user, data = request.data, partial=True)  
        if serializer.is_valid():  
            serializer.save()  
            return Response(serializer.data)  
        else:  
            return Response(serializer.errors)

    def delete(self, request, id):
        result = get_object_or_404(UserProfile, id=id)  
        result.delete()  
        return Response({})
    