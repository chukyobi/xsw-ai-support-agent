"""
Event Generator with Anomalies
Generates 100,000+ events with intentional anomaly patterns for AI agent detection
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid

class XswEventGenerator:
    def __init__(self):
        self.events = []
        self.user_ids = [f"user_{i}" for i in range(1, 501)]  # 500 users
        self.event_types = [
            "page_view",
            "button_click",
            "form_submit",
            "video_play",
            "search",
            "add_to_cart",
            "checkout_start",
            "payment_success",
            "payment_failed",
            "logout"
        ]
        self.pages = [
            "/home", "/products", "/pricing", "/about", 
            "/contact", "/dashboard", "/settings", "/checkout"
        ]
        
    def generate_timestamp(self, base_time: datetime, offset_minutes: int = 0) -> str:
        """Generate ISO format timestamp"""
        return (base_time + timedelta(minutes=offset_minutes)).isoformat()
    
    def create_normal_event(self, user_id: str, timestamp: datetime) -> Dict[str, Any]:
        """Create a normal event with realistic properties"""
        event_type = random.choice(self.event_types)
        
        base_event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "event": event_type,
            "timestamp": self.generate_timestamp(timestamp),
            "properties": {
                "platform": random.choice(["web", "mobile", "tablet"]),
                "browser": random.choice(["chrome", "firefox", "safari", "edge"]),
                "os": random.choice(["windows", "mac", "linux", "ios", "android"]),
            }
        }
        
        # Add event-specific properties
        if event_type == "page_view":
            base_event["properties"]["page"] = random.choice(self.pages)
            base_event["properties"]["referrer"] = random.choice(["google", "direct", "facebook", "twitter"])
            base_event["properties"]["session_duration"] = random.randint(10, 600)
            
        elif event_type == "button_click":
            base_event["properties"]["button_id"] = random.choice(["cta_main", "nav_menu", "buy_now", "learn_more"])
            base_event["properties"]["page"] = random.choice(self.pages)
            
        elif event_type == "payment_success":
            base_event["properties"]["amount"] = round(random.uniform(10, 500), 2)
            base_event["properties"]["currency"] = "USD"
            base_event["properties"]["payment_method"] = random.choice(["credit_card", "paypal", "stripe"])
            
        elif event_type == "search":
            base_event["properties"]["query"] = random.choice(["pricing", "features", "documentation", "support"])
            base_event["properties"]["results_count"] = random.randint(0, 100)
            
        return base_event
    
    def create_anomaly_pattern_1(self, user_id: str, start_time: datetime) -> List[Dict[str, Any]]:
        """
        Anomaly Pattern 1: Rapid page views followed by payment failure
        10 consecutive page_view events + payment_failed with database_timeout
        """
        anomaly_events = []
        
        # 10 rapid page views (within 2 minutes)
        for i in range(10):
            event = {
                "event_id": str(uuid.uuid4()),
                "user_id": user_id,
                "event": "page_view",
                "timestamp": self.generate_timestamp(start_time, i * 0.2),  # 12 seconds apart
                "properties": {
                    "page": random.choice(self.pages),
                    "platform": "web",
                    "browser": "chrome",
                    "session_duration": random.randint(5, 15),
                    "is_rapid": True  # Flag for anomaly
                }
            }
            anomaly_events.append(event)
        
        # Payment failed event
        failed_event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "event": "payment_failed",
            "timestamp": self.generate_timestamp(start_time, 2.5),
            "properties": {
                "error_code": 500,
                "message": "database_timeout",
                "amount": round(random.uniform(50, 500), 2),
                "payment_method": "credit_card",
                "retry_count": 0
            }
        }
        anomaly_events.append(failed_event)
        
        return anomaly_events
    
    def create_anomaly_pattern_2(self, user_id: str, start_time: datetime) -> List[Dict[str, Any]]:
        """
        Anomaly Pattern 2: Cart abandonment with specific error
        Multiple add_to_cart events, checkout_start, then payment_failed with card_declined
        """
        anomaly_events = []
        
        # 3-5 add to cart events
        for i in range(random.randint(3, 5)):
            event = {
                "event_id": str(uuid.uuid4()),
                "user_id": user_id,
                "event": "add_to_cart",
                "timestamp": self.generate_timestamp(start_time, i * 2),
                "properties": {
                    "product_id": f"prod_{random.randint(100, 999)}",
                    "price": round(random.uniform(20, 200), 2),
                    "quantity": random.randint(1, 3)
                }
            }
            anomaly_events.append(event)
        
        # Checkout start
        checkout_event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "event": "checkout_start",
            "timestamp": self.generate_timestamp(start_time, 10),
            "properties": {
                "cart_value": round(random.uniform(100, 600), 2),
                "item_count": random.randint(3, 5)
            }
        }
        anomaly_events.append(checkout_event)
        
        # Payment failed
        failed_event = {
            "event_id": str(uuid.uuid4()),
            "user_id": user_id,
            "event": "payment_failed",
            "timestamp": self.generate_timestamp(start_time, 12),
            "properties": {
                "error_code": 402,
                "message": "card_declined_insufficient_funds",
                "amount": round(random.uniform(100, 600), 2),
                "payment_method": "credit_card",
                "retry_count": 2
            }
        }
        anomaly_events.append(failed_event)
        
        return anomaly_events
    
    def create_anomaly_pattern_3(self, user_id: str, start_time: datetime) -> List[Dict[str, Any]]:
        """
        Anomaly Pattern 3: Bot-like behavior
        Identical events with same properties at regular intervals
        """
        anomaly_events = []
        
        # 15 identical page views every 5 seconds
        for i in range(15):
            event = {
                "event_id": str(uuid.uuid4()),
                "user_id": user_id,
                "event": "page_view",
                "timestamp": self.generate_timestamp(start_time, i * 0.083),  # 5 seconds
                "properties": {
                    "page": "/pricing",
                    "platform": "web",
                    "browser": "chrome",
                    "session_duration": 5,
                    "bot_pattern": True
                }
            }
            anomaly_events.append(event)
        
        return anomaly_events
    
    def create_anomaly_pattern_4(self, user_id: str, start_time: datetime) -> List[Dict[str, Any]]:
        """
        Anomaly Pattern 4: Late night suspicious activity
        Multiple high-value transactions at unusual hours
        """
        anomaly_events = []
        
        # Set time to 3 AM
        late_night = start_time.replace(hour=3, minute=random.randint(0, 59))
        
        for i in range(5):
            event = {
                "event_id": str(uuid.uuid4()),
                "user_id": user_id,
                "event": "payment_success",
                "timestamp": self.generate_timestamp(late_night, i * 1),
                "properties": {
                    "amount": round(random.uniform(800, 2000), 2),  # High value
                    "currency": "USD",
                    "payment_method": "credit_card",
                    "unusual_hour": True,
                    "location": random.choice(["unknown", "VPN_detected"])
                }
            }
            anomaly_events.append(event)
        
        return anomaly_events
    
    def generate_events(self, total_events: int = 100000, anomaly_ratio: float = 0.05):
        """
        Generate total_events with anomaly_ratio percentage being anomalies
        """
        print(f"Generating {total_events} events with {anomaly_ratio*100}% anomalies...")
        
        base_time = datetime.now() - timedelta(days=30)  # Start 30 days ago
        num_anomalies = int(total_events * anomaly_ratio)
        
        # Generate anomalies first
        anomaly_users = random.sample(self.user_ids, min(num_anomalies // 10, len(self.user_ids)))
        
        anomaly_count = 0
        for user in anomaly_users:
            if anomaly_count >= num_anomalies:
                break
                
            # Randomly choose anomaly pattern
            pattern = random.choice([1, 2, 3, 4])
            random_time = base_time + timedelta(minutes=random.randint(0, 43200))  # Random time in 30 days
            
            if pattern == 1:
                anomaly_events = self.create_anomaly_pattern_1(user, random_time)
            elif pattern == 2:
                anomaly_events = self.create_anomaly_pattern_2(user, random_time)
            elif pattern == 3:
                anomaly_events = self.create_anomaly_pattern_3(user, random_time)
            else:
                anomaly_events = self.create_anomaly_pattern_4(user, random_time)
            
            self.events.extend(anomaly_events)
            anomaly_count += len(anomaly_events)
        
        print(f"Generated {anomaly_count} anomaly events")
        
        # Generate normal events
        normal_events_needed = total_events - len(self.events)
        print(f"Generating {normal_events_needed} normal events...")
        
        for i in range(normal_events_needed):
            user_id = random.choice(self.user_ids)
            random_time = base_time + timedelta(minutes=random.randint(0, 43200))
            event = self.create_normal_event(user_id, random_time)
            self.events.append(event)
            
            if (i + 1) % 10000 == 0:
                print(f"  Progress: {i + 1}/{normal_events_needed} normal events generated")
        
        # Sort events by timestamp
        self.events.sort(key=lambda x: x["timestamp"])
        
        print(f"\nTotal events generated: {len(self.events)}")
        return self.events
    
    def save_to_file(self, filename: str = "events.json"):
        """Save events to JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=2)
        print(f"Events saved to {filename}")
    
    def save_to_ndjson(self, filename: str = "events.ndjson"):
        """Save events to newline-delimited JSON (better for streaming)"""
        with open(filename, 'w') as f:
            for event in self.events:
                f.write(json.dumps(event) + '\n')
        print(f"Events saved to {filename}")
    
    def get_statistics(self):
        """Print statistics about generated events"""
        print("\n=== Event Statistics ===")
        print(f"Total events: {len(self.events)}")
        
        # Count by event type
        event_types = {}
        for event in self.events:
            event_type = event["event"]
            event_types[event_type] = event_types.get(event_type, 0) + 1
        
        print("\nEvents by type:")
        for event_type, count in sorted(event_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {event_type}: {count}")
        
        # Count anomalies
        anomalies = sum(1 for e in self.events if 
                       e["properties"].get("is_rapid") or 
                       e["properties"].get("bot_pattern") or 
                       e["properties"].get("unusual_hour") or
                       (e["event"] == "payment_failed" and "database_timeout" in str(e["properties"])))
        
        print(f"\nDetectable anomaly events: ~{anomalies}")
        print(f"Anomaly ratio: {anomalies/len(self.events)*100:.2f}%")



import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ingestion.clickhouse_client import get_clickhouse_client

def create_events_table(client):
    """Create events table if it doesn't exist"""
    print("Ensuring 'events' table exists...")
    client.command("""
        CREATE TABLE IF NOT EXISTS events (
            event_id String,
            user_id String,
            event String,
            timestamp DateTime,
            properties String
        ) ENGINE = MergeTree()
        ORDER BY (event, timestamp)
    """)
    print("Table 'events' is ready.")

def upload_to_clickhouse(client, events):
    """Upload events to ClickHouse in batches"""
    print(f"Uploading {len(events)} events to ClickHouse...")
    
    # Prepare data for insertion
    data = []
    for event in events:
        data.append([
            event['event_id'],
            event['user_id'],
            event['event'],
            datetime.fromisoformat(event['timestamp']),
            json.dumps(event['properties'])
        ])
    
    # Insert in batches of 10,000
    batch_size = 10000
    total_batches = (len(data) + batch_size - 1) // batch_size
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        client.insert('events', batch, column_names=['event_id', 'user_id', 'event', 'timestamp', 'properties'])
        print(f"  Uploaded batch {i//batch_size + 1}/{total_batches}")
    
    print("Upload complete!")

def main():
    """Main execution function"""
    generator = XswEventGenerator()
    
    # Generate 100,000+ events with 5% anomalies
    events = generator.generate_events(total_events=100000, anomaly_ratio=0.05)
    
    # Save to files
    generator.save_to_ndjson("events.ndjson")  # Recommended format
    
    # Upload to ClickHouse
    try:
        print("\nConnecting to ClickHouse...")
        client = get_clickhouse_client()
        create_events_table(client)
        upload_to_clickhouse(client, events)
    except Exception as e:
        print(f"\nFailed to upload to ClickHouse: {e}")
    
    # Print statistics
    generator.get_statistics()
    
    print("\nEvent generation and ingestion complete!")
    print("\nAnomalies to look for:")
    print("1. Rapid page views (10 in <2 min) → payment_failed with database_timeout")
    print("2. Cart abandonment → payment_failed with card_declined")
    print("3. Bot patterns (identical events at regular intervals)")
    print("4. Late night high-value transactions (3-4 AM, $800-2000)")


if __name__ == "__main__":
    main()