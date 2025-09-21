"""
App configuration for listings.
"""
from django.apps import AppConfig


class ListingsConfig(AppConfig):
    """
    Configuration class for the listings app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'
    verbose_name = 'Travel Listings'
    
    def ready(self):
        """
        Import signals when the app is ready.
        """
        pass
