"""
ClickHouse Database Connection Helper
"""
import clickhouse_connect
from django.conf import settings

def get_clickhouse_client():
    """
    Create and return a ClickHouse client connection
    """
    client = clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_SETTINGS['host'],
        port=settings.CLICKHOUSE_SETTINGS['port'],
        username=settings.CLICKHOUSE_SETTINGS['username'],
        password=settings.CLICKHOUSE_SETTINGS['password'],
        database=settings.CLICKHOUSE_SETTINGS['database']
    )
    return client

def test_connection():
    """
    Test if ClickHouse connection works
    """
    try:
        client = get_clickhouse_client()
        result = client.query("SELECT version()")
        print(f"Connected to ClickHouse version: {result.first_row[0]}")
        return True
    except Exception as e:
        print(f"ClickHouse connection failed: {e}")
        return False