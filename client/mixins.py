from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from client.models import Lead, Customer
from accounts.models import Admin, Agent
from django.core.exceptions import PermissionDenied
from accounts.constants import AGENT, ADMIN


class LeadAccessMixin(LoginRequiredMixin):
    def get_leads(self):
        user = self.request.user
        if user.role == ADMIN:
            try:
                admin = Admin.objects.get(user=user)
                return Lead.objects.filter(organization=admin.org)
            except Admin.DoesNotExist:
                raise PermissionDenied('Admin profile does not exist for the current user.')
        elif user.role == AGENT:
            try:
                agent = Agent.objects.get(user=user)
                return Lead.objects.filter(organization=agent.org, agent=agent)
            except Agent.DoesNotExist:
                raise PermissionDenied('Agent profile does not exist for the current user.')
        else:
            raise PermissionDenied('User role is not authorized to access leads.')

    def get_lead(self, pk):
        leads = self.get_leads()
        try:
            lead = leads.get(pk=pk) 
        except Lead.DoesNotExist:
            raise PermissionDenied('You do not have permission to view this lead.')
        return lead


class CustomerAccessMixin(LoginRequiredMixin):
    def get_customers(self):
        user = self.request.user
        if user.role == ADMIN:
            try:
                admin = Admin.objects.get(user=user)
                return Customer.objects.filter(org=admin.org)
            except Admin.DoesNotExist:
                raise PermissionDenied('Admin profile does not exist for the current user.')
        elif user.role == AGENT:
            try:
                agent = Agent.objects.get(user=user)
                return Customer.objects.filter(org=agent.org,  lead__agent=agent)
            except Agent.DoesNotExist:
                raise PermissionDenied('Agent profile does not exist for the current user.')
        else:
            raise PermissionDenied('User role is not authorized to access customers.')

    def get_customer(self, pk):
        customers = self.get_customers()
        return get_object_or_404(customers, pk=pk)
