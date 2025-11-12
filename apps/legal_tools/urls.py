from django.urls import path
from . import views

app_name = 'legal_tools'

urlpatterns = [
    # --- Page URLs ---
    path('', views.LegalToolsIndexView.as_view(), name='tools_index'),
    path('bot/', views.LegalBotView.as_view(), name='legalbot'),
    path('books/', views.LegalBooksView.as_view(), name='legal_books'),

    # --- API URLs ---
    path('api/acts/', views.LegalActListAPI.as_view(), name='api_legal_acts'),
    path('api/bot-query/', views.LegalBotQueryAPI.as_view(), name='api_bot_query'),
]
