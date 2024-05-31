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
    
    def update(self, instance, validated_data):
        """ 
        Update and return an existing `UserProfile` instance, given the validated data. 
        """  
        instance.first_name = validated_data.get('first_name', instance.first_name)  
        instance.last_name = validated_data.get('last_name', instance.last_name)  
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance