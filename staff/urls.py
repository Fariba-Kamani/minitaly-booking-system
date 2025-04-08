from django.urls import path
from .views import (
    BookingDashboardView,
    StaffBookingUpdateView,
    StaffBookingDeleteView,
    StaffBookingCreateView
)

urlpatterns = [
    path('dashboard/', BookingDashboardView.as_view(), name='staff_dashboard'),
    path('edit/<int:pk>/', StaffBookingUpdateView.as_view(), name='staff_booking_edit'),
    path('delete/<int:pk>/', StaffBookingDeleteView.as_view(), name='staff_booking_delete'),
    path('create/', StaffBookingCreateView.as_view(), name='staff_booking_create'),
]