"""
menu/apps.py

Defines the application configuration for the 'menu' app,
which manages menu categories and items in the restaurant system.
"""

from django.apps import AppConfig


class MenuConfig(AppConfig):
    """
    Configuration class for the 'menu' app.

    Sets default auto primary key field and app name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'
