from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, reverse, redirect, get_object_or_404

from django.urls import reverse
from django.views import View

from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView,
)

from accounts.mixins import AdminRequiredMixin  
from accounts.forms import CustomUserCreationForm
from accounts.constants import ADMIN
from accounts.models import Agent, Admin



class SignUpView(AdminRequiredMixin, CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('home-page')


class CustomLoginView(LoginView):

    def get_success_url(self):
        user = self.request.user
        if user.role == ADMIN: 
            return reverse('home-page') 
        else:
            return reverse(
                'client:lead-list'
            )  


class CustomLogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('landing-page')


class LandingPageView(TemplateView):
    template_name = 'landing_page.html'


class HomePageView(TemplateView):
    template_name = 'home_page.html'


class AgentListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'agent_list.html'
    paginate_by = 4

    def get_queryset(self):
        admin = get_object_or_404(Admin, user=self.request.user)
        return Agent.objects.filter(org=admin.org).order_by('-created_at')


class AgentCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'agent_create.html'
    form_class = CustomUserCreationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        admin = get_object_or_404(Admin, user=self.request.user)
        kwargs['admin_org'] = admin.org
        return kwargs


    def get_success_url(self):
        return reverse('accounts:agent-list')
    


class AgentUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'agent_update.html'
    # queryset = Agent.objects.all()
    form_class = CustomUserCreationForm

    def get_queryset(self):
        admin = get_object_or_404(Admin, user=self.request.user)
        return Agent.objects.filter(org=admin.org)
    
    def get_success_url(self):
        return reverse('accounts:agent-list')


class AgentDetailView(AdminRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = 'agent_detail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        admin = get_object_or_404(Admin, user=self.request.user)
        return Agent.objects.filter(org=admin.org)


class AgentDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'agent_delete.html'

    def get_queryset(self):
        admin = get_object_or_404(Admin, user=self.request.user)
        return Agent.objects.filter(org=admin.org)
    
    def get_success_url(self):
        return reverse('accounts:agent-list')
