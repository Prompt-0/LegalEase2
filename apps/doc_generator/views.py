from django.views.generic import TemplateView
from rest_framework import generics
from .models import DocumentTemplate
from .serializers import DocumentTemplateSerializer

# --- 1. Page-Serving View (HTML) ---

class DocumentGeneratorIndexView(TemplateView):
    template_name = "doc_generator/document_generator.html"

# --- 2. API View (JSON) ---

class DocumentTemplateListAPI(generics.ListAPIView):
    """
    API endpoint for listing all available document templates.
    """
    queryset = DocumentTemplate.objects.all()
    serializer_class = DocumentTemplateSerializer
