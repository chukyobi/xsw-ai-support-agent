# XSW AI Support Agent

An autonomous AI agent that investigates user issues by querying ClickHouse event data and providing root cause analysis.

## 🎯 What This Project Does

This project demonstrates a complete **Agentic AI** system that can autonomously diagnose user problems:

1. **The Memory (ClickHouse):** Stores 100k+ user events (page views, payments, errors)
2. **The Data Pipeline (`ingestion/`):** Generates and uploads mock event data with intentional anomalies
3. **The Brain (`backend/agent/`):** An AI agent powered by Groq (Llama 3) that can write and execute SQL queries autonomously to find root causes

**Example:** User complains "I keep getting payment errors" → Agent queries database → Finds `payment_failed` events with `database_timeout` error → Provides diagnosis

---

## 📁 Project Structure

```
xsw-ai-support-agent/
├── backend/
│   ├── agent/
│   │   ├── clickhouse_tool.py      # LangChain tool for SQL execution
│   │   └── investigation_agent.py  # Main agent logic
│   ├── xsw_backend/
│   │   └── settings.py             # Django settings (ClickHouse credentials)
│   ├── .env                        # Environment variables (DO NOT COMMIT)
│   └── venv/                       # Python virtual environment
├── deployments/
│   ├── docker-compose.yml          # 🐳 Docker setup for ClickHouse & Redis
│   └── clickhouse-init.sql         # Database initialization script
├── ingestion/
│   ├── clickhouse_client.py        # ClickHouse connection helper
│   └── mock_generator.py           # Event data generator (100k+ events)
├── demo_agent.py                   # 🚀 Main demo script
├── query_clickhouse.py             # Helper script to query ClickHouse
├── requirements.txt                # Python dependencies
└── .env.example                    # Template for environment variables
```

---

## 🚀 Complete Setup Guide

### Prerequisites

Before starting, ensure you have:

1. **Python 3.9+** installed
   ```bash
   python3 --version
   ```

2. **ClickHouse** installed and running
   - **macOS (Homebrew):**
     ```bash
     brew install clickhouse
     brew services start clickhouse
     ```
   - **Other platforms:** See [ClickHouse Installation Guide](https://clickhouse.com/docs/en/install)

3. **Groq API Key** (free tier available)
   - Visit [console.groq.com](https://console.groq.com)
   - Sign up and create an API key

---

### Step 1: Clone and Navigate to Project

```bash
cd /Users/mac/Documents/DevWork/AI/xsw-ai-support-agent
```

---

### Step 2: Set Up Python Virtual Environment

The project already has a virtual environment in `backend/venv/`, but if you need to recreate it:

```bash
# Create virtual environment
python3 -m venv backend/venv

# Activate it
source backend/venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Verify installation:**
```bash
backend/venv/bin/pip list | grep -E "(langchain|clickhouse|groq|django)"
```

You should see:
- `langchain`, `langchain-groq`, `langchain-core`
- `clickhouse-connect`
- `groq`
- `Django`, `djangorestframework`

---

### Step 3: Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp .env.example backend/.env
   ```

2. **Edit `backend/.env` and add your Groq API key:**
   ```bash
   nano backend/.env
   ```
   
   Replace `your_groq_api_key_here` with your actual API key:
   ```
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

3. **Export the API key for the demo script:**
   ```bash
   export GROQ_API_KEY="gsk_your_actual_key_here"
   ```

---

### Step 4: Set Up ClickHouse Database

The project includes a [`docker-compose.yml`](deployments/docker-compose.yml) file that sets up both ClickHouse and Redis.

1. **Start the services:**
   ```bash
   cd deployments
   docker-compose up -d
   ```

2. **Verify services are running:**
   ```bash
   docker-compose ps
   ```
   
   You should see both `clickhouse` and `redis` running.

3. **Test ClickHouse connection:**
   ```bash
   docker-compose exec clickhouse clickhouse-client --password
   # Enter password: password123
   # You should see: ClickHouse client version...
   ```

4. **The settings in `backend/xsw_backend/settings.py` should match:**
   ```python
   CLICKHOUSE_SETTINGS = {
       'host': 'localhost',
       'port': 8123,
       'username': 'default',
       'password': 'password123',
       'database': 'default',
   }
   ```

> [!NOTE]
> The docker-compose file also includes Redis for future caching features. The `clickhouse-init.sql` file automatically creates the database schema on first startup.

---

### Step 5: Generate and Upload Mock Data

This step creates 100,000+ events with intentional anomalies for the agent to investigate.

```bash
# Make sure you're in the project root directory
cd /Users/mac/Documents/DevWork/AI/xsw-ai-support-agent

# Activate virtual environment
source backend/venv/bin/activate

# Run the data generator
python ingestion/mock_generator.py
```

**Expected output:**
```
Generating 100000 events with 5.0% anomalies...
Generated 5500 anomaly events
Generating 94500 normal events...
  Progress: 10000/94500 normal events generated
  ...
Connecting to ClickHouse...
Table 'events' is ready.
Uploading 100000 events to ClickHouse...
  Uploaded batch 1/10
  ...
Upload complete!
```

**Verify data was uploaded:**
```bash
python query_clickhouse.py "SELECT event, count() FROM events GROUP BY event"
```

You should see event counts like:
```
page_view: 45000
payment_success: 12000
payment_failed: 3000
...
```

---

### Step 6: Run the AI Agent Demo

Now for the exciting part! 🎉

```bash
# Make sure GROQ_API_KEY is exported
export GROQ_API_KEY="gsk_your_actual_key_here"

# Run the demo
python demo_agent.py
```

**What happens:**
1. The script initializes the AI agent with Llama 3 (70B) via Groq
2. Presents a mock scenario: "User 'user_42' reported 'I keep getting errors when trying to pay'"
3. The agent autonomously:
   - Formulates a hypothesis
   - Writes SQL queries to investigate
   - Analyzes the results
   - Provides a root cause analysis

**Example output:**
```
=== XSW AI Support Agent Demo ===

Initializing Agent...

Scenario: User 'user_42' reported 'I keep getting errors when trying to pay'.
Agent is investigating...

[Agent Tool] Executing: SELECT * FROM events WHERE user_id='user_42' AND event='payment_failed' ORDER BY timestamp DESC LIMIT 10

=== Agent Analysis ===
Based on my investigation, user_42 experienced 3 payment failures in the last 24 hours.
The root cause is database_timeout errors (error_code: 500) occurring during checkout.
This suggests the payment gateway is experiencing connectivity issues with the database.

Recommendation: Check database connection pool settings and increase timeout thresholds.
======================
```

---

## 🔧 Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Solution:**
```bash
export GROQ_API_KEY="gsk_your_actual_key_here"
```

Make sure to run this in the same terminal session where you run `demo_agent.py`.

---

### Issue: "ClickHouse connection failed"

**Possible causes:**

1. **ClickHouse not running:**
   
   **Docker Compose (recommended):**
   ```bash
   cd deployments
   docker-compose ps
   # If not running:
   docker-compose up -d
   ```
   
   **Docker (standalone):**
   ```bash
   docker ps | grep clickhouse
   # If not running:
   docker start clickhouse-server
   ```
   
   **Local:**
   ```bash
   brew services start clickhouse
   ```

2. **Wrong password:**
   - Check `backend/xsw_backend/settings.py`
   - Default is `password123`
   - Reset if needed:
     
     **Docker Compose:**
     ```bash
     cd deployments
     docker-compose exec clickhouse clickhouse-client --password
     ALTER USER default IDENTIFIED WITH plaintext_password BY 'password123';
     ```
     
     **Docker (standalone):**
     ```bash
     docker exec -it clickhouse-server clickhouse-client --password
     ALTER USER default IDENTIFIED WITH plaintext_password BY 'password123';
     ```
     
     **Local:**
     ```bash
     clickhouse client
     ALTER USER default IDENTIFIED WITH plaintext_password BY 'password123';
     ```

3. **Test connection manually:**
   ```bash
   python ingestion/clickhouse_client.py
   ```

---

### Issue: "ModuleNotFoundError: No module named 'langchain'"

**Solution:**
```bash
source backend/venv/bin/activate
pip install -r requirements.txt
```

---

### Issue: "Query returned 0 rows"

This means the mock data wasn't uploaded or the user_id doesn't exist.

**Solution:**
1. **Check if data exists:**
   ```bash
   python query_clickhouse.py "SELECT count() FROM events"
   ```

2. **If 0, regenerate data:**
   ```bash
   python ingestion/mock_generator.py
   ```

3. **Pick a user that exists:**
   ```bash
   python query_clickhouse.py "SELECT DISTINCT user_id FROM events LIMIT 10"
   ```
   
   Then edit `demo_agent.py` line 34 to use one of those user IDs.

---

## 🧪 Testing the Agent with Different Scenarios

You can modify `demo_agent.py` to test different scenarios:

```python
# Line 34-38 in demo_agent.py

# Scenario 1: Payment issues
user_id = "user_42"
query = f"Investigate why user '{user_id}' is facing payment issues."

# Scenario 2: Bot detection
user_id = "user_123"
query = f"Check if user '{user_id}' shows bot-like behavior."

# Scenario 3: Late-night suspicious activity
query = "Find users with high-value transactions between 2-4 AM."

# Scenario 4: General investigation
query = "What are the most common errors in the last 24 hours?"
```

---

## 📊 Understanding the Data

### Events Table Schema

```sql
CREATE TABLE events (
    event_id String,      -- Unique event identifier
    user_id String,       -- User identifier (e.g., "user_42")
    event String,         -- Event type (e.g., "payment_failed")
    timestamp DateTime,   -- When the event occurred
    properties String     -- JSON string with event details
) ENGINE = MergeTree()
ORDER BY (event, timestamp)
```

### Sample Event

```json
{
  "event_id": "abc-123",
  "user_id": "user_42",
  "event": "payment_failed",
  "timestamp": "2025-12-29T14:05:00",
  "properties": {
    "error_code": 500,
    "message": "database_timeout",
    "amount": 49.99,
    "payment_method": "credit_card"
  }
}
```

### Event Types

- `page_view` - User viewed a page
- `button_click` - User clicked a button
- `form_submit` - User submitted a form
- `video_play` - User played a video
- `search` - User performed a search
- `add_to_cart` - User added item to cart
- `checkout_start` - User started checkout
- `payment_success` - Payment completed successfully
- `payment_failed` - Payment failed (with error details)
- `logout` - User logged out

### Intentional Anomalies

The mock data generator creates these patterns for the agent to detect:

1. **Rapid page views → payment failure**
   - 10 page views in <2 minutes
   - Followed by `payment_failed` with `database_timeout`

2. **Cart abandonment**
   - Multiple `add_to_cart` events
   - `checkout_start`
   - `payment_failed` with `card_declined_insufficient_funds`

3. **Bot-like behavior**
   - Identical events at regular intervals (every 5 seconds)
   - Same properties (page, browser, etc.)

4. **Late-night suspicious activity**
   - High-value transactions ($800-2000) at 3-4 AM
   - Unusual locations or VPN detected

---

## 🛠️ How It Works

### The Agent Workflow

**User Complaint:** "I tried to buy a shirt 5 minutes ago and it failed!"

**Agent's Thought Process:**
1. **Hypothesis:** "Maybe they have failed payment events"
2. **Action:** Writes SQL: `SELECT * FROM events WHERE user_id='user_42' AND event='payment_failed'`
3. **Observation:** Finds error: `{"error_code": 500, "message": "database_timeout"}`
4. **Analysis:** "The user experienced a database timeout during payment at 2:05 PM"

### The Tool (ClickHouseTool)

Located in [`backend/agent/clickhouse_tool.py`](backend/agent/clickhouse_tool.py):
- Accepts SQL queries from the AI
- Executes them against ClickHouse
- Returns formatted results to the AI
- Limits results to 20 rows to prevent context overflow

### The Brain (Investigation Agent)

Located in [`backend/agent/investigation_agent.py`](backend/agent/investigation_agent.py):
- **Model:** Llama 3 (70B) via Groq
- **Temperature:** 0 (deterministic)
- **Prompt:** Instructs the AI to act as a Support Engineer
- **Schema:** Provides the `events` table structure
- **Verbose:** Shows the agent's reasoning process

---

## 🎓 Next Steps

1. **Customize the agent** by editing the system prompt in `investigation_agent.py`
2. **Add more tools** (e.g., send emails, create tickets, query other databases)
3. **Build a web interface** using Django REST Framework
4. **Deploy to production** with proper authentication and rate limiting
5. **Add more event types** and anomaly patterns in `mock_generator.py`

---

## 🔐 Security Notes

> [!WARNING]
> **DO NOT commit `.env` files to Git!**

The `.gitignore` file is configured to exclude:
- `backend/.env` (contains API keys)
- `backend/venv/` (virtual environment)
- `*.ndjson` (large data files)
- `db.sqlite3` (database files)

Always use `.env.example` as a template and keep your actual `.env` file private.

---

## 🚀 Why Groq + Llama 3?

- **Fast:** Groq's inference is extremely fast (~500 tokens/sec)
- **Cost-effective:** Free tier available, cheaper than GPT-4
- **Powerful:** Llama 3 70B handles SQL generation and reasoning well
- **Open:** Can switch to other providers easily via LangChain

---

## 📝 Quick Reference Commands

```bash
# Activate virtual environment
source backend/venv/bin/activate

# Generate mock data
python ingestion/mock_generator.py

# Query ClickHouse manually
python query_clickhouse.py "SELECT count() FROM events"

# Run the AI agent demo
export GROQ_API_KEY="gsk_..."
python demo_agent.py

# ClickHouse with Docker Compose (recommended)
cd deployments
docker-compose up -d
docker-compose down
docker-compose exec clickhouse clickhouse-client --password
# Password: password123

# ClickHouse with Docker (standalone)
docker start clickhouse-server
docker stop clickhouse-server
docker exec -it clickhouse-server clickhouse-client --password
# Password: password123

# ClickHouse with Homebrew
brew services start clickhouse
brew services stop clickhouse
clickhouse client --password
# Password: password123
```

---

## 📄 License

This is a demonstration project for educational purposes.

---

## 🤝 Contributing

Feel free to fork this project and experiment with:
- Different LLM providers (OpenAI, Anthropic, local models)
- Additional tools for the agent
- More complex anomaly patterns
- Real-time event streaming
- Multi-agent collaboration

---

**Happy Investigating! 🔍🤖**
