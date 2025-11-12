from django.urls import path
from . import views

app_name = 'doc_generator'

urlpatterns = [
    # --- Page URL ---
    path('', views.DocumentGeneratorIndexView.as_view(), name='doc_index'),

    # --- API URL ---
    path('api/templates/', views.DocumentTemplateListAPI.as_view(), name='api_template_list'),
]
