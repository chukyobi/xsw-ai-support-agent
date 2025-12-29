"""
ClickHouse Database Connection Helper
Works both inside and outside Django
"""
import clickhouse_connect
import os

def get_clickhouse_settings():
    """
    Get ClickHouse settings from environment or defaults
    """
    # Try to get settings from Django first
    try:
        # Ensure Django is set up to read settings
        if not os.environ.get('DJANGO_SETTINGS_MODULE'):
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xsw_backend.settings')
        
        import django
        try:
            django.setup()
        except Exception:
            # Maybe already setup or issue with setup, continue to try import
            pass

        from django.conf import settings
        if hasattr(settings, 'CLICKHOUSE_SETTINGS'):
            return settings.CLICKHOUSE_SETTINGS
    except Exception as e:
        print(f"Warning: Could not load Django settings: {e}")
    
    # Fallback to environment variables or defaults
    return {
        'host': os.environ.get('CLICKHOUSE_HOST', 'localhost'),
        'port': int(os.environ.get('CLICKHOUSE_PORT', 8123)),
        'username': os.environ.get('CLICKHOUSE_USER', 'default'),
        'password': os.environ.get('CLICKHOUSE_PASSWORD', 'default'),
        'database': os.environ.get('CLICKHOUSE_DB', 'default'),
    }

def get_clickhouse_client():
    """
    Create and return a ClickHouse client connection
    """
    settings = get_clickhouse_settings()
    
    client = clickhouse_connect.get_client(
        host=settings['host'],
        port=settings['port'],
        username=settings['username'],
        password=settings['password'],
        database=settings['database']
    )
    return client

def test_connection():
    """
    Test if ClickHouse connection works
    """
    try:
        client = get_clickhouse_client()
        result = client.query("SELECT version()")
        version = result.first_row[0]
        print(f"Connected to ClickHouse version: {version}")
        return True
    except Exception as e:
        print(f"ClickHouse connection failed: {e}")
        return False

if __name__ == "__main__":
    # Quick test when run directly
    print("Testing ClickHouse connection...")
    test_connection()