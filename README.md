# Self-Order Agent 🍽️

A production-ready multi-tool AI agent built with Google's Agent Development Kit (ADK) that enables customers to seamlessly order food through natural conversation. The agent handles the complete ordering workflow including menu browsing, order creation, promotion application, **QR code payment processing**, and order management.

## 🎯 Overview

This project demonstrates a **production-ready** conversational AI agent that can:

- **Browse Menus**: Retrieve and display food items from BigQuery database
- **Manage Orders**: Create, save, and retrieve customer orders  
- **Apply Promotions**: Validate and apply discount codes and special offers
- **Process Payments**: Generate **QRIS QR codes** for mobile payments with secure transaction tracking
- **QR Code Display**: Render payment QR codes directly in ADK Web UI with embedded HTML
- **Provide Support**: Answer questions and guide customers through the ordering process

The agent uses Google's Agent Development Kit (ADK) framework with Gemini 2.5 Flash model and integrates with Google Cloud BigQuery for data persistence. **Ready for Cloud Run deployment!**

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
                       │  • generate_qr   │
                       └──────────────────┘
```

The system follows a **single-agent architecture** with multiple tools, including **QR code generation** for seamless mobile payments. The agent generates QRIS-compatible QR codes that display directly in the ADK Web UI using embedded HTML with data URIs.

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
- `qrcode` - QR code generation library
- `Pillow` - Image processing for QR codes

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

## 🚀 Cloud Run Deployment

This project is **production-ready** and can be deployed to Google Cloud Run with a single command.

### Prerequisites for Deployment
- Google Cloud Project with billing enabled
- Docker installed and running
- gcloud CLI installed and authenticated

### One-Command Deployment

```bash
# Deploy to Cloud Run (replace with your project ID and API key)
./deploy.sh YOUR-PROJECT-ID us-central1 YOUR-GOOGLE-API-KEY

# For Jakarta BigQuery with US Cloud Run (cross-region optimization)
./deploy.sh YOUR-PROJECT-ID us-central1 YOUR-GOOGLE-API-KEY asia-southeast2
```

**🌏 Cross-Region Setup (Jakarta BigQuery + US Cloud Run):**
- ✅ **Optimized for Indonesia users**: Cloud Run in US for better global user latency
- ✅ **Data in Jakarta**: BigQuery remains in Asia-Southeast2 for data residency  
- ✅ **Acceptable latency**: +50-100ms for cross-region calls (good for restaurant ordering)
- ✅ **Cost effective**: Minimal egress charges for typical usage

The deployment script will:
1. ✅ Enable required Google Cloud APIs (including Secret Manager)
2. 🏗️ Build the container image using Cloud Build
3. 🚀 Deploy to Cloud Run with optimized settings
4. 🔑 Set environment variables (including BigQuery region)
5. 🌐 Provide the public service URL
6. 📊 Show monitoring and logging commands

### Environment Variable Management

**🔑 Option 1: Deploy with API Key (Quick)**
```bash
# Include API key in deployment command
./deploy.sh my-project us-central1 "your-api-key-here"
```

**🔐 Option 2: Use Google Secret Manager (Recommended for Production)**
```bash
# Deploy first, then set up secure secrets
./deploy.sh my-project us-central1
./manage-env.sh my-project us-central1 setup-secrets
```

**⚙️ Option 3: Manual Environment Variable Management**
```bash
# Deploy then manage variables individually
./deploy.sh my-project us-central1
./manage-env.sh my-project us-central1 set GOOGLE_API_KEY=your-key
./manage-env.sh my-project us-central1 list
```

### Manual Deployment Steps

If you prefer manual deployment:

```bash
# 1. Set your project
gcloud config set project YOUR-PROJECT-ID

# 2. Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com bigquery.googleapis.com secretmanager.googleapis.com

# 3. Build container
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/self-order-agent

# 4. Deploy to Cloud Run with environment variables
gcloud run deploy self-order-agent \
  --image gcr.io/YOUR-PROJECT-ID/self-order-agent \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "PYTHONPATH=/app,PYTHONUNBUFFERED=1,PROJECT_ID=YOUR-PROJECT-ID,BIGQUERY_DATASET=self_order_agent,GOOGLE_API_KEY=YOUR-API-KEY"
```

### Required Environment Variables

Your Cloud Run service needs these environment variables:

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `GOOGLE_API_KEY` | Google AI Studio API Key | ✅ Yes | `AIzaSyC...` |
| `PROJECT_ID` | Google Cloud Project ID | ✅ Yes | `my-project-123` |
| `BIGQUERY_DATASET` | BigQuery dataset name | ✅ Yes | `self_order_agent` |
| `GOOGLE_CLOUD_REGION` | BigQuery region | ✅ Yes | `asia-southeast2` |
| `PYTHONPATH` | Python import path | ✅ Yes | `/app` |
| `PYTHONUNBUFFERED` | Python output buffering | ✅ Yes | `1` |
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI instead | ❌ No | `TRUE` |

### Security Best Practices

**🔐 For Production (Recommended):**
Use Google Secret Manager to store sensitive data:
```bash
# Create secret
echo "your-api-key" | gcloud secrets create google-api-key --data-file=-

# Update service to use secret
gcloud run services update self-order-agent \
  --region us-central1 \
  --set-secrets "GOOGLE_API_KEY=google-api-key:latest"
```

**⚠️ Environment Variable Security:**
- ❌ **Never commit API keys** to your repository
- ✅ **Use Secret Manager** for production deployments
- ✅ **Rotate API keys** regularly
- ✅ **Use least-privilege** IAM roles
- ✅ **Enable authentication** for production services

### Production Configuration

The deployment includes:
- **Auto-scaling**: 0 to 10 instances based on traffic
- **Resource limits**: 1 CPU, 512Mi memory per instance
- **Health checks**: HTTP health endpoints for reliability
- **Environment**: Optimized Python 3.12 container
- **Security**: Non-root user execution

### Testing Your Deployment

Once deployed, test your Cloud Run service:

```bash
# Get your service URL
SERVICE_URL=$(gcloud run services describe self-order-agent --platform managed --region us-central1 --format 'value(status.url)')

# Test QR code generation
curl -X POST $SERVICE_URL/process_payment \
  -H 'Content-Type: application/json' \
  -d '{"amount": 25.50, "currency": "USD", "payment_method": "qris"}'
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

#### 💳 Payment & QR Code Tests
```
Process payment for $25.50
I want to pay with QRIS for $15.75
Generate QR code for my payment
Process payment using mobile payment
Pay $30 with QR code
I'd like to pay via mobile banking
```

#### 📱 QR Code Display Tests
```
Show me the QR code for payment
Can you display the payment QR code?
I need to scan the QR code to pay
Generate QR for $25.50 payment
How do I pay using QR code?
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
├── 📄 Core Application
│   ├── agent.py              # Main agent with QR code generation
│   ├── __init__.py           # Package initialization  
│   └── requirements.txt      # Python dependencies
│
├── ⚙️ Configuration  
│   ├── pyproject.toml        # Project metadata & ADK entry point
│   ├── .env                  # Environment variables (create this)
│   └── .env.example          # Environment template
│
├── 🚢 Deployment
│   ├── Dockerfile            # Optimized container configuration
│   ├── cloudrun.yaml         # Cloud Run service specification
│   ├── deploy.sh             # One-command deployment script
│   └── .dockerignore         # Docker build exclusions
│
├── 📊 Data
│   └── data/                 # Sample data files
│       ├── menu.csv          # Restaurant menu items
│       ├── orders.csv        # Order templates  
│       └── promos.csv        # Available promotions
│
└── 📚 Documentation
    └── README.md             # This comprehensive guide
```

### Key Features
- **🎯 Production Ready**: Optimized for Cloud Run deployment
- **📱 QR Code Generation**: QRIS-compatible payment QR codes
- **🖥️ ADK Web UI Compatible**: QR codes display directly in web interface
- **🔧 Auto Environment Loading**: Environment variables loaded automatically
- **🔄 Fallback Mode**: Works without ADK for local development/testing
- **🏆 Modern ADK Patterns**: Uses latest Agent class and function tools
- **⚡ Error Handling**: Graceful handling of missing dependencies
- **🧪 Container Ready**: Dockerfile optimized for production deployment

### Troubleshooting

**Port already in use:**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
adk web --port 8001
```

**QR code generation errors:**
```bash
# Ensure dependencies are installed in your environment
pip install qrcode Pillow

# Test QR generation directly
python -c "import qrcode; print('QR code library working!')"
```

**ADK import errors:**
```bash
# Force local fallback mode
export FORCE_LOCAL_ADK_FALLBACK=1
python -c "from agent import process_payment; print('Agent working!')"
```

**BigQuery permissions:**
```bash
# Authenticate with Google Cloud
gcloud auth application-default login
```

**Cloud Run deployment issues:**
```bash
# Check Docker is running
docker info

# Verify gcloud authentication
gcloud auth list

# Check project permissions
gcloud projects get-iam-policy YOUR-PROJECT-ID
```

## 📚 Next Steps

### 🎯 Production Enhancements
- **🔐 Enhanced Security**: Add input validation, rate limiting, and API authentication
- **📊 Advanced Analytics**: Integrate with Google Cloud Monitoring and Logging
- **🚀 Auto-scaling**: Configure Cloud Run for high-traffic scenarios
- **🌍 Multi-region**: Deploy across multiple regions for global availability

### 🔧 Feature Extensions  
- **📦 Inventory Management**: Real-time stock tracking and availability updates
- **🚚 Delivery Tracking**: Integration with delivery services and GPS tracking
- **💰 Payment Gateways**: Support for multiple payment processors beyond QRIS
- **🎨 Custom Branding**: White-label solution for different restaurants

### 🧠 AI Improvements
- **💭 Memory & Context**: Implement conversation history and user preferences  
- **🤖 Multi-language**: Support for multiple languages and localization
- **📈 Recommendations**: AI-powered menu recommendations based on user behavior
- **📱 Voice Integration**: Voice ordering capabilities for accessibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Resources

### 📖 Documentation
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Python Samples](https://github.com/google/adk-samples)
- [Gemini API Documentation](https://ai.google.dev/)
- [Google Cloud BigQuery](https://cloud.google.com/bigquery/docs)

### ☁️ Deployment & Infrastructure  
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Container Registry](https://cloud.google.com/container-registry/docs)

### 📱 QR Code & Payments
- [QR Code Python Library](https://pypi.org/project/qrcode/)
- [QRIS Payment Standard](https://www.bi.go.id/qris/)
- [Payment Gateway Integration](https://developers.google.com/pay)

---

**🚀 Ready for production deployment with QR code payments!**  
**Built with ❤️ using Google Agent Development Kit**