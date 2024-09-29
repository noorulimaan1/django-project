from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


from api.views import (
    UserViewSet,
    OrganizationViewSet,
    AgentViewSet,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView,
    CustomerViewSet,
    LeadsByAgentView,
    LeadsOfAgentByCategoryView,
    AdminViewSet,
    LeadViewSet,
    UserTokenView,
    AgentUpdateView,
    LeadIngestionView,
    TopOrganizationByCustomersView,
    AverageLeadsPerAgentView,
    AgentsCountPerOrgView,
    CustomersConvertedByAgentLastWeekView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'leads', LeadViewSet)
router.register(r'admins', AdminViewSet)


app_name = 'api'

urlpatterns = [
    
    path('token/', UserTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('leads/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('agents/<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path(
        'agents/<int:agent_id>/leads/',
        LeadsByAgentView.as_view(),
        name='leads-by-agent',
    ),
    path(
        'agents/<int:agent_id>/leads/category/<str:category>/',
        LeadsOfAgentByCategoryView.as_view(),
        name='leads-of-agent-by-category',
    ),
    path('organizations/higest-customers/', TopOrganizationByCustomersView.as_view(), name='org-by-highest-customers'),
    path('organizations/average-leads-per-agent/', AverageLeadsPerAgentView.as_view(), name='avg-leads-per-agent'),
    path('organizations/agent-count/', AgentsCountPerOrgView.as_view(), name='agent-count-per-org'),
    path('agents/<str:agent_name>/customers-converted-last-week/', CustomersConvertedByAgentLastWeekView.as_view(), name='leads-converted-per-agents'),
    path('leads/ingest/', LeadIngestionView.as_view(), name='lead-ingestion'),
    path('', include(router.urls)),
]


