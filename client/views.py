from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from .models import Lead
from accounts.models import Admin, Agent
from .forms import LeadModelForm, LeadForm


# Create your views here.


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

# class LeadListView(LoginRequiredMixin, generic.ListView):
#     template_name = "leads_list.html"
    
#     def get_queryset(self):
#         user = self.request.user
#         if user.admin_profile.exists():
#             org = user.admin_profile.org
#             return Lead.objects.filter(organization=org)
#         elif user.agent_profile.exists():
#             return Lead.objects.filter(agent=user.agent_profile)
#         return Lead.objects.none()


class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "lead_details.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


# class LeadCreateView(LoginRequiredMixin, generic.CreateView):
#     template_name = "lead_create.html"
#     form_class = LeadModelForm

#     def get_success_url(self):
#         return reverse("client:lead-list")


class LeadCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("client:lead-list")
    
    # def form_valid(self, form):
    #     user = self.request.user
    #     if user.admin_profile.exists():
    #         form.instance.organization = user.admin_profile.org
    #     elif user.agent_profile.exists():
    #         form.instance.agent = user.agent_profile
    #     return super().form_valid(form)


class LeadUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("client:lead-list")


class LeadDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("client:lead-list")

