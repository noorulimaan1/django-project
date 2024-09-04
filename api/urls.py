from django.urls import path, include

from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, OrganizationViewSet, AgentViewSet, AdminViewSet, LeadViewSet

router = DefaultRouter()
router.register(r'leads', LeadViewSet)
router.register(r'users', UserViewSet)
router.register(r'organizations', OrganizationViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'admins', AdminViewSet)


app_name = 'api'

urlpatterns = [

    # API routes
    path('', include(router.urls)),


]
