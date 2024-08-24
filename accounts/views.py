from django.shortcuts import render, reverse
from django.views.generic import TemplateView
from django.views import generic
from django.http import HttpResponse

from .forms import CustomUserCreationForm


# Create your views here.

class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(TemplateView):
    template_name = "landing_page.html"

def landing_page(request):
    return render(request, "home_view.html")
