from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from .models import Lead
from .forms import LeadModelForm, LeadForm


# Create your views here.


class LeadListView(generic.ListView):
    template_name = "leads_list.html"
    queryset = Lead.objects.all()
    context_object_name = "client"


class LeadDetailView(generic.DetailView):
    template_name = "lead_details.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


class LeadCreateView(generic.CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("client:lead-list")


class LeadUpdateView(generic.UpdateView):
    template_name = "lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("client:lead-list")


class LeadDeleteView(generic.DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("client:lead-list")

