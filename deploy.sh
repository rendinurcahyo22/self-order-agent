#!/bin/bash

# Cloud Run Deployment Script for Self-Order Agent
# Usage: ./deploy.sh [PROJECT_ID] [REGION]

set -e

# Configuration
PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
GOOGLE_API_KEY=${3:-""}
BIGQUERY_REGION=${4:-"asia-southeast2"}
SERVICE_NAME="self-order-agent"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

echo "🚀 Deploying Self-Order Agent to Cloud Run"
echo "Project: $PROJECT_ID"
echo "Cloud Run Region: $REGION"
echo "BigQuery Region: $BIGQUERY_REGION"
echo "Service: $SERVICE_NAME"

# Check for cross-region setup
if [[ "$REGION" == "us-"* && "$BIGQUERY_REGION" == "asia-"* ]]; then
    echo "🌏 Cross-region setup detected:"
    echo "   📱 Cloud Run in US for better user latency"
    echo "   📊 BigQuery in Asia for data residency"
    echo "   ⚡ Expected latency: +50-100ms (acceptable for restaurant ordering)"
fi

# Check if API key is provided
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️  No Google API Key provided as third argument."
    echo "   You can set it later using: gcloud run services update $SERVICE_NAME --set-env-vars GOOGLE_API_KEY=your-key"
    echo "   Or use Google Secret Manager (recommended for production)"
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Please install it first:"
    echo "https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if Docker is running
if ! docker info &> /dev/null; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Set the project
echo "📋 Setting gcloud project..."
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    containerregistry.googleapis.com \
    bigquery.googleapis.com \
    secretmanager.googleapis.com

# Build the container image
echo "🏗️  Building container image..."
gcloud builds submit --tag $IMAGE_NAME .

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."

# Prepare environment variables
ENV_VARS="PYTHONPATH=/app,PYTHONUNBUFFERED=1,PROJECT_ID=$PROJECT_ID,BIGQUERY_DATASET=self_order_agent,GOOGLE_CLOUD_REGION=$BIGQUERY_REGION"

# Add Google API key if provided
if [ ! -z "$GOOGLE_API_KEY" ]; then
    ENV_VARS="$ENV_VARS,GOOGLE_API_KEY=$GOOGLE_API_KEY"
    echo "✅ Including Google API Key in deployment"
fi

gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 512Mi \
    --cpu 1 \
    --max-instances 10 \
    --min-instances 0 \
    --concurrency 80 \
    --timeout 300 \
    --set-env-vars="$ENV_VARS"

# Get the service URL
echo "✅ Deployment complete!"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(status.url)')
echo "🌐 Service URL: $SERVICE_URL"

echo ""
echo "🔑 Environment Variable Management:"
echo "Current environment variables:"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format 'value(spec.template.spec.template.spec.containers[0].env[].name,spec.template.spec.template.spec.containers[0].env[].value)' | sed 's/\t/ = /g'

echo ""
echo "💡 To update environment variables later:"
echo "gcloud run services update $SERVICE_NAME --region $REGION --set-env-vars GOOGLE_API_KEY=your-new-key"

echo ""
echo "🔐 For production, consider using Google Secret Manager:"
echo "gcloud secrets create google-api-key --data-file=- <<< 'your-api-key'"
echo "gcloud run services update $SERVICE_NAME --region $REGION --set-secrets GOOGLE_API_KEY=google-api-key:latest"

echo ""
echo "📱 Test your agent:"
echo "curl -X POST $SERVICE_URL/process_payment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"amount\": 25.50, \"currency\": \"USD\", \"payment_method\": \"qris\"}'"

echo ""
echo "🔍 Monitor logs:"
echo "gcloud logs tail /projects/$PROJECT_ID/logs/run.googleapis.com%2Fstdout"

echo ""
echo "📊 View in Console:"
echo "https://console.cloud.google.com/run/detail/$REGION/$SERVICE_NAME/metrics?project=$PROJECT_ID"
