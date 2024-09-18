from rest_framework import serializers

from django.core.validators import EmailValidator
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User, Admin, Agent, Organization
from client.models import Lead, Customer
from client.constants import (
    LEAD_CATEGORY_UNCONVERTED,
    LEAD_CATEGORY_CONTACTED,
    LEAD_CATEGORY_CONVERTED,
    LEAD_CATEGORY_NEW,
)

from datetime import date


class UserTokenViewSerializer(TokenObtainPairSerializer):
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
            raise serializers.ValidationError('Invalid credentials.')

        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])

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
            'role'
        ]


class OrganizationSerializer(serializers.ModelSerializer):

    logo = serializers.ImageField(required=False)

    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'email',
            'address',
            'phone_number',
            'website',
            'logo',
        ]

    def validate_name(self, value):
        if Organization.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                'An organization with this name already exists'
            )
        return value


class AgentSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Agent
        fields = ['id', 'user', 'org', 'hire_date', 'profile_photo']

    def update(self, instance, validated_data):
        # Handle nested User update
        user_data = validated_data.pop('user', None)

        if user_data:
            # Update the related User model
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        # Update the Agent instance itself
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    def save(self, **kwargs):
        agent = super().save(**kwargs)

        if not agent.hire_date:
            agent.hire_date = date.today()
        if agent.hire_date < date(2024, 1, 1):
            raise serializers.ValidationError(
                'Hire date cannot be before January 1, 2024.'
            )

        return agent


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'profile_photo',
            'date_of_birth',
            'address',
            'phone_number',
        ]


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = ['id', 'user', 'org']


class LeadSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator()])

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

    def validate(self, data):
        lead = self.instance
        if lead:
            if lead.category == LEAD_CATEGORY_NEW:
                if data.get('category') not in [
                    LEAD_CATEGORY_CONTACTED,
                    LEAD_CATEGORY_UNCONVERTED,
                ]:
                    raise serializers.ValidationError(
                        'Lead status must transition from New to Contacted or Unconverted.'
                    )

            elif lead.category == LEAD_CATEGORY_CONTACTED:
                if data.get('category') not in [
                    LEAD_CATEGORY_CONVERTED,
                    LEAD_CATEGORY_UNCONVERTED,
                ]:
                    raise serializers.ValidationError(
                        'Lead status must transition from Contacted to Converted or Unconverted.'
                    )

            elif lead.category == LEAD_CATEGORY_CONVERTED:
                raise serializers.ValidationError(
                    'Lead status cannot be changed once it is Converted.'
                )

        return data

    def save(self, **kwargs):
        lead = super().save(**kwargs)

        if lead.age < 18 or lead.age > 45:
            raise serializers.ValidationError('Age must be between 18 and 45')
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
