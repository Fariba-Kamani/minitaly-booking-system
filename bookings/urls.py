from django.urls import path
from .views import (
    BookingListView,
    BookingCreateView,
    BookingUpdateView,
    BookingDeleteView,
    available_slots_api,
)

urlpatterns = [
    # You can add your booking views here
    path('', BookingListView.as_view(), name='booking_list'),
    path('api/available-slots/', available_slots_api,
         name='available_slots_api'),
    path('book/', BookingCreateView.as_view(), name='booking_create'),
    path('edit/<int:pk>/', BookingUpdateView.as_view(), name='booking_edit'),
    path('delete/<int:pk>/', BookingDeleteView.as_view(),
         name='booking_delete'),
]
