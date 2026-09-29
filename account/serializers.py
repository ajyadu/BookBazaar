from rest_framework import serializers
from  .models import UserProfile



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'address', 'phone_number', 'profile_picture']



class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['email', 'password']