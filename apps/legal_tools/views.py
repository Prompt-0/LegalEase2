from django.views.generic import TemplateView
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LegalAct
from .serializers import LegalActSerializer

# --- 1. Page-Serving Views (HTML) ---

class LegalToolsIndexView(TemplateView):
    template_name = "legal_tools/legal_tools_index.html"

class LegalBotView(TemplateView):
    template_name = "legal_tools/legalbot.html"

class LegalBooksView(TemplateView):
    template_name = "legal_tools/legal_books.html"


# --- 2. API Views (JSON) ---

class LegalActListAPI(generics.ListAPIView):
    """
    API endpoint for listing all legal acts with their
    nested chapters and sections.
    """
    queryset = LegalAct.objects.all()
    serializer_class = LegalActSerializer
    # We don't need search here, the JS will handle it

class LegalBotQueryAPI(APIView):
    """
    API endpoint for the simple, rule-based LegalBot.
    """
    def post(self, request, *args, **kwargs):
        query = request.data.get("query", "").lower().strip()

        if not query:
            return Response(
                {"answer": "I'm sorry, I didn't get that. Please ask a question."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Rule-based responses
        if any(greeting in query for greeting in ["hello", "hi", "hey"]):
            answer = "Hello! I am LegalEase Bot. How can I help you with your legal query today?"
        elif "fir" in query:
            answer = "A First Information Report (FIR) is a document prepared by police... You can file one using our 'Online FIR' tool."
        elif "theft" in query:
            answer = "Theft is covered under Section 378 of the Indian Penal Code (IPC)."
        elif "assault" in query:
            answer = "Assault is defined under Section 351 of the IPC."
        else:
            answer = "I'm sorry, I don't have specific information on that topic right now. Please try asking about 'FIR', 'theft', or 'assault'."

        return Response({"answer": answer}, status=status.HTTP_200_OK)
