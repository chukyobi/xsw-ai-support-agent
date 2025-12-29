"""
Health check endpoint
"""
from rest_framework.views import APIView
from rest_framework.response import Response

class HealthCheckView(APIView):
    """
    GET /api/v1/health/
    Check if API is running
    """
    def get(self, request):
        return Response({
            'status': 'healthy',
            'message': 'API is running!'
        })