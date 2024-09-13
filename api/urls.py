from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


from api.views import (
    UserViewSet,
    OrganizationViewSet,
    AgentViewSet,
    AdminListView,
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView,
    CustomerViewSet,
    LeadsByAgentView,
    LeadsOfAgentByCategoryView,
    AdminViewSet,
    LeadViewSet,
    CustomTokenObtainPairView,
    AgentUpdateView,
    Demo
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'lead', LeadViewSet)


app_name = 'api'

urlpatterns = [

    # API routes
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admins/', AdminListView.as_view(), name='admin-list'),
    path('leads/', LeadListView.as_view(), name='lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('leads/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('agents/<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('agents/<int:agent_id>/leads/', LeadsByAgentView.as_view(), name='leads-by-agent'),
    path('agents/<int:agent_id>/leads/category/<str:category>/', LeadsOfAgentByCategoryView.as_view(), name='leads-of-agent-by-category'),
    path('test/', Demo.as_view(), name='test'),
]








# Implement serialisers for all the views.
# List all the clients associated with the agent.
# Validate lead status transitions: New > Contacted > Unconverted/Converted.
# Validate email formats.
# Ensure that the agent's hire date is not before 2024.
# Allow agents to edit their profile where they can update info and upload a profile photo as well.
# Create a page which list clients(lead and customers). 
# For admin, it should display all clients and allow to update, edit or delete.
# For Agent only list the leads and customers associated with it and an Agent can only change status of lead, or update lead info and create a new lead.
