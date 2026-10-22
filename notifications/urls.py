from django.urls import path
from . import views


urlpatterns = [
    path("", views.notifications, name="notifications"),
    path("read/<int:id>/", views.mark_as_read, name="mark_as_read"),
]