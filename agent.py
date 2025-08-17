"""Self-order agent for the ADK.

This file contains all the agents for the self-ordering system.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import uuid
import warnings
from datetime import datetime
from typing import Optional
from google.cloud import bigquery

# Try to import the real ADK classes. Only swallow import-related errors so
# runtime exceptions raised by ADK code don't get masked. Provide an env var
# `FORCE_LOCAL_ADK_FALLBACK=1` to force using the local fallback (useful for
# testing).
_ADK_AVAILABLE = False
_ADK_IMPORT_EXCEPTION = None
try:
    if os.getenv("FORCE_LOCAL_ADK_FALLBACK", "").lower() in ("1", "true", "yes"):
        # Allow tests or developers to force the fallback
        raise ModuleNotFoundError("Forced local ADK fallback via env var")

    # Use the modern ADK Agent class (recommended approach)
    from google.adk.agents import Agent
    _ADK_AVAILABLE = True
except (ImportError, ModuleNotFoundError) as e:
    _ADK_AVAILABLE = False
    _ADK_IMPORT_EXCEPTION = e
    warnings.warn(
        "ADK libraries not available; using local fallback agents. "
        f"See https://google.github.io/adk-docs/ for installation. Reason: {e}",
        ImportWarning,
    )

# Load .env from the repository root if present so env-based config like
# PROJECT_ID or FORCE_LOCAL_ADK_FALLBACK works during local development.
_ROOT = Path(__file__).parent
dot_env = _ROOT / ".env"
if dot_env.exists():
    load_dotenv(dot_env)

# Customer information collection through conversation

def collect_customer_info(name: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None) -> dict:
    """Collect and store customer information during conversation"""
    customer_info = {
        "name": name,
        "email": email, 
        "phone": phone,
        "timestamp": datetime.now().isoformat(),
        "session_id": str(uuid.uuid4())
    }
    
    # Filter out None values
    customer_info = {k: v for k, v in customer_info.items() if v is not None}
    
    return {
        "status": "SUCCESS",
        "customer_info": customer_info,
        "message": f"Thank you {name}! I've collected your information for this order."
    }

def get_customer_order_history(customer_name: Optional[str] = None, customer_email: Optional[str] = None) -> list[dict]:
    """Get customer's previous orders based on name or email"""
    try:
        client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
        
        if customer_email:
            # Search by email in customer_name field (if email was used as identifier)
            query = f"""
                SELECT order_id, customer_name, items, total_price, status
                FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_ORDERS_TABLE}`
                WHERE LOWER(customer_name) LIKE LOWER(@customer_email)
                ORDER BY order_id DESC
                LIMIT 10
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("customer_email", "STRING", f"%{customer_email}%"),
                ]
            )
        elif customer_name:
            # Search by name
            query = f"""
                SELECT order_id, customer_name, items, total_price, status  
                FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_ORDERS_TABLE}`
                WHERE LOWER(customer_name) LIKE LOWER(@customer_name)
                ORDER BY order_id DESC
                LIMIT 10
            """
            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("customer_name", "STRING", f"%{customer_name}%"),
                ]
            )
        else:
            return [{"message": "Please provide either customer name or email to retrieve order history"}]

        query_job = client.query(query, job_config=job_config)
        rows = query_job.result()
        order_history = [dict(row) for row in rows]
        
        if not order_history:
            return [{"message": f"No previous orders found for {customer_name or customer_email}"}]
            
        return order_history
        
    except Exception as e:
        return [{"error": f"Failed to retrieve order history: {str(e)}"}]

def save_order_for_customer(customer_name: str, customer_email: Optional[str] = None, items: str = "", total_price: float = 0.0) -> dict:
    """Save an order with customer information collected during conversation"""
    try:
        # Create customer identifier (prefer email, fallback to name)
        customer_identifier = customer_email if customer_email else customer_name
        
        order_data = {
            'order_id': str(uuid.uuid4()),
            'customer_name': customer_identifier,
            'items': items,
            'total_price': float(total_price),
            'status': 'pending'
        }
        
        client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
        table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_ORDERS_TABLE}"
        
        errors = client.insert_rows_json(table_id, [order_data])
        if errors == []:
            return {
                "status": "SUCCESS", 
                "order_id": order_data['order_id'],
                "customer": customer_identifier,
                "message": f"Order saved successfully for {customer_name}!"
            }
        else:
            return {"status": "FAILURE", "errors": errors}
    except Exception as e:
        return {"status": "FAILURE", "error": str(e)}


if not _ADK_AVAILABLE:
    class Agent:
        """Minimal local fallback agent used when ADK is unavailable."""

        def __init__(
            self,
            name: str,
            model: str = "gemini-2.5-flash",
            description: str = "",
            instruction: str = "",
            tools: list = None,
        ):
            self.name = name
            self.model = model
            self.description = description
            self.instruction = instruction
            self.tools = {}
            for tool in tools or []:
                if callable(tool):
                    self.tools[tool.__name__] = tool
                else:
                    self.tools[getattr(tool, 'name', str(tool))] = tool

        def respond(self, prompt: str) -> str:
            """Return a deterministic mock response for quick local tests."""
            return (
                f"[mock:{self.name}] I don't have ADK available. "
                f"You asked: {prompt}"
            )

        def info(self) -> dict:
            return {
                "model": self.model,
                "name": self.name,
                "description": self.description,
                "instruction": self.instruction,
            }


# Storage Agent

PROJECT_ID = os.getenv("PROJECT_ID")
GOOGLE_CLOUD_REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
BIGQUERY_DATASET = os.getenv("BIGQUERY_DATASET", "demo_adk")
BIGQUERY_ORDERS_TABLE = "order"  # Changed from "orders" to match your table
BIGQUERY_MENU_TABLE = "menu"
BIGQUERY_PROMOS_TABLE = "promos"


def save_order(order: dict) -> dict:
    """Save an order to BigQuery."""
    try:
        client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
        table_id = f"{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_ORDERS_TABLE}"
        
        # Ensure the order data matches the table schema
        formatted_order = {
            'order_id': order.get('order_id', str(uuid.uuid4())),
            'customer_name': order.get('customer_name', 'Anonymous'),
            'items': order.get('items', ''),
            'total_price': float(order.get('total_price', order.get('total_amount', 0.0))),
            'status': order.get('status', 'pending')
        }

        errors = client.insert_rows_json(table_id, [formatted_order])
        if errors == []:
            return {"status": "SUCCESS", "order_id": formatted_order['order_id']}
        else:
            return {"status": "FAILURE", "errors": errors}
    except Exception as e:
        return {"status": "FAILURE", "error": str(e)}


def get_order(order_id: str) -> dict:
    """Get an order from BigQuery."""
    client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_ORDERS_TABLE}`
        WHERE order_id = @order_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("order_id", "STRING", order_id),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    rows = query_job.result()
    for row in rows:
        return dict(row)
    return {}


def get_menu() -> list[dict]:
    """Get the menu from BigQuery."""
    try:
        client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
        query = f"""
            SELECT name, CAST(price AS FLOAT64) as price
            FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_MENU_TABLE}`
            ORDER BY name
        """
        query_job = client.query(query)
        rows = query_job.result()
        menu_items = [dict(row) for row in rows]
        
        if not menu_items:
            return [{"message": "No menu items found. Menu may be empty."}]
        
        return menu_items
    except Exception as e:
        return [{"error": f"Failed to retrieve menu: {str(e)}"}]


def get_promo(promo_code: str) -> dict:
    """Get a promo from BigQuery."""
    client = bigquery.Client(project=PROJECT_ID, location=GOOGLE_CLOUD_REGION)
    query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_PROMOS_TABLE}`
        WHERE promo_code = @promo_code
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("promo_code", "STRING", promo_code),
        ]
    )
    query_job = client.query(query, job_config=job_config)
    rows = query_job.result()
    for row in rows:
        return dict(row)
    return {}


# Payment processing function

def process_payment(amount: float, currency: str = "USD") -> dict:
    """Process a payment."""
    return {"transaction_id": str(uuid.uuid4()), "status": "SUCCESS"}


# Root Agent - A helpful assistant for self-ordering food

root_agent = Agent(
    name="root_agent", 
    model="gemini-2.5-flash",
    description="A helpful assistant for self-ordering food.",
    instruction=(
        "You are a helpful assistant for ordering food. You can help customers "
        "browse the menu, apply promotions, process payments, and place orders. "
        "IMPORTANT: Always greet customers warmly and ask for their name at the beginning "
        "of the conversation. You can also collect their email or phone number for order "
        "tracking and future promotions. Use this information to personalize their experience. "
        "If they're a returning customer, you can look up their order history using "
        "get_customer_order_history. When placing orders, use save_order_for_customer "
        "to associate the order with their information. Be conversational and natural - "
        "collect customer information through friendly dialogue rather than formal forms."
    ),
    tools=[
        save_order,
        save_order_for_customer,
        get_order,
        get_menu,
        get_promo,
        process_payment,
        collect_customer_info,
        get_customer_order_history,
    ],
)

__all__ = ["root_agent"]