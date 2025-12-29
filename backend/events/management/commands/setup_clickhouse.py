"""
Django management command to initialize ClickHouse using your SQL file
"""
from django.core.management.base import BaseCommand
from pathlib import Path

# Import your existing clickhouse_client
from ingestion.clickhouse_client import get_clickhouse_client


class Command(BaseCommand):
    help = 'Initialize ClickHouse database using deployments/clickhouse-init.sql'

    def handle(self, *args, **options):
        self.stdout.write(' Setting up ClickHouse database...\n')
        
        try:
            # Get path to SQL file
            project_root = Path(__file__).resolve().parent.parent.parent.parent.parent
            sql_file = project_root / 'deployments' / 'clickhouse-init.sql'
            
            if not sql_file.exists():
                self.stdout.write(self.style.ERROR(f' SQL file not found: {sql_file}'))
                return
            
            # Read SQL file
            self.stdout.write(f'📄 Reading SQL from: {sql_file}')
            with open(sql_file, 'r') as f:
                sql_content = f.read()
            
            # Connect to ClickHouse
            self.stdout.write('🔌 Connecting to ClickHouse...')
            client = get_clickhouse_client()
            
            # Execute SQL statements (split by semicolon)
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements, 1):
                self.stdout.write(f'\n Executing statement {i}/{len(statements)}...')
                self.stdout.write(f'   {statement[:100]}...' if len(statement) > 100 else f'   {statement}')
                
                client.command(statement)
                self.stdout.write(self.style.SUCCESS('   Success'))
            
            # Verify table exists
            self.stdout.write('\n🔍 Verifying setup...')
            
            # Use the database name from settings
            from django.conf import settings
            db_name = settings.CLICKHOUSE_SETTINGS['database']
            
            result = client.query(f"SHOW TABLES FROM {db_name}")
            tables = [row[0] for row in result.result_rows]
            self.stdout.write(f'📊 Tables in database: {tables}')
            
            # Show table structure
            if 'events' in tables:
                self.stdout.write('\n📋 Events table structure:')
                result = client.query(f"DESCRIBE {db_name}.events")
                for row in result.result_rows:
                    self.stdout.write(f'   {row[0]}: {row[1]}')
            
            self.stdout.write(self.style.SUCCESS('\n ClickHouse setup complete!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n Error: {e}'))
            import traceback
            self.stdout.write(traceback.format_exc())