from django.shortcuts import render
from .models import Lead

# Create your views here.
def leads_list(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request,"leads_list.html", context)
