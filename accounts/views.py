from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import render, reverse
from django.views import generic
from django.views.generic import TemplateView

from accounts.forms import AgentModelForm, CustomUserCreationForm
from accounts.models import Admin, Agent


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

    def get_success_url(self):
        return reverse("accounts:agent-list")
    

class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "agent_update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("accounts:agent-list")
    
    

class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'agent_detail.html'
    queryset = Agent.objects.all()
    context_object_name = 'agent'


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("accounts:agent-list")
