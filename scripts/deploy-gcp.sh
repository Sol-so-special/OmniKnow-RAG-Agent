#!/bin/bash
# GCP Deployment Script

set -e

PROJECT_ID="YOUR_PROJECT_ID"
REGION="us-central1"
CLUSTER_NAME="omniknow-cluster"

echo "🚀 Deploying to GCP..."

# 1. Build and push to GCR
echo "📦 Building Docker image..."
cd backend
docker build -t gcr.io/$PROJECT_ID/omniknow-backend:latest .

echo "⬆️  Pushing to GCR..."
docker push gcr.io/$PROJECT_ID/omniknow-backend:latest

# 2. Update K8s deployment
echo "☸️  Deploying to GKE..."
kubectl set image deployment/omniknow-backend \
  backend=gcr.io/$PROJECT_ID/omniknow-backend:latest \
  -n omniknow

echo "✅ Deployment complete!"
kubectl get svc omniknow-backend -n omniknow
