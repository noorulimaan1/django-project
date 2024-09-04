from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import render, reverse, redirect
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

from accounts.mixins import AdminRequiredMixin  # Import the custom mixin
from accounts.forms import CustomUserCreationForm, AgentModelForm
from accounts.models import Agent


class SignUpView(AdminRequiredMixin, CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        # return reverse('accounts:login')
        return reverse("home-page")


class CustomLoginView(LoginView):

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:  # Assuming superusers are your admins
            return reverse("home-page")  # Redirect to the admin home page
        else:
            return reverse(
                "client:lead-list"
            )  # Redirect to the default lead list page for agents


class CustomLogoutView(View):
    # def get(self, request, *args, **kwargs):
    #     logout(request)
    #     return redirect('landing-page')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect("landing-page")


class LandingPageView(TemplateView):
    template_name = "landing_page.html"


class HomePageView(TemplateView):
    template_name = "home_page.html"


class landing_page(TemplateView):
    template_name = "home_view.html"


class AgentListView(AdminRequiredMixin, LoginRequiredMixin, ListView):
    template_name = "agent_list.html"
    paginate_by = 4

    def get_queryset(self):
        return Agent.objects.all().order_by("-created_at")


class AgentCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = "agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("accounts:agent-list")


class AgentUpdateView(AdminRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = "agent_update.html"
    queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("accounts:agent-list")


class AgentDetailView(AdminRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = "agent_detail.html"
    queryset = Agent.objects.all()
    context_object_name = "agent"


class AgentDeleteView(AdminRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = "agent_delete.html"
    queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("accounts:agent-list")


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class OrganizationViewSet(viewsets.ModelViewSet):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer


# class AgentViewSet(viewsets.ModelViewSet):
#     queryset = Agent.objects.all()
#     serializer_class = AgentSerializer


# class AdminViewSet(viewsets.ModelViewSet):
#     queryset = Admin.objects.all()
#     serializer_class = AdminSerializer
