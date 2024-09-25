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
        agent = get_object_or_404(Agent, user=self.request.user)
        return self.request.user.role == ADMIN or agent == self.get_object()


# class RoleRequiredMixin(UserPassesTestMixin):
#     required_role = None

#     def test_func(self):
#         user_role = self.request.user.role
#         return user_role and user_role.name == self.required_role

#     def handle_no_permission(self):
#         if not self.request.user.is_authenticated:
#             return redirect('login')
#         else:
#             raise PermissionDenied

# class AdminRequiredMixin(RoleRequiredMixin):
#     required_role = 'Admin'

#     def dispatch(self, request, *args, **kwargs):
#         # Check if user is staff as well
#         if not request.user.is_staff:
#             raise PermissionDenied
#         return super().dispatch(request, *args, **kwargs)
    


