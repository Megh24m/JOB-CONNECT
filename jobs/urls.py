from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.job_list,
        name="job_list"
    ),


    path(
        "create/",
        views.create_job,
        name="create_job"
    ),


    path(
        "<int:id>/",
        views.job_detail,
        name="job_detail"
    ),


    path(
        "save/<int:id>/",
        views.save_job,
        name="save_job"
    ),


    path(
        "saved/",
        views.saved_jobs,
        name="saved_jobs"
    ),

    path(
        "recent/",
        views.recently_viewed,
        name="recently_viewed"
    ),

    path(
        "suggestions/",
        views.search_suggestions,
        name="suggestions"
    ),

]