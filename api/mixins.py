from rest_framework.exceptions import PermissionDenied
from django.http import Http404

from accounts.models import Agent, Admin, Organization

from client.models import Lead, Customer



class LeadsOrgRestrictedMixin:
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin_profile'):
            return Lead.objects.filter(organization=user.admin_profile.org)
        elif hasattr(user, 'agent_profile'):
            return Lead.objects.filter(agent=user.agent_profile)
        return Lead.objects.none()
    
class LeadOrgRestrictedMixin:
    def get_object(self, pk):
        user = self.request.user
        try:
            lead = Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            raise Http404

        if hasattr(user, 'admin_profile'):
            if lead.organization != user.admin_profile.org:
                raise PermissionDenied('You do not have permission to access this lead.')
        elif hasattr(user, 'agent_profile'):
            if lead.agent != user.agent_profile:
                raise PermissionDenied('You do not have permission to access this lead.')

        return lead


class AgentsOrgRestrictedMixin:
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin_profile'):
            return Agent.objects.filter(org=user.admin_profile.org)

        return Agent.objects.none()
    
class AgentOrgRestrictedMixin:
    def get_object(self, pk):
        user = self.request.user
        try:
            agent = Agent.objects.get(pk=pk)
        except Agent.DoesNotExist:
            raise Http404

        if hasattr(user, 'admin_profile'):
            if agent.org != user.admin_profile.org:
                raise PermissionDenied('You do not have permission to access this agent.')
        elif hasattr(user, 'agent_profile'):
            if agent.pk != user.agent_profile.pk:
                raise PermissionDenied('You do not have permission to access this agent.')

        return agent
    
    
class OrgRestrictedMixin:
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin_profile'):
            return Organization.objects.filter(name=user.admin_profile.org)

        return Organization.objects.none()
    
class AdminOrgRestrictedMixin:
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin_profile'):
            return Admin.objects.filter(org=user.admin_profile.org)

        return Admin.objects.none()
    
class CustomerOrgRestrictedMixin:
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'admin_profile'):
            return Customer.objects.filter(org=user.admin_profile.org)
        elif hasattr(user, 'agent_profile'):
            return Customer.objects.filter(lead__agent=user.agent_profile)
    
        return Customer.objects.none()


class SuperuserRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("You do not have permission to access this resource.")
        return super().dispatch(request, *args, **kwargs)
