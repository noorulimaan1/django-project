from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import (
    UserViewSet,
    OrganizationViewSet,
    AgentViewSet,
    AdminListView,
    LeadListView,
    LeadCreateView,
    LeadDetailView,
    LeadUpdateView,
    LeadDeleteView
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)


app_name = 'api'

urlpatterns = [

    # API routes
    path('', include(router.urls)),
    path('admins/', AdminListView.as_view(), name='admin-list'),
    path('leads/', LeadListView.as_view(), name='lead-list'),
    path('leads/create/', LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('leads/<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('leads/<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),

]
