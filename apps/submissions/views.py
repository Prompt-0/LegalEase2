from django.views.generic import TemplateView
from rest_framework import generics, permissions
from .models import OnlineFIR, AnonymousReport, ContactMessage
from .serializers import (
    OnlineFIRSerializer,
    AnonymousReportSerializer,
    ContactMessageSerializer
)

# --- 1. Page-Serving Views (HTML) ---

class OnlineFIRView(TemplateView):
    template_name = "submissions/online_fir.html"

class AnonymousReportView(TemplateView):
    template_name = "submissions/anonymous_report.html"

class ContactView(TemplateView):
    template_name = "submissions/contact.html"


# --- 2. API Views (JSON) ---

class OnlineFIRCreateAPI(generics.CreateAPIView):
    """
    API endpoint to create an OnlineFIR.
    Must be logged in to use.
    """
    queryset = OnlineFIR.objects.all()
    serializer_class = OnlineFIRSerializer
    # This view is protected; only logged-in users can access it
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in user to the submission
        serializer.save(user=self.request.user)

class AnonymousReportCreateAPI(generics.CreateAPIView):
    """
    API endpoint to create an AnonymousReport.
    Can be used by anyone (logged in or not).
    """
    queryset = AnonymousReport.objects.all()
    serializer_class = AnonymousReportSerializer
    # This view is public
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        # If the user is logged in, link the report to them.
        # If not, the 'user' field will remain null.
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class ContactMessageCreateAPI(generics.CreateAPIView):
    """
    API endpoint to create a ContactMessage.
    Can be used by anyone.
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
