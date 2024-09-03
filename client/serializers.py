from rest_framework import serializers
from .models import Lead, Customer
from accounts.models import User, Organization

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
