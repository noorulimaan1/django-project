from rest_framework import serializers
from .models import User, Organization, Agent, Admin

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'age', 'profile_photo', 'is_active', 'is_staff', 'date_of_birth', 'address', 'phone_number']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'email', 'admin', 'address', 'phone_number', 'website', 'logo']

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'org', 'hire_date']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'user', 'org']
