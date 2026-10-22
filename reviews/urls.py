from django.urls import path
from . import views


urlpatterns = [
    path("add/<int:id>/", views.add_review, name="add_review"),
    path("add/app/<int:app_id>/", views.add_review_app, name="add_review_app"),
]