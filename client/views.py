from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.core.exceptions import PermissionDenied


from accounts.models import Agent, Admin
from accounts.constants import AGENT, ADMIN

from client.forms import LeadModelForm, CustomerModelForm
from client.models import Lead
from client.mixins import LeadAccessMixin, CustomerAccessMixin

# Create your views here.


class LeadListView(LeadAccessMixin, View):
    def get(self, request, *args, **kwargs):
        leads = self.get_leads()
        paginator = Paginator(leads, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'leads': page_obj.object_list, 'page_obj': page_obj}
        return render(request, 'leads_list.html', context)


class LeadDetailView(LeadAccessMixin, View):
    def get(self, request, pk, *args, **kwargs):
        lead = self.get_lead(pk)
        context = {'lead': lead}
        return render(request, 'lead_details.html', context)


class LeadCreateView(LeadAccessMixin, View):
    def get(self, request, *args, **kwargs):
        form = LeadModelForm(request=request)
        context = {'form': form}
        return render(request, 'lead_create.html', context)

    def post(self, request, *args, **kwargs):
        form = LeadModelForm(request.POST, request=request)
        if form.is_valid():
            lead = form.save(commit=False)

            if request.user.role == ADMIN:
                admin = get_object_or_404(Admin, user=request.user)
                lead.organization = admin.org
            elif request.user.role == AGENT:
                agent = get_object_or_404(Agent, user=request.user)
                lead.organization = agent.org
                lead.agent = agent
            else:
                raise PermissionDenied(
                    'User does not have an associated organization.')

            lead.save()
            return redirect(reverse('client:lead-list'))

        context = {'form': form}
        return render(request, 'lead_create.html', context)


class LeadUpdateView(LeadAccessMixin, View):
    def get(self, request, pk, *args, **kwargs):
        lead = self.get_lead(pk)
        form = LeadModelForm(instance=lead)
        context = {'form': form, 'lead': lead}
        return render(request, 'lead_update.html', context)

    def post(self, request, pk, *args, **kwargs):
        lead = self.get_lead(pk)
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect(reverse('client:lead-list'))
        context = {'form': form, 'lead': lead}
        return render(request, 'lead_update.html', context)


class LeadDeleteView(LeadAccessMixin, View):
    def get(self, request, pk, *args, **kwargs):
        lead = self.get_lead(pk)
        context = {'lead': lead}
        return render(request, 'lead_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        lead = self.get_lead(pk)
        lead.delete()
        return redirect(reverse('client:lead-list'))


class CustomerListView(CustomerAccessMixin, View):
    def get(self, request, *args, **kwargs):
        customers = self.get_customers()
        paginator = Paginator(customers, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {'customers': page_obj.object_list, 'page_obj': page_obj}
        return render(request, 'customers_list.html', context)


class CustomerDetailView(CustomerAccessMixin, View):
    def get(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        context = {'customer': customer}
        return render(request, 'customer_details.html', context)


class CustomerCreateView(CustomerAccessMixin, View):
    def get(self, request, *args, **kwargs):
        form = CustomerModelForm(request=request)
        context = {'form': form}
        return render(request, 'customer_create.html', context)

    def post(self, request, *args, **kwargs):
        form = CustomerModelForm(request.POST, request=request)
        if form.is_valid():
            customer = form.save(commit=False)

            if request.user.role == ADMIN:
                admin = get_object_or_404(Admin, user=request.user)
                customer.org = admin.org
            elif request.user.role == AGENT:
                agent = get_object_or_404(Agent, user=request.user)
                customer.org = agent.org
                customer.agent = agent
            else:
                raise PermissionDenied(
                    'User does not have an associated organization.')

            customer.save()
            return redirect(reverse('client:customer-list'))

        context = {'form': form}
        return render(request, 'customer_create.html', context)


class CustomerUpdateView(CustomerAccessMixin, View):
    def get(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        form = CustomerModelForm(instance=customer)
        context = {'form': form, 'customer': customer}
        return render(request, 'customer_update.html', context)

    def put(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect(reverse('client:customer-list'))
        context = {'form': form, 'customer': customer}
        return render(request, 'customer_update.html', context)


class CustomerDeleteView(CustomerAccessMixin, View):
    def get(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        context = {'customer': customer}
        return render(request, 'customer_delete.html', context)

    def post(self, request, pk, *args, **kwargs):
        customer = self.get_customer(pk)
        customer.delete()
        return redirect(reverse('client:customer-list'))
