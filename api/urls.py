from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views import (
    UserViewSet,
    OrganizationViewSet,
    AgentViewSet,
    AdminViewSet,
    LeadViewSet,
    CustomTokenObtainPairView,
)



router = DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'admins', AdminViewSet)


app_name = "api"

urlpatterns = [
    # API routes
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
