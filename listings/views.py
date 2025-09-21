"""
Views for the listings app.
"""
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    operation_description="Health check endpoint to verify API is running",
    responses={
        200: openapi.Response(
            description="API is healthy",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'status': openapi.Schema(type=openapi.TYPE_STRING, description='Health status'),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Status message'),
                }
            )
        )
    }
)
@api_view(['GET'])
def health_check(request):
    """
    Simple health check endpoint.
    Returns a JSON response indicating the API is running.
    """
    return Response({
        'status': 'healthy',
        'message': 'ALX Travel App API is running successfully!'
    }, status=status.HTTP_200_OK)
