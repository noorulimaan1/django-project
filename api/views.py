from django.shortcuts import render
from django.http import Http404

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView


from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from accounts.models import User, Organization, Agent, Admin

from api.serializers import (
    UserSerializer,
    OrganizationSerializer,
    AgentSerializer,
    AdminSerializer,
    LeadSerializer, 
    CustomerSerializer,
    LeadSerializer,
    CustomTokenObtainPairSerializer,
)



from client.models import Lead, Customer


# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer



class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer


class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

class LeadsByAgentView(generics.ListAPIView):
    serializer_class = LeadSerializer

    def get_queryset(self):
        agent_id = self.kwargs.get('agent_id')
        try:
            agent = Agent.objects.get(pk=agent_id)
        except Agent.DoesNotExist:
            raise NotFound(f"Agent with id {agent_id} does not exist.")
        
        return Lead.objects.filter(agent=agent)

class LeadsOfAgentByCategoryView(APIView):
    
    def get(self, request, agent_id, category, format=None):
        try:
            agent = Agent.objects.get(pk=agent_id)
        except Agent.DoesNotExist:
            raise NotFound(f"Agent with id {agent_id} does not exist.")
        
        leads = Lead.objects.filter(agent=agent, category=category)
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)


class AdminListView(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class LeadListView(APIView):

    def get(self, request):
        leads = Lead.objects.all()
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)
    

class LeadCreateView(APIView):

    def post(self, request):
        serializer = LeadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LeadDetailView(APIView):

    def get_object(self, pk):
        try:
            return Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        lead = self.get_object(pk)
        serializer = LeadSerializer(lead)
        return Response(serializer.data)
    
class LeadUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        lead = self.get_object(pk)
        serializer = LeadSerializer(lead, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LeadDeleteView(APIView):

    def get_object(self, pk):
        try:
            return Lead.objects.get(pk=pk)
        except Lead.DoesNotExist:
            raise Http404

    def delete(self, request, pk):
        lead = self.get_object(pk)
        lead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

