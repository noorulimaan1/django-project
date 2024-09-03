from django.urls import path, include
from django.contrib.auth.views import LoginView
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, OrganizationViewSet, AgentViewSet, AdminViewSet

from accounts.views import (
    AgentListView,
    AgentCreateView,
    AgentDetailView,
    AgentUpdateView,
    AgentDeleteView,
    SignUpView,
    CustomLoginView,
    CustomLogoutView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'admins', AdminViewSet)

app_name = 'accounts'

urlpatterns = [

    # API routes
    path('api/', include(router.urls)),
    
    # Web interface routes
    path('', AgentListView.as_view(), name='agent-list'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('<int:pk>/', AgentDetailView.as_view(), name='agent-details'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
