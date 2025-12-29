"""
API URL Configuration
All endpoints are prefixed with /api/v1/
"""
from django.urls import path
from api.views.events import (
    IngestEventView, 
    BatchIngestView,
    QueryEventsView,
    HealthCheckView
)

urlpatterns = [
    # Health check
    path('health/', HealthCheckView.as_view(), name='health'),
    
    # Event ingestion
    path('events/ingest/', IngestEventView.as_view(), name='ingest-event'),
    path('events/batch/', BatchIngestView.as_view(), name='batch-ingest'),
    
    # Event querying
    path('events/', QueryEventsView.as_view(), name='query-events'),
]