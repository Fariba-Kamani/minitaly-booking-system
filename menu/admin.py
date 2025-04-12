"""
menu/admin.py

Registers Category and MenuItem models with the Django admin interface.

Features:
- Inline editing of MenuItems within their Category
- Filtering, searching, and display enhancements for easier staff management
"""

from django.contrib import admin
from .models import Category, MenuItem

# Inline admin interface to add/edit MenuItems directly within a Category admin page
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1  # Show one extra blank item by default for convenience

# Admin config for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  # Show category names in admin list view
    inlines = [MenuItemInline]  # Allow inline editing of related menu items

# Admin config for MenuItem model
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']  # Columns shown in list view
    list_filter = ['category']  # Filter sidebar for category
    search_fields = ['name', 'description']  # Enable admin search on name/description
