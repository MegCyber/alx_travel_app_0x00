"""
URL configuration for listings app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for ViewSets (when you add them later)
router = DefaultRouter()

app_name = 'listings'

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Health check endpoint
    path('health/', views.health_check, name='health-check'),
]
