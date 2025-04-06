from django.urls import path
from .views import BookingDashboardView

urlpatterns = [
    path('dashboard/', BookingDashboardView.as_view(), name='staff_dashboard'),
]