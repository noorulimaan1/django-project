from rest_framework import serializers


from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import User, Admin, Agent, Organization
from client.models import Lead, Customer
from client.constants import LEAD_CATEGORY_CONVERTED
from datetime import date


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        # Check if the username is an email
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # If not an email, fall back to using the username
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            attrs['username'] = user.username
        else:
            raise serializers.ValidationError("Invalid credentials.")

        return super().validate(attrs)
      

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'age',
            'profile_photo',
            'is_active',
            'is_staff',
            'date_of_birth',
            'address',
            'phone_number',
        ]



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'email',
            'admin',
            'address',
            'phone_number',
            'website',
            'logo',
        ]

    def validate_name(self, value):
        if Organization.objects.filter(name=value).exists():
            raise serializers.ValidationError('An organization with this name already exists')
        return value


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'user', 'org', 'hire_date']

    def save(self, **kwargs):
        agent = super().save(**kwargs) 

        if not agent.hire_date:
            agent.hire_date = date.today()
        if agent.hire_date < date(2024, 1, 1):
            raise serializers.ValidationError("Hire date cannot be before January 1, 2024.")

        return agent



class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'user', 'org']


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'id',
            'agent',
            'organization',
            'first_name',
            'last_name',
            'age',
            'email',
            'phone_number',
            'address',
            'category',
            'created_at',
        ]

    def save(self, **kwargs):
        # Save the lead
        lead = super().save(**kwargs)

        if lead.age < 18 or lead.age > 45:
            raise serializers.ValidationError('Age must be between 18 and 45')

        if lead.category == LEAD_CATEGORY_CONVERTED:
            if not Customer.objects.filter(lead=lead).exists():

                username = f'{lead.first_name.lower()}.{lead.last_name.lower()}_{get_random_string(3)}'
                
                password = get_random_string(10)
                
                user = User.objects.create(
                    first_name=lead.first_name,
                    last_name=lead.last_name,
                    username=username,
                    email=lead.email,
                    password=make_password(password), 
                    is_active=True  
                )
                
      
                Customer.objects.create(
                    user=user,
                    org=lead.organization,
                    lead=lead,
                    total_purchases=0.00,
                )
                # send_credentials_email(user.email, username, password)

        return lead

    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError('Age cannot be negative.')
        return value

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id',
            'user',
            'org',
            'lead',
            'total_purchases',
            'first_purchase_date',
            'last_purchase_date',
        ]

    def save(self, **kwargs):
        customer = super().save(**kwargs) 

        if customer.age < 18 or customer.age > 45:
            raise serializers.ValidationError('Age must be between 18 and 45')

        return customer
    
