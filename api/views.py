from django.db.models import Q
from django.shortcuts import render
from django.http import Http404

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser

from api.permissions import IsAdminUser, IsAgentOrAdminUser
from api.tasks import test

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
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    queryset = User.objects.all()
    serializer_class = UserSerializer


    def get_queryset(self):
        queryset = User.objects.all()
        name_query = self.request.GET.get("name", None)
        email_query = self.request.GET.get("email", None)

        if name_query:
            queryset = queryset.filter(
                Q(first_name__icontains=name_query)
                | Q(last_name__icontains=name_query)
            )
        if email_query:
            queryset = queryset.filter(
                Q(email__icontains=email_query)
            )

        return queryset

    def get(self, request):
        users = self.get_queryset()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

class AgentUpdateView(APIView):

    def get_object(self, pk):
        try:
            return Agent.objects.get(pk=pk)
        except Agent.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        agent = self.get_object(pk)
        # Check if the logged-in user is trying to update their own profile
        if request.user.agent_profile.pk != agent.pk:
            raise PermissionDenied("You cannot update another agent's profile.")

        serializer = AgentSerializer(agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminViewSet(viewsets.ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAgentOrAdminUser]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, "admin_profile"):
            return Lead.objects.filter(organization=user.admin_profile.org)
        elif hasattr(user, "agent_profile"):
            return Lead.objects.filter(agent=user.agent_profile)
        return Lead.objects.none()

    def perform_create(self, serializer):
        serializer.save(agent=self.request.user.agent_profile)


class LeadsByAgentView(generics.ListAPIView):
    serializer_class = LeadSerializer

    def get_queryset(self):
        agent_id = self.kwargs.get("agent_id")
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

    def get_queryset(self):
        queryset = Lead.objects.all()
        name_query = self.request.GET.get("name", None)
        email_query = self.request.GET.get("email", None)
        age_query = self.request.GET.get("age", None)
        if name_query:
            queryset = queryset.filter(
                Q(first_name__icontains=name_query)
                | Q(last_name__icontains=name_query)
            )
        if email_query:
            queryset = queryset.filter(
                Q(email__icontains=email_query)
            )
        if age_query:
            queryset = queryset.filter(
                Q(age=age_query)
            )

        sort_by = self.request.GET.get("sort_by", None)
        if sort_by in ['agent', 'address', 'age']:
            queryset = queryset.order_by(sort_by)
        elif sort_by:
            # Handle invalid sort_by values
            raise ValidationError(f"Invalid sorting field: {sort_by}")

        return queryset

    def get(self, request):
        # leads = Lead.objects.all()
        leads = self.get_queryset()
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


class Demo(APIView):
    permission_classes = []
    def get(self, request):
        test.delay()
        return Response({'details' : 'true'}, status=status.HTTP_204_NO_CONTENT)





