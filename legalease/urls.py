from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # --- NEW: Include all our app's URL files ---
    path("", include("apps.core.urls")),
    path("users/", include("apps.users.urls")),
    path("finders/", include("apps.finders.urls")),
    path("submit/", include("apps.submissions.urls")),
    path("tools/", include("apps.legal_tools.urls")),
    path("generator/", include("apps.doc_generator.urls")),
]
