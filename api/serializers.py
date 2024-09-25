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

        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
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
            'email',
            'age',
            'profile_photo',
            'is_active',
            'date_of_birth',
            'address',
            'phone_number',
        ]

    def create(self, validated_data):
        user_role = self.context.get('role')  # Pass role through context
        
        if user_role == 'customer':
            # Generate username and password for customer
            first_name = validated_data['first_name']
            last_name = validated_data['last_name']
            base_username = f"{first_name.lower()}.{last_name.lower()}"
            username = self.generate_unique_username(base_username)
            password = get_random_string(10)
            validated_data['username'] = username
            user = User.objects.create(**validated_data)
            user.set_password(password)
        else:
            # Use default behavior for other user roles
            user = User.objects.create(**validated_data)
        
        user.save()
        return user


    def generate_unique_username(self, base_username):
        # Logic to ensure unique username
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        return username


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
        fields = ['id', 'user', 'hire_date']

    def create(self, validated_data):
        # Get the request object from the context
        request = self.context.get('request')
        user = request.user
        admin_profile = user.admin_profile

        # Automatically set org and role for the agent
        org = admin_profile.org
        role = 2

        # Extract first and last name from validated data
        user_data = validated_data.pop('user')
        first_name = user_data.get('first_name', '')
        last_name = user_data.get('last_name', '')

        # Generate username using first and last name
        base_username = f"{first_name.lower()}.{last_name.lower()}"
        username = self.generate_unique_username(base_username)

        # Generate random password
        password = get_random_string(10)

        print(f"Generated password for {username}: {password}")
        # Create user for the agent
        user_data = {
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': user_data.get('email', ''),
            'role': role
        }
        new_user = User.objects.create(**user_data)
        new_user.set_password(password)
        new_user.save()

        # Create the agent with the new user and organization
        agent = Agent.objects.create(user=new_user, org=org, hire_date=validated_data.get('hire_date'))

        # Optionally send the credentials via email to the agent
        # send_email_to_agent(new_user.email, username, password)

        return agent

    def generate_unique_username(self, base_username):
        """
        Helper method to generate a unique username by appending a number
        if the base username already exists.
        """
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        return username
    
    def validate_user(self, user_data):
        age = user_data.get('age')
        if age and (age < 18 or age > 45):
            raise serializers.ValidationError("Age must be between 18 and 45.")
        return user_data


  

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and hasattr(request.user, 'agent_profile'):
            self.fields.pop('agent', None)
            self.fields.pop('organization', None)

        elif request and hasattr(request.user, 'admin_profile'):
            self.fields.pop('organization', None)
            self.fields['agent'].queryset = Agent.objects.filter(org=request.user.admin_profile.org)

    def validate(self, data):
        lead = self.instance  # Get the current lead instance

        if lead:  # Only perform checks if we're updating an existing lead
            new_category = data.get('category', lead.category)  # Get the new category or default to the current one

            if lead.category != new_category:  # Check if the category is changing
                if lead.category == LEAD_CATEGORY_NEW and new_category not in [
                    LEAD_CATEGORY_CONTACTED,
                    LEAD_CATEGORY_UNCONVERTED,
                ]:
                    raise serializers.ValidationError(
                        'Lead status must transition from New to Contacted or Unconverted.'
                    )

                if lead.category == LEAD_CATEGORY_CONTACTED and new_category not in [
                    LEAD_CATEGORY_CONVERTED,
                    LEAD_CATEGORY_UNCONVERTED,
                ]:
                    raise serializers.ValidationError(
                        'Lead status must transition from Contacted to Converted or Unconverted.'
                    )

                if lead.category == LEAD_CATEGORY_CONVERTED:
                    raise serializers.ValidationError('Lead status cannot be changed once it is Converted.')

        return data

    def save(self, **kwargs):
        request = self.context['request']
        lead = self.instance

        # Automatically set agent and organization if creating a new lead
        if lead is None:
            if hasattr(request.user, 'agent_profile'):
                # If the user is an agent, auto-assign agent and organization
                agent = request.user.agent_profile
                organization = agent.org
                self.validated_data['agent'] = agent
                self.validated_data['organization'] = organization

            elif hasattr(request.user, 'admin_profile'):
                # If the user is an admin, allow the agent to be explicitly set
                organization = request.user.admin_profile.org
                self.validated_data['organization'] = organization

                if 'agent' not in self.validated_data:
                    raise serializers.ValidationError("Admin must assign an agent to the lead.")

        return super().save(**kwargs)




    def validate_category(self, value):

        if self.instance is None and value == LEAD_CATEGORY_CONVERTED:
            raise serializers.ValidationError("A new lead cannot be marked as 'Converted'.")
        return value

    def validate_age(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('Age cannot be negative.')
        elif value is not None and (value < 18 or value > 45):
            raise serializers.ValidationError('Age must be between 18 and 45')
        return value

    def validate_email(self, value):

        # Check if the instance exists (update case)
        if self.instance:
            if Lead.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A lead with this email already exists.")
        else:
            if Lead.objects.filter(email=value).exists():
                raise serializers.ValidationError("A lead with this email already exists.")

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
    

    

# class CustomerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()  # Nested serializer to handle user creation

#     class Meta:
#         model = Customer
#         fields = ['user', 'org', 'lead', 'total_purchases', 'first_purchase_date', 'last_purchase_date', 'agent']

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     current_user = request.user
        
    #     # User data is nested, pop it from validated_data to handle separately
    #     user_data = validated_data.pop('user')
    #     # Create the User instance
    #     user = User.objects.create(**user_data)
        
    #     # If the current user is an admin, allow them to assign an agent
    #     if hasattr(current_user, 'admin_profile'):
    #         org = current_user.admin_profile.org
    #         validated_data['org'] = org
    #         agent = validated_data.get('agent')
    #         if agent and agent.org != org:
    #             raise serializers.ValidationError("You can only assign agents from your own organization.")
        
    #     # If the current user is an agent, set the agent field to the current user and their organization
    #     elif hasattr(current_user, 'agent_profile'):
    #         agent = current_user.agent_profile
    #         validated_data['agent'] = agent
    #         validated_data['org'] = agent.org
        
    #     # Create the Customer object with the validated data
    #     customer = Customer.objects.create(user=user, **validated_data)
    #     return customer


# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = [
#             'id',
#             'user',
#             'org',
#             'lead',
#             'total_purchases',
#             'first_purchase_date',
#             'last_purchase_date',
#         ]

#     def save(self, **kwargs):
#         customer = super().save(**kwargs)

#         if customer.age < 18 or customer.age > 45:
#             raise serializers.ValidationError('Age must be between 18 and 45')
            
#         return customer

