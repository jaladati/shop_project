from django.urls import path

from .views import DashboardView


app_name = 'user_panel'

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard")
]
