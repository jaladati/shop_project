from django.urls import path

from .views import DashboardView, EditProfileView


app_name = 'user_panel'

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("edit-profile", EditProfileView.as_view(), name="edit_profile")
]
