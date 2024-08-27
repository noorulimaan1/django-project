from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'accounts'

urlpatterns = [
    path('', AgentListView.as_view(), name='agent-list'),
    path('create/', AgentCreateView.as_view(), name='agent-create'),
    path('<int:pk>/', AgentDetailView.as_view(), name = 'agent-details'),
    path('<int:pk>/update/', AgentUpdateView.as_view(), name='agent-update'),
    path('<int:pk>/delete/', AgentDeleteView.as_view(), name='agent-delete'),
]