#!/bin/bash

# Google Cloud Run Environment Variable Management Script
# Usage: ./manage-env.sh [PROJECT_ID] [REGION] [ACTION] [KEY=VALUE]

set -e

PROJECT_ID=${1:-"your-project-id"}
REGION=${2:-"us-central1"}
ACTION=${3:-"list"}
SERVICE_NAME="self-order-agent"

echo "🔑 Cloud Run Environment Variable Manager"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo "Action: $ACTION"

case $ACTION in
    "list")
        echo ""
        echo "📋 Current Environment Variables:"
        gcloud run services describe $SERVICE_NAME \
            --platform managed \
            --region $REGION \
            --format 'table(spec.template.spec.template.spec.containers[0].env[].name:label="NAME",spec.template.spec.template.spec.containers[0].env[].value:label="VALUE")'
        ;;
    
    "set")
        if [ -z "$4" ]; then
            echo "❌ Usage: $0 $PROJECT_ID $REGION set KEY=VALUE"
            exit 1
        fi
        
        ENV_VAR="$4"
        echo ""
        echo "🔧 Setting environment variable: $ENV_VAR"
        gcloud run services update $SERVICE_NAME \
            --platform managed \
            --region $REGION \
            --set-env-vars "$ENV_VAR"
        echo "✅ Environment variable updated successfully!"
        ;;
    
    "unset")
        if [ -z "$4" ]; then
            echo "❌ Usage: $0 $PROJECT_ID $REGION unset KEY"
            exit 1
        fi
        
        ENV_KEY="$4"
        echo ""
        echo "🗑️  Removing environment variable: $ENV_KEY"
        gcloud run services update $SERVICE_NAME \
            --platform managed \
            --region $REGION \
            --remove-env-vars "$ENV_KEY"
        echo "✅ Environment variable removed successfully!"
        ;;
    
    "setup-secrets")
        echo ""
        echo "🔐 Setting up Google Secret Manager for production..."
        
        # Create secrets for sensitive data
        echo "Creating secrets (you'll be prompted for values)..."
        
        echo "Enter your Google API Key:"
        read -s GOOGLE_API_KEY
        echo "$GOOGLE_API_KEY" | gcloud secrets create google-api-key --data-file=-
        
        # Update Cloud Run to use secrets
        echo ""
        echo "🔗 Configuring Cloud Run to use secrets..."
        gcloud run services update $SERVICE_NAME \
            --platform managed \
            --region $REGION \
            --set-secrets "GOOGLE_API_KEY=google-api-key:latest"
        
        echo "✅ Secret Manager setup complete!"
        echo "🔐 Your API key is now securely stored and automatically injected into your service."
        ;;
    
    "production-setup")
        echo ""
        echo "🚀 Setting up production environment variables..."
        
        # Set all required production environment variables
        gcloud run services update $SERVICE_NAME \
            --platform managed \
            --region $REGION \
            --set-env-vars \
                "PYTHONPATH=/app" \
                "PYTHONUNBUFFERED=1" \
                "PROJECT_ID=$PROJECT_ID" \
                "BIGQUERY_DATASET=self_order_agent" \
                "GOOGLE_CLOUD_REGION=asia-southeast2" \
                "GOOGLE_GENAI_USE_VERTEXAI=FALSE"
        
        echo "✅ Production environment variables configured!"
        echo "🌏 BigQuery region set to: asia-southeast2 (Jakarta)"
        echo "📱 Cloud Run region: $REGION"
        echo ""
        echo "🔑 Next steps:"
        echo "1. Run: $0 $PROJECT_ID $REGION setup-secrets"
        echo "2. Or manually set: $0 $PROJECT_ID $REGION set GOOGLE_API_KEY=your-key"
        ;;
    
    *)
        echo ""
        echo "📖 Usage: $0 [PROJECT_ID] [REGION] [ACTION] [ARGS...]"
        echo ""
        echo "Available actions:"
        echo "  list              - Show current environment variables"
        echo "  set KEY=VALUE     - Set an environment variable"
        echo "  unset KEY         - Remove an environment variable"
        echo "  setup-secrets     - Configure Google Secret Manager (recommended)"
        echo "  production-setup  - Set all required production variables"
        echo ""
        echo "Examples:"
        echo "  $0 my-project us-central1 list"
        echo "  $0 my-project us-central1 set GOOGLE_API_KEY=abc123"
        echo "  $0 my-project us-central1 setup-secrets"
        echo "  $0 my-project us-central1 production-setup"
        ;;
esac
