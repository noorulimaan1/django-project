from django import forms
from .models import Lead
from .constants import LEAD_CATEGORIES

class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = {
            'agent',
            'organization',
            'name',
            'age',
            'email',
            'phone_number',
            'address',
            'category'

        }

class LeadForm(forms.Form):
    name = forms.CharField(label = "Your Name", max_length=25)
    email = forms.EmailField()
    age = forms.IntegerField(min_value=0)
    phone_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=100, required=False, widget=forms.Textarea)
    category = forms.ChoiceField(choices=LEAD_CATEGORIES.items())