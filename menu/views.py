from django.shortcuts import render
from .models import Category

# Create your views here.
def menu_view(request):
    # Groups menu items by category using Django’s prefetch_related
    categories = Category.objects.prefetch_related('menu_items').all()
    return render(request, 'menu/menu.html', {'categories': categories})
