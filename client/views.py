from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View

from client.forms import LeadForm, LeadModelForm
from client.models import Lead
from client.models import Lead 


 


# Create your views here.

class LeadListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        leads = Lead.objects.all().order_by('-name') 
        paginator = Paginator(leads, 10) 

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'leads': page_obj.object_list,
            'page_obj': page_obj
        }
        return render(request, 'leads_list.html', context)


class LeadDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=pk)
        context = {
            'lead': lead
        }
        return render(request, 'lead_details.html', context)



class LeadCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = LeadModelForm()
        context = {
            'form': form
        }
        return render(request, 'lead_create.html', context)
    
    def post(self, request, *args, **kwargs):
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('client:lead-list'))
        context = {
            'form': form
        }
        return render(request, 'lead_create.html', context)


class LeadUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadModelForm(instance=lead)
        context = {
            'form': form,
            'lead': lead
        }
        return render(request, 'lead_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=pk)
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect(reverse('client:lead-list'))
        context = {
            'form': form,
            'lead': lead
        }
        return render(request, 'lead_update.html', context)


class LeadDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=pk)
        context = {
            'lead': lead
        }
        return render(request, 'lead_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        lead = get_object_or_404(Lead, pk=pk)
        lead.delete()
        return redirect(reverse('client:lead-list'))



