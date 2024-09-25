from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.exceptions import ValidationError

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
import json

from accounts.models import User, Organization, Agent, Admin

from api.mixins import (
    LeadOrgRestrictedMixin, 
    AgentOrgRestrictedMixin, 
    LeadsOrgRestrictedMixin, 
    OrgRestrictedMixin, 
    AdminOrgRestrictedMixin,
    AgentsOrgRestrictedMixin,
    CustomerOrgRestrictedMixin,
    SuperuserRequiredMixin
)

from api.permissions import IsAdminUser, IsAgentOrAdminUser
from api.utilities import ingest_leads
from api.serializers import (
    UserSerializer,
    OrganizationSerializer,
    AgentSerializer,
    AdminSerializer,
    LeadSerializer,
    CustomerSerializer,
    LeadSerializer,
    UserTokenViewSerializer,
)


from client.models import Lead, Customer


# Create your views here.

class LeadIngestionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]
    parser_classes = [MultiPartParser, JSONParser] 

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file', None)

        if file:
            try:
                leads_data = json.load(file)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON format in file'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            leads_data = request.data

            if isinstance(leads_data, list):
                pass
            else:
                return Response({'error': 'Invalid data format. Expected a list of leads or a file.'}, status=status.HTTP_400_BAD_REQUEST)

        results = ingest_leads(leads_data)

        response_data = {
            'ingested_leads': [],
            'errors': []
        }

        for result in results:
            if 'error' in result:
                response_data['errors'].append(result)
            else:
                response_data['ingested_leads'].append(result)

        return Response(response_data, status=status.HTTP_200_OK)
       

class UserTokenView(TokenObtainPairView):
    serializer_class = UserTokenViewSerializer


class UserViewSet(SuperuserRequiredMixin, viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = UserSerializer
    queryset = User.objects.all()


    def get_queryset(self):
        queryset = User.objects.all()
        name_query = self.request.GET.get('name', None)
        email_query = self.request.GET.get('email', None)
        role_query = self.request.GET.get('role', None)

        if name_query:
            queryset = queryset.filter(
                Q(first_name__icontains=name_query)
                | Q(last_name__icontains=name_query)
            )
        if email_query:
            queryset = queryset.filter(
                Q(email__icontains=email_query)
            )
        if role_query:
            queryset = queryset.filter(
                Q(role__icontains=role_query)
            )

        return queryset



class OrganizationViewSet(OrgRestrictedMixin, viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class AgentViewSet(AgentsOrgRestrictedMixin, viewsets.ModelViewSet):
    queryset = Agent.objects.none()  
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


    def get_queryset(self):
        return super().get_queryset() 
    
    def create(self, request, *args, **kwargs):
        # Pass the request to the serializer context
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

# for agents to update their own profile

class AgentUpdateView(AgentOrgRestrictedMixin, APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]
    
    def get(self, request, pk):
        agent = self.get_object(pk)
        serializer = AgentSerializer(agent)
        return Response(serializer.data)

    def put(self, request, pk):
        agent = self.get_object(pk)
        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class AdminViewSet(AdminOrgRestrictedMixin, viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class LeadViewSet(LeadsOrgRestrictedMixin, viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]


    def get_queryset(self):
        queryset = super().get_queryset()

        name_query = self.request.GET.get('name', None)
        email_query = self.request.GET.get('email', None)
        age_query = self.request.GET.get('age', None)
        sort_by = self.request.GET.get('sort_by', None)

        if name_query:
            queryset = queryset.filter(
                Q(first_name__icontains=name_query) | Q(last_name__icontains=name_query)
            )
        if email_query:
            queryset = queryset.filter(Q(email__icontains=email_query))
        if age_query:
            queryset = queryset.filter(Q(age=age_query))

        if sort_by in ['agent', 'address', 'age']:
            queryset = queryset.order_by(sort_by)
        elif sort_by:
            raise ValidationError(f'Invalid sorting field: {sort_by}')

        return queryset

    # def perform_create(self, serializer):
    #     serializer.save(agent=self.request.user.agent_profile)


class LeadsByAgentView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]

    serializer_class = LeadSerializer

    def get_queryset(self):
        user = self.request.user
        agent_id = self.kwargs.get('agent_id')

        try:
            agent = Agent.objects.get(pk=agent_id)
        except Agent.DoesNotExist:
            raise NotFound(f'Agent with id {agent_id} does not exist.')

        if hasattr(user, 'admin_profile'):
            if agent.org != user.admin_profile.org:
                raise PermissionDenied('You do not have permission to access this agent.')
        elif hasattr(user, 'agent_profile'):
            if agent != user.agent_profile:
                raise PermissionDenied('You do not have permission to access this agent.')

        return Lead.objects.filter(agent=agent)
 

class LeadsOfAgentByCategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, agent_id, category, format=None):
        user = request.user

        try:
            agent = Agent.objects.get(pk=agent_id)
        except Agent.DoesNotExist:
            raise NotFound(f'Agent with id {agent_id} does not exist.')

        if hasattr(user, 'admin_profile'):
            if agent.org != user.admin_profile.org:
                raise PermissionDenied('You do not have permission to access this agent.')
        elif hasattr(user, 'agent_profile'):
            if agent != user.agent_profile:
                raise PermissionDenied('You do not have permission to access this agent.')

        leads = Lead.objects.filter(agent=agent, category=category)
        serializer = LeadSerializer(leads, many=True)
        return Response(serializer.data)


class LeadCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]

    def post(self, request):
        user = request.user
        
        if hasattr(user, 'agent_profile'):
            agent = user.agent_profile
            request.data['agent'] = agent.pk
            request.data['organization'] = agent.org.pk

        elif hasattr(user, 'admin_profile'):
            admin = user.admin_profile
            agent_id = request.data.get('agent')
            if agent_id:
                agent = Agent.objects.get(pk=agent_id)
                if agent.org != admin.org:
                    return Response(
                        {'error': 'You can only assign leads to agents in your organization.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                request.data['organization'] = admin.org.pk
        
        serializer = LeadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LeadDetailView(LeadOrgRestrictedMixin, APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]
    def get(self, request, pk):
        lead = self.get_object(pk)
        serializer = LeadSerializer(lead)
        return Response(serializer.data)

class LeadUpdateView(LeadOrgRestrictedMixin, APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]

    def put(self, request, pk):
        user = request.user
        data = request.data.copy()  # Create a mutable copy of request.data

        # If the user is an agent, automatically set the agent and organization
        if hasattr(user, 'agent_profile'):
            agent = user.agent_profile
            data['agent'] = agent.pk
            data['organization'] = agent.org.pk

        # If the user is an admin, ensure they can assign only to agents from their organization
        elif hasattr(user, 'admin_profile'):
            admin = user.admin_profile
            # Verify that the agent belongs to the same organization
            agent_id = data.get('agent')
            if agent_id:
                agent = Agent.objects.get(pk=agent_id)
                if agent.org != admin.org:
                    return Response(
                        {'error': 'You can only assign leads to agents in your organization.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                data['organization'] = admin.org.pk

        lead = get_object_or_404(Lead, pk=pk)
        serializer = LeadSerializer(lead, data=data, context={'request': request})  # Pass context with request
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeadDeleteView(LeadOrgRestrictedMixin, APIView):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]
    def delete(self, request, pk):
        lead = self.get_object(pk)
        lead.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CustomerViewSet(CustomerOrgRestrictedMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
