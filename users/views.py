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
        """
        Create a new resource.
        This method handles the creation of a UserProfile. 
        It takes in a `request` object, which contains the data to be created.
        The data is passed to the serializer using the `get_serializer` method. 
        If the serializer is valid, the data is saved and a response with the serialized data and a status code of 201 is returned.
        If the serializer is not valid, a response with the serializer errors and a status code of 400 is returned.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailsView(APIView):
    """
    The permission_classes field specifies that only authenticated users can access these methods.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """
        Retrieves a user profile by its id.Check the user in database with the given id.
        If the user is found, return the user profile data.If the user is not found, return an error message.
        used serializers for serializing the data.
        """
        try:
            user = UserProfile.objects.get(id = id)
        except:
            content = {'status':f'User with id {id} not available.'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserProfileSerializer(user, many=False)
        return Response(serializer.data)
    
    def put(self, request, id):
        """
        Updates a user profile with the given id using the provided data.
        """
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
        """
        Deletes a UserProfile instance with the given id.
        If no UserProfile instance with the given id is found in the database, an error message is returned with status code 404.
        """
        result = get_object_or_404(UserProfile, id=id)  
        result.delete()  
        return Response({})
    