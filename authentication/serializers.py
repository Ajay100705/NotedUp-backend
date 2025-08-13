from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'role']

    def validate(self, attrs):
        if attrs['password'] !=attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        
        # Prevent self-assigning admin role
        if attrs.get('role') == 'admin':
            raise serializers.ValidationError({"role": "You cannot register directly as admin."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.get('role', 'student')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=role
        )
        return user


        
        
