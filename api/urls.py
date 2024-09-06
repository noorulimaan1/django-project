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
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'customer', CustomerViewSet)


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
    path('agents/<int:agent_id>/leads/', LeadsByAgentView.as_view(), name='leads-by-agent'),
    path('agents/<int:agent_id>/leads/category/<str:category>/', LeadsOfAgentByCategoryView.as_view(), name='leads-of-agent-by-category'),
]
