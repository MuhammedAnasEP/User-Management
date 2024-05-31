from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

    def create(self, validated_data):  
        """ 
        Create and return a new `UserProfile` instance, given the validated data. 
        """  
        return UserProfile.objects.create(**validated_data)  