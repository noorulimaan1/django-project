from django.urls import path, include

from rest_framework.routers import DefaultRouter

from client.views import (
    LeadListView,
    LeadDetailView,
    LeadCreateView,
    LeadUpdateView,
    LeadDeleteView,
    CustomerListView,
    CustomerDetailView,
    CustomerCreateView,
    CustomerUpdateView,
    CustomerDeleteView,
)


app_name = 'client'

urlpatterns = [
    path('lead/', LeadListView.as_view(), name='lead-list'),
    path('lead/<int:pk>/', LeadDetailView.as_view(), name='lead-details'),
    path('lead/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('lead/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('lead/create/', LeadCreateView.as_view(), name='lead-create'),
    path('customer/', CustomerListView.as_view(), name='customer-list'),
    path('customer/<int:pk>/', CustomerDetailView.as_view(), name='customer-details'),
    path('customer/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('customer/create/', CustomerCreateView.as_view(), name='customer-create'),
]
