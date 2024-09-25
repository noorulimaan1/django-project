from django import forms
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from accounts.models import Agent, Admin, User
from client.models import Lead, Customer
from client.constants import LEAD_CATEGORIES, LEAD_CATEGORY_CONVERTED
from accounts.constants import ADMIN, AGENT

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            'agent',
            'first_name',
            'last_name',
            'age',
            'email',
            'phone_number',
            'address',
            'category'
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            if user.role == ADMIN:
                admin = get_object_or_404(Admin, user=user)
                self.fields['agent'].queryset = Agent.objects.filter(org=admin.org)
            elif user.role == AGENT:

                self.fields.pop('agent', None)  

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and (age < 18 or age > 45):
            raise forms.ValidationError("Age must be between 18 and 45.")
        return age
    
    def clean_category(self):
        category = self.cleaned_data.get('category')
        # Check if the form is being created for the first time (not an existing instance)
        if self.instance.pk is None:  # If there's no primary key, it's a new instance
            if category == LEAD_CATEGORY_CONVERTED:
                raise forms.ValidationError("A new lead cannot be marked as Converted.")
        return category



class CustomerModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    # Agentdob
    # address
    # phone_number

    class Meta:
        model = Customer
        fields = [
            'total_purchases',
            'first_purchase_date',
            'last_purchase_date',
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            user = self.request.user
            if user.role == ADMIN:
                self.org = user.admin_profile.org
            elif user.role == AGENT:
                self.org = user.agent_profile.org

    def save(self, commit=True):
        # Create a new user first
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        email = self.cleaned_data.get('email')

        random_string = get_random_string(length=3)  
        username = f"{first_name.lower()}.{last_name.lower()}.{random_string}"
        password = get_random_string(length=12)  
        
        print(f"Generated Username: {username}")
        print(f"Generated Password: {password}")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        customer = super().save(commit=False)
        customer.user = user
        customer.org = self.org  

        if commit:
            customer.save()

        return customer

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data



