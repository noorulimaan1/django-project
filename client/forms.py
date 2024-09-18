from django import forms
from django.shortcuts import get_object_or_404

from accounts.models import Agent, Admin
from client.models import Lead
from client.constants import LEAD_CATEGORIES
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
                agent = get_object_or_404(Agent, user=user)
                self.fields['agent'].queryset = Agent.objects.filter(org=agent.org)



# class LeadForm(forms.Form):
#     first_name = forms.CharField(label = 'Your Name', max_length=25)
#     email = forms.EmailField()
#     age = forms.IntegerField(min_value=0)
#     phone_number = forms.CharField(max_length=15)
#     address = forms.CharField(max_length=100, required=False, widget=forms.Textarea)
#     category = forms.ChoiceField(choices=LEAD_CATEGORIES.items())
