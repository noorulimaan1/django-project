from django.urls import path

from client.views import LeadCreateView, LeadDeleteView, LeadDetailView, LeadListView, LeadUpdateView

app_name = "client"

urlpatterns = [
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name = 'lead-details'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view() ,name='lead-create')
]
