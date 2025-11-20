from django.urls import path
from . import views

app_name = 'finders'

urlpatterns = [
    # --- Finder Index URL ---
    path('', views.FinderIndexView.as_view(), name='finder_index'),

    # --- Page URLs ---
    path('lawyers/', views.LawyerFinderView.as_view(), name='lawyer_finder'),
    path('police-stations/', views.StationFinderView.as_view(), name='station_finder'),
    path('cases/', views.CaseFinderView.as_view(), name='case_finder'),
    path('helplines/', views.ContactDirectoryView.as_view(), name='contact_directory'), # <-- ADD THIS

    # --- API URLs ---
    path('api/lawyers/', views.LawyerListAPI.as_view(), name='api_lawyer_list'),
    path('api/stations/', views.PoliceStationListAPI.as_view(), name='api_station_list'),
    path('api/cases/', views.LegalCaseListAPI.as_view(), name='api_case_list'),
    path('api/helplines/', views.HelplineListAPI.as_view(), name='api_helpline_list'), # <-- ADD THIS
]
