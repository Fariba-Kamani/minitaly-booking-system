"""
menu/views.py

Defines views for displaying the restaurant menu to users.
"""

from django.shortcuts import render
from .models import Category


def menu_view(request):
    """
    Renders the full menu grouped by category.

    Loads all categories and their related menu items efficiently in one go.
    This prevents unnecessary database lookups when displaying the full menu.

    Template: menu/menu.html
    Context:
        categories (QuerySet): All categories with their related menu items.
    """
    # Load categories and their items together to improve performance
    categories = Category.objects.prefetch_related('menu_items').all()
    return render(request, 'menu/menu.html', {'categories': categories})
