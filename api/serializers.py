from rest_framework import serializers
from accounts.models import User, Organization, Agent, Admin
from client.models import Lead, Customer


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

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id', 'agent', 'organization', 'name', 'age', 'email', 
            'phone_number', 'address', 'category', 'created_at'
        ]
        # read_only_fields = ['created_at', 'updated_at']

    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative.")
        return value

