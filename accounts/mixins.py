from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404

from accounts.constants import ADMIN, AGENT
from accounts.models import Agent

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == ADMIN

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        # authenticated, not authorized
        else:
            raise PermissionDenied

class AdminOrAgentsRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role in [ADMIN, AGENT]

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect('login')
        # authenticated, not authorized
        else:
            raise PermissionDenied
        
class AdminOrAgentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        try:
            agent = Agent.objects.get(user=self.request.user)
        except Agent.DoesNotExist:
            agent = None  

        obj = self.get_object()  

        return self.request.user.role == ADMIN or (agent is not None and agent.user == obj.user)
