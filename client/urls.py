from django.urls import path, include

from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, OrganizationViewSet, AgentViewSet, AdminViewSet
from client.views import LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, LeadViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet)



app_name = 'client'

urlpatterns = [

    # API routes
    path('api/', include(router.urls)),
    
    # Web interface routes
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/', LeadDetailView.as_view(), name = 'lead-details'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('create/', LeadCreateView.as_view() ,name='lead-create')
]
