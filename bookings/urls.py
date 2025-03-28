from django.urls import path
from .views import BookingListView

urlpatterns = [
    # You can add your booking views here
    path('', BookingListView.as_view(), name='booking_list'),
]