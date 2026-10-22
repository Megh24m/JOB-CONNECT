from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('employer-dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path("applicants/", views.applicants, name="applicants"),
    path("profile/", views.profile, name="profile"),
    path('employer/<int:employer_id>/', views.employer_detail, name='employer_detail'),
    path("settings/", views.settings_view, name="settings_view"),
    path("messages/", views.messages_view, name="messages"),
    path("messages/send/", views.send_message, name="send_message"),
]