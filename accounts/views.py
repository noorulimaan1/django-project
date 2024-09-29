from django import forms
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied
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

from accounts.mixins import AdminRequiredMixin, AdminOrAgentsRequiredMixin, AdminOrAgentRequiredMixin
from accounts.forms import CustomUserCreationForm, AgentUpdateForm
from accounts.constants import ADMIN, AGENT
from accounts.models import Agent, Admin


class SignUpView(AdminRequiredMixin, CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('home-page')


class CustomLoginView(LoginView):

    def get_success_url(self):
        user = self.request.user
        if user.role == ADMIN or AGENT:
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


class HomePageView(AdminOrAgentsRequiredMixin, TemplateView):
    template_name = 'home_page.html'


class AgentListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'agent_list.html'
    paginate_by = 5

    def get_queryset(self):
        admin = get_object_or_404(Admin, user=self.request.user)
        return Agent.objects.filter(org=admin.org).order_by('-created_at')


class AgentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'agent_create.html'
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        admin = get_object_or_404(Admin, user=self.request.user)
        kwargs['admin_org'] = admin.org
        return kwargs

    def get_success_url(self):
        return reverse('accounts:agent-list')


class AgentUpdateView(AdminOrAgentRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'agent_update.html'
    form_class = AgentUpdateForm  
    model = Agent

    def get_queryset(self):
        print(f'User role: {self.request.user.role}')  
        if self.request.user.role == ADMIN:
            admin = get_object_or_404(Admin, user=self.request.user)
            queryset = Agent.objects.filter(org=admin.org)
            print(f'Admin org queryset: {queryset}')
            return queryset
        elif self.request.user.role == AGENT:
            queryset = Agent.objects.filter(user=self.request.user)
            print(f'Agent queryset: {queryset}')
            return queryset

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user.role == AGENT and obj.user != self.request.user:
            raise PermissionDenied(
                'You do not have permission to update this profile.')
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        agent = self.get_object() 
        kwargs['instance'] = agent
        kwargs['user_instance'] = agent.user 
        return kwargs

    def get_success_url(self):
        if self.request.user.role == AGENT:
            return reverse('home-page')
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
