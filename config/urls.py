from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    path("jobs/", include("jobs.urls")),

    path("applications/", include("applications.urls")),

    path("reviews/", include("reviews.urls")),

    path("notifications/", include("notifications.urls")),
]