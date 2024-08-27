from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, reverse
from django.views.generic import TemplateView
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, AgentModelForm
from .models import Agent, Admin


# Create your views here.

class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing_page.html"

class landing_page(TemplateView):
    template_name = "home_view.html"

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = 'agent_list.html'

    def get_queryset(self):
        return Agent.objects.all()
    
class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agent_create.html"
    form_class = AgentModelForm

    def form_valid(self, form):
        agent = form.save(commit=False)
        admin = Admin.objects.get(user=self.request.user)
        agent.org = self.request.user.org  # Automatically assign the organization
        agent.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("account:agent-list")

