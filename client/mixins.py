from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from client.models import Lead
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
                return Lead.objects.filter(organization=agent.org)
            except Agent.DoesNotExist:
                raise PermissionDenied('Agent profile does not exist for the current user.')
        else:
            raise PermissionDenied('User role is not authorized to access leads.')

    def get_lead(self, pk):
        leads = self.get_leads()
        return get_object_or_404(leads, pk=pk)

