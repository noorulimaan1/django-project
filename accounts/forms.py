from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from accounts.models import Agent, User
from accounts.constants import ROLE_CHOICES, AGENT



# class CustomUserCreationFormForAgent(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'age', 'phone_number', 'address', 'profile_photo')
#         field_classes = {'username': UsernameField}

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.role = AGENT  # Automatically set the role to AGENT
#         if commit:
#             user.save()
#         return user
    
# class AgentCreationForm(forms.ModelForm):
#     class Meta:
#         model = Agent
#         fields = ['profile_photo', 'hire_date']  # Fields specific to the Agent model

#     def __init__(self, *args, **kwargs):
#         self.admin_user = kwargs.pop('admin_user')  # Pass the admin user to get the organization
#         super().__init__(*args, **kwargs)

#     def save(self, commit=True):
#         agent = super().save(commit=False)
#         user = self.instance.user  # This assumes that User is already created by this point
#         user.role = AGENT  # Ensures that the user role is set to agent
#         agent.org = self.admin_user.admin_profile.org  # Automatically associate with the admin's organization
#         if commit:
#             user.save()
#             agent.save()
#         return agent


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    # Exclude role from form fields; it will be set programmatically
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        self.admin_org = kwargs.pop('admin_org', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = AGENT  # Automatically set the role to AGENT
        if commit:
            user.save()
            # Create the Agent object linked to this user
            if self.admin_org:
                Agent.objects.create(user=user, org=self.admin_org)
        return user

# class CustomUserCreationForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)

#     # role = forms.ChoiceField(
#     #     choices=ROLE_CHOICES,

#     # )  

#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'role')
#         field_classes = {'username': UsernameField}

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.role = AGENT
#         if commit:
#             user.save()
#         return user


# class AgentModelForm(forms.ModelForm):
#     class Meta:
#         model = Agent
#         fields = (
#             'user',
#             'org',
#         )
    
#     def save(self, commit=True):
#         agent = super().save(commit=False)
#         if commit:
#             user = agent.user
#             user.role = AGENT 
#             user.save()
#             agent.save()
#         return agent
