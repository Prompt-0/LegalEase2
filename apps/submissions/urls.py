from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    # --- Page URLs ---
    path('fir/', views.OnlineFIRView.as_view(), name='online_fir'),
    path('report/', views.AnonymousReportView.as_view(), name='anonymous_report'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    # --- API URLs ---
    path('api/fir/', views.OnlineFIRCreateAPI.as_view(), name='api_create_fir'),
    path('api/report/', views.AnonymousReportCreateAPI.as_view(), name='api_create_report'),
    path('api/contact/', views.ContactMessageCreateAPI.as_view(), name='api_create_contact'),
]
