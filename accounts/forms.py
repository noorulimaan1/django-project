from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.utils.crypto import get_random_string

from accounts.models import Agent, User
from accounts.constants import ROLE_CHOICES, AGENT


class CustomUserCreationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'date_of_birth',
                  'address', 'phone_number', 'profile_photo')

    def __init__(self, *args, **kwargs):
        self.admin_org = kwargs.pop('admin_org', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        random_suffix = get_random_string(length=3)
        user.username = f'{user.first_name.lower()}{user.last_name.lower()}{
            random_suffix}'
        generated_password = get_random_string(length=8)
        user.set_password(generated_password)

        user.role = AGENT

        if commit:
            user.save()
            if self.admin_org:
                Agent.objects.create(user=user, org=self.admin_org)

        print(f'Username: {user.username}, Password: {generated_password}')

        return user


class AgentUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_photo = forms.ImageField(required=False)
    date_of_birth = forms.DateField(required=False)
    address = forms.CharField(required=False, max_length=255)
    phone_number = forms.CharField(required=False)

    class Meta:
        model = Agent
        fields = ('first_name', 'last_name', 'email', 'date_of_birth',
                  'address', 'phone_number', 'profile_photo')

    def __init__(self, *args, **kwargs):
        self.user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)

        if self.user_instance:
            self.fields['first_name'].initial = self.user_instance.first_name
            self.fields['last_name'].initial = self.user_instance.last_name
            self.fields['email'].initial = self.user_instance.email
            self.fields['date_of_birth'].initial = self.user_instance.date_of_birth
            self.fields['address'].initial = self.user_instance.address
            self.fields['phone_number'].initial = self.user_instance.phone_number
            self.fields['profile_photo'].initial = self.user_instance.profile_photo

    def save(self, commit=True):
        agent = super().save(commit=False)
        user = self.user_instance

        if user:
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
                agent.user = user
                agent.save()

        return agent
