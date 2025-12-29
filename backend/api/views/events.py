"""
Event API endpoints
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import uuid

# Import your existing clickhouse_client
from ingestion.clickhouse_client import get_clickhouse_client


class IngestEventView(APIView):
    """
    POST /api/v1/events/ingest/
    Ingest a single event into ClickHouse
    """
    def post(self, request):
        try:
            event_data = request.data
            
            # Validate required fields
            required_fields = ['user_id', 'event_name', 'timestamp']
            for field in required_fields:
                if field not in event_data:
                    return Response(
                        {'error': f'Missing required field: {field}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Generate event_id if not provided
            event_id = event_data.get('event_id', str(uuid.uuid4()))
            
            # Insert into ClickHouse
            client = get_clickhouse_client()
            client.insert(
                'events',
                [[
                    event_id,
                    event_data['user_id'],
                    event_data['event_name'],
                    event_data['timestamp'],
                    json.dumps(event_data.get('properties', {})),
                    event_data.get('site_url', 'https://example.com')
                ]],
                column_names=['event_id', 'user_id', 'event_name', 
                             'timestamp', 'properties', 'site_url']
            )
            
            return Response(
                {
                    'message': 'Event ingested successfully',
                    'event_id': event_id
                },
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BatchIngestView(APIView):
    """
    POST /api/v1/events/batch/
    Ingest multiple events at once
    """
    def post(self, request):
        try:
            events = request.data.get('events', [])
            
            if not events:
                return Response(
                    {'error': 'No events provided'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            client = get_clickhouse_client()
            
            # Prepare batch data
            data = []
            for event in events:
                data.append([
                    event.get('event_id', str(uuid.uuid4())),
                    event['user_id'],
                    event['event_name'],
                    event['timestamp'],
                    json.dumps(event.get('properties', {})),
                    event.get('site_url', 'https://example.com')
                ])
            
            # Batch insert
            client.insert(
                'events',
                data,
                column_names=['event_id', 'user_id', 'event_name', 
                             'timestamp', 'properties', 'site_url']
            )
            
            return Response(
                {'message': f'{len(events)} events ingested'},
                status=status.HTTP_201_CREATED
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class QueryEventsView(APIView):
    """
    GET /api/v1/events/?user_id=X&limit=100
    Query events from ClickHouse
    """
    def get(self, request):
        try:
            client = get_clickhouse_client()
            
            # Get query parameters
            limit = int(request.GET.get('limit', 100))
            user_id = request.GET.get('user_id')
            event_name = request.GET.get('event_name')
            
            # Build query
            query = "SELECT * FROM events WHERE 1=1"
            params = {}
            
            if user_id:
                query += " AND user_id = %(user_id)s"
                params['user_id'] = user_id
            
            if event_name:
                query += " AND event_name = %(event_name)s"
                params['event_name'] = event_name
            
            query += f" ORDER BY timestamp DESC LIMIT {limit}"
            
            # Execute query
            result = client.query(query, parameters=params)
            
            # Convert to list of dicts
            events = []
            for row in result.result_rows:
                events.append({
                    'event_id': str(row[0]),
                    'user_id': row[1],
                    'event_name': row[2],
                    'timestamp': row[3].isoformat(),
                    'properties': json.loads(row[4]) if row[4] else {},
                    'site_url': row[5]
                })
            
            return Response({
                'count': len(events),
                'events': events
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class HealthCheckView(APIView):
    """
    GET /api/v1/health/
    Check API and ClickHouse health
    """
    def get(self, request):
        try:
            from ingestion.clickhouse_client import test_connection
            clickhouse_healthy = test_connection()
            
            return Response({
                'status': 'healthy' if clickhouse_healthy else 'degraded',
                'clickhouse': 'connected' if clickhouse_healthy else 'disconnected'
            })
        except Exception as e:
            return Response({
                'status': 'unhealthy',
                'error': str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)