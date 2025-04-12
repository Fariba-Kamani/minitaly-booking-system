"""
menu/models.py

Defines the models for the restaurant menu.

Includes:
- Category: Menu item categories (e.g., Starters, Main Courses)
- MenuItem: Individual dishes with descriptions, pricing, and categorization
"""

from django.db import models


class Category(models.Model):
    """
    Represents a category of menu items (e.g., Starters, Desserts).
    
    Fields:
        name (str): The name of the category.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    Represents an individual dish on the menu.

    Fields:
        category (ForeignKey): Link to the Category this item belongs to.
        name (str): Name of the menu item.
        description (str): Optional description of the item.
        price (Decimal): Price of the item in euros (up to 9999.99).
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='menu_items'
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
