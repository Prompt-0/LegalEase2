from django.views.generic import TemplateView
from rest_framework import generics, filters
from .models import PoliceStation, LegalCase, Helpline
from .serializers import (
    LawyerProfileSerializer,
    PoliceStationSerializer,
    LegalCaseSerializer,
    HelplineSerializer
)
from apps.users.models import Profile

# --- 0. Finder Index Page ---
class FinderIndexView(TemplateView):
    template_name = "finders/finder_index.html"

# --- 1. Page-Serving Views (HTML) ---

class LawyerFinderView(TemplateView):
    template_name = "finders/lawyer_finder.html"

class StationFinderView(TemplateView):
    template_name = "finders/station_finder.html"

class CaseFinderView(TemplateView):
    template_name = "finders/case_finder.html"

class ContactDirectoryView(TemplateView):
    template_name = "finders/contact_directory.html"

# --- 2. API Views (JSON) ---

class LawyerListAPI(generics.ListAPIView):
    """
    API endpoint for searching lawyers.
    Supports search on: ?search=...
    """
    serializer_class = LawyerProfileSerializer
    # We only want to list users who are 'LAWYER'
    queryset = Profile.objects.filter(user_type='LAWYER')
    filter_backends = [filters.SearchFilter]
    # 'user__username' searches the related User's username
    search_fields = ['specialization', 'location', 'user__username', 'user__first_name', 'user__last_name']

class PoliceStationListAPI(generics.ListAPIView):
    """
    API endpoint for searching police stations.
    Supports search on: ?search=...
    """
    queryset = PoliceStation.objects.all()
    serializer_class = PoliceStationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'address', 'pincode', 'district']

class LegalCaseListAPI(generics.ListAPIView):
    """
    API endpoint for searching legal cases.
    Supports search on: ?search=...
    """
    queryset = LegalCase.objects.all()
    serializer_class = LegalCaseSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'summary', 'category']

class HelplineListAPI(generics.ListAPIView):
    """
    API endpoint for searching helplines.
    Supports search on: ?search=...
    """
    queryset = Helpline.objects.all()
    serializer_class = HelplineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'phone_number', 'category']
