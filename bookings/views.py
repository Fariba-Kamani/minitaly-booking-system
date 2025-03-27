from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_bookings(request):
   return HttpResponse("Welcome to Minitaly booking system!")
