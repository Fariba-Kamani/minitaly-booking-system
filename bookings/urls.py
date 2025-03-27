from django.urls import path
from . import views

urlpatterns = [
    # You can add your booking views here
    path('', views.my_bookings, name='my_bookings'),
]