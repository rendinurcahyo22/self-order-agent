# Self-Order Agent 🍽️

A sophisticated multi-tool AI agent built with Google's Agent Development Kit (ADK) that enables customers to seamlessly order food through natural conversation. The agent handles the complete ordering workflow including menu browsing, order creation, promotion application, payment processing, and order management.

## 🎯 Overview

This project demonstrates a production-ready conversational AI agent that can:

- **Browse Menus**: Retrieve and display food items from BigQuery database
- **Manage Orders**: Create, save, and retrieve customer orders
- **Apply Promotions**: Validate and apply discount codes and special offers
- **Process Payments**: Handle secure payment transactions with UUID tracking
- **Provide Support**: Answer questions and guide customers through the ordering process

The agent uses Google's Agent Development Kit (ADK) framework with Gemini 2.5 Flash model and integrates with Google Cloud BigQuery for data persistence.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Customer      │    │   Root Agent     │    │  Google Cloud   │
│   Interface     │◄──►│  (Gemini 2.5)    │◄──►│   BigQuery      │
│  (ADK Web UI)   │    │                  │    │   Database      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Tool Functions │
                       │  • save_order    │
                       │  • get_order     │
                       │  • get_menu      │
                       │  • get_promo     │
                       │  • process_payment│
                       └──────────────────┘
```

The system follows a **single-agent architecture** with multiple tools, replacing complex multi-agent workflows with a streamlined approach that's easier to maintain and debug.

## 👤 User Identification & Session Management

The agent includes a comprehensive user identification system to personalize the ordering experience:

### Features:
- **User Recognition**: Identifies users by email, name, or phone
- **Session Management**: Maintains conversation context and current order state
- **Order History**: Tracks previous orders for each user
- **Preferences**: Stores dietary restrictions and preferences
- **Personalization**: Customizes recommendations based on user profile

### User Tools:
- `get_user_info(user_identifier)` - Retrieve user profile and preferences
- `create_user_session(user_identifier)` - Initialize user session with context
- `get_user_orders(user_identifier)` - Get user's order history
- `save_order_with_user(order, user_identifier)` - Save order with user context

### Demo Users:
The system includes demo users for testing:
- **john@example.com**: Vegetarian, mild spice preference
- **jane@example.com**: Vegan, hot spice preference

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.9+ 
- **Operating System**: macOS, Linux, or Windows
- **IDE**: VS Code, PyCharm, or similar (recommended)

### Google Cloud Setup
1. **Google Cloud Project**: Active GCP project with billing enabled
2. **BigQuery**: Enabled BigQuery API with appropriate datasets
3. **Authentication**: One of the following:
   - Google AI Studio API key (easier for development)
   - Google Cloud service account credentials (recommended for production)

### Required APIs
- Google AI Studio API (for Gemini model access)
- BigQuery API (for data storage and retrieval)

## 🚀 Installation

### 1. Clone and Setup Environment

```bash
# Clone the repository
cd /path/to/your/projects
git clone <repository-url>
cd self-order-agent

# Create and activate virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate
# Windows CMD:
.venv\Scripts\activate.bat
# Windows PowerShell:
.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**Dependencies installed:**
- `google-adk` - Google Agent Development Kit
- `google-cloud-bigquery` - BigQuery client library  
- `python-dotenv` - Environment variable management
- `PyYAML` - YAML configuration support

### 3. Environment Configuration

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Google AI Studio API Key (get from https://aistudio.google.com/apikey)
GOOGLE_API_KEY=your_actual_api_key_here

# Google Cloud Configuration
PROJECT_ID=your-gcp-project-id
BIGQUERY_DATASET=self_order_agent

# Optional: Force local fallback mode for testing
# FORCE_LOCAL_ADK_FALLBACK=1
```

### 4. BigQuery Setup

Ensure your BigQuery dataset contains these tables:

```sql
-- Menu table
CREATE TABLE `your-project.self_order_agent.menu` (
  item_id STRING,
  name STRING,
  description STRING,
  price FLOAT64,
  category STRING,
  available BOOLEAN
);

-- Orders table  
CREATE TABLE `your-project.self_order_agent.orders` (
  order_id STRING,
  customer_name STRING,
  items ARRAY<STRUCT<item_id STRING, quantity INT64>>,
  total_amount FLOAT64,
  status STRING,
  created_at TIMESTAMP
);

-- Promotions table
CREATE TABLE `your-project.self_order_agent.promo` (
  promo_code STRING,
  discount_percent FLOAT64,
  min_order_amount FLOAT64,
  valid_until DATE,
  active BOOLEAN
);
```

## 🧪 Testing Your Agent

### Method 1: ADK Web Interface (Recommended)

1. **Start the development server:**
   ```bash
   cd /path/to/self-order-agent
   adk web --port 8002
   ```

2. **Open in browser:** http://localhost:8002

3. **Select your agent:** Choose "self_order_agent" from the dropdown

4. **Test with these prompts:**

#### 🍽️ Menu Browsing Tests
```
Show me the menu
What food do you have available?
Do you have vegetarian options?
List all items under $10
```

#### 📦 Order Creation Tests  
```
I want to order a burger and fries
Can I get a pizza with extra cheese?
I'd like to place an order for delivery
Create an order with 2 burgers and 1 drink
```

#### � Promotion Tests
```
Do you have any current promotions?
Can I use promo code SAVE20?
Apply discount code STUDENT10 to my order
What deals are available today?
```

#### 💳 Payment Tests
```
Process payment for $25.50
I want to pay with credit card
Complete my payment of $15.75
Process payment in EUR currency
```

#### � Complete Workflow Tests
```
I want to order a pizza, apply any available discounts, and pay $20
Show me the menu, help me order something under $15, and process payment
Help me order lunch for 2 people with a budget of $30
```

### 💬 Conversational Tests
```
Hi, I'm hungry and need help ordering food
What would you recommend for a quick lunch?
I'm on a diet, what are my healthiest options?
I have a food allergy, can you help me choose safely?
I'm having a party, what should I order for 10 people?
```

### 👤 User Identification Tests
```
Hi, I'm john@example.com
My name is Jane Smith, email jane@example.com  
I'm a new customer, my email is test@example.com
What's my order history?
Show me my previous orders
What are my food preferences?
I'm vegetarian, can you recommend something?
```

### 🔄 Session Management Tests
```
Start a new order for john@example.com
Add burger to my current order
What's in my cart right now?
Save my current session
Resume my previous session
```

## 🔍 Verifying Order Entry

To ensure orders are entered perfectly into BigQuery, use these verification methods:

### Method 1: Automated Verification Script
```bash
# Run comprehensive order verification
python verify_orders.py

# This will:
# - Create a test order
# - Save it to BigQuery  
# - Retrieve and verify all fields
# - Check data integrity
# - Show recent orders
```

### Method 2: Quick Order Check
```bash
# Check a specific order by ID
python check_order.py [order-id]

# Example:
python check_order.py 180538d2-3c56-4bba-bbb3-3bf4dc4f6017
```

### Method 3: Direct BigQuery Queries
```bash
# View recent orders
bq query --use_legacy_sql=false "SELECT * FROM trial-genai.demo_adk.order ORDER BY order_id DESC LIMIT 5"

# Check order statistics
bq query --use_legacy_sql=false "SELECT COUNT(*) as total_orders, AVG(total_price) as avg_order_value FROM trial-genai.demo_adk.order"

# Verify specific order
bq query --use_legacy_sql=false "SELECT * FROM trial-genai.demo_adk.order WHERE order_id = 'your-order-id'"
```

### Method 4: Agent Function Testing
```bash
# Test individual functions
python test_bigquery_functions.py

# This tests:
# - get_menu() - Menu retrieval
# - save_order() - Order saving  
# - get_order() - Order retrieval
# - get_promo() - Promotion lookup
# - process_payment() - Payment processing
```

### Verification Checklist ✅

When verifying order entry, check that:

- **Order ID**: UUID format, unique identifier
- **Customer Name**: Stored exactly as provided
- **Items**: Valid JSON array with name, price, quantity
- **Total Price**: Matches calculated sum of items
- **Status**: Appropriate status (pending, completed, etc.)
- **Data Types**: Numbers stored as FLOAT64, strings as STRING
- **No Data Loss**: All original data preserved
- **JSON Integrity**: Items field parses correctly

### Troubleshooting Order Issues

**Order not found:**
- Check order ID format (should be UUID)
- Verify BigQuery dataset/table names match configuration
- Ensure proper authentication to BigQuery

**Data mismatch:**
- Check column names match between code and BigQuery schema
- Verify data types (total_price vs total_amount)
- Ensure JSON formatting is correct for items field

**Performance issues:**
- Monitor BigQuery query costs and usage
- Use indexed columns for faster lookups
- Consider partitioning large order tables

---

**Built with ❤️ using Google Agent Development Kit**
```

### Method 2: Command Line Testing

```bash
# Run unit tests
pytest -v

# Run workflow tests (displays all test prompts)
python test_workflow.py

# Test with fallback mode (no ADK required)
FORCE_LOCAL_ADK_FALLBACK=1 python test_workflow.py
```

### Method 3: Terminal Interface

```bash
# Interactive terminal chat
adk run

# API server mode
adk api_server --port 8003
```

## 🛠️ Development

### Project Structure
```
self-order-agent/
├── agent.py              # Main agent definition and tools
├── __init__.py           # Package initialization  
├── self_order_agent.py   # Compatibility shim
├── test_agent.py         # Unit tests
├── test_workflow.py      # Workflow test prompts
├── requirements.txt      # Python dependencies
├── pyproject.toml       # Project metadata
├── .env                 # Environment variables (create this)
├── README.md            # This file
└── data/                # Sample data files
    ├── menu.csv
    ├── orders.csv
    ├── orders.json
    └── promos.csv
```

### Key Features
- **Automatic .env loading**: Environment variables loaded automatically
- **Fallback mode**: Works without ADK for local development/testing
- **Modern ADK patterns**: Uses latest Agent class and function tools
- **Error handling**: Graceful handling of missing dependencies
- **Comprehensive testing**: Unit tests and workflow test prompts

### Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
adk web --port 8001
```

**ADK import errors:**
```bash
# Force local fallback mode
export FORCE_LOCAL_ADK_FALLBACK=1
python test_workflow.py
```

**BigQuery permissions:**
```bash
# Authenticate with Google Cloud
gcloud auth application-default login
```

## 📚 Next Steps

- **Extend functionality**: Add more tools like inventory management, delivery tracking
- **Deploy to production**: Use Cloud Run or Vertex AI Agent Engine
- **Add memory**: Implement conversation history and user preferences  
- **Enhance security**: Add input validation and rate limiting
- **Monitor performance**: Integrate with Google Cloud Trace and Logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Samples](https://github.com/google/adk-samples)
- [Gemini API Documentation](https://ai.google.dev/)
- [Google Cloud BigQuery](https://cloud.google.com/bigquery/docs)

---

**Built with ❤️ using Google Agent Development Kit**