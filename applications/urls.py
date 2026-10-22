from django.urls import path
from . import views


urlpatterns = [
    path("apply/<int:id>/", views.apply_job, name="apply_job"),
    path("", views.my_applications, name="my_applications"),
    path("update/<int:id>/<str:status>/", views.update_application_status, name="update_status"),
    path("respond/<int:id>/<str:response>/", views.respond_to_offer, name="respond_to_offer"),
]