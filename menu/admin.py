from django.contrib import admin
from .models import Category, MenuItem

# Register your models here.
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [MenuItemInline]

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']
    list_filter = ['category']
    search_fields = ['name', 'description']
