# DEPLOYMENT GUIDE

## Overview

**OmniKnow RAG Agent** is a production-ready RAG system that suports local hosting and multi-cloud deployment. This guide covers local development, AWS (EKS), and GCP (Cloud Run/GKE) deployments.

---

## Prerequisites

### Required Tools

- Docker & Docker Compose
- Python 3.11+
- kubectl (for Kubernetes deployments)
- AWS CLI (for AWS deployment)
- gcloud CLI (for GCP deployment)
- Git

### Required API Keys

- **Gemini API Key** (Google AI)
- **Pinecone API Key** (cloud vector store)
- **Google Search API Key** + **CSE ID** (optional, for live search)

---

## Local Development

### 1. Clone Repository

```bash
git clone https://github.com/Sol-so-special/OmniKnow-RAG-Agent
cd OmniKnow-RAG-Agent
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```bash
GEMINI_API_KEY=your-actual-key
GOOGLE_SEARCH_API_KEY=your-key
GOOGLE_CSE_ID=your-cse-id
```

### 3. Start Services

```bash
docker-compose up --build
```

**Access Points:**

- Frontend: <http://localhost:8501>
- Backend API: <http://localhost:8000>
- API Docs: <http://localhost:8000/docs>

### 4. Run Tests

```bash
python tests/test_api.py
```

---

## AWS Deployment (EKS)

### Architecture

- **Container Registry:** AWS ECR
- **Orchestration:** Amazon EKS
- **Storage:** S3 (file uploads)
- **Vector Store:** Pinecone (cloud)

### Prerequisites

```bash
# Configure AWS credentials
aws configure

# Install eksctl
brew install eksctl  # macOS
# or download from: https://eksctl.io
```

### 1. Create EKS Cluster

```bash
eksctl create cluster \
  --name omniknow-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2
```

### 2. Create S3 Bucket

```bash
aws s3 mb s3://omniknow-uploads --region us-east-1
```

### 3. Create ECR Repository

```bash
aws ecr create-repository \
  --repository-name omniknow-backend \
  --region us-east-1
```

### 4. Update ConfigMap (Optional)

If you changed the bucket name, edit `kubernetes/configmap.yaml`:

```yaml
S3_BUCKET_NAME: "your-bucket-name"  # Change if needed
```

### 5. Deploy to EKS

```bash
# Create namespace
kubectl apply -f kubernetes/namespace.yaml

# Create secrets dynamically (and NEVER commit secrets.yaml!)
kubectl create secret generic omniknow-secrets -n omniknow \
  --from-literal=GEMINI_API_KEY=your-actual-gemini-key \
  --from-literal=PINECONE_API_KEY=your-actual-pinecone-key \
  --from-literal=GOOGLE_SEARCH_API_KEY=your-google-key \
  --from-literal=GOOGLE_CSE_ID=your-cse-id

# Apply manifests
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml
```

### 6. Verify Deployment

```bash
kubectl get pods -n omniknow
kubectl logs -f deployment/omniknow-backend -n omniknow
kubectl get svc omniknow-backend -n omniknow
```

---

## GCP Deployment (Cloud Run - Serverless)

### Architecture

- **Container Registry:** GCR (Google Container Registry)
- **Compute:** Cloud Run (serverless)
- **Storage:** GCS (optional)
- **Vector Store:** Pinecone (cloud)

### Prerequisites

```bash
# Install gcloud CLI
# Follow: https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login
gcloud config set project omniknow-v2
```

### 1. Enable APIs

```bash
gcloud services enable \
  run.googleapis.com \
  containerregistry.googleapis.com \
  cloudbuild.googleapis.com
```

### 2. Build and Push Image

```bash
cd backend

# Build
docker build -t gcr.io/omniknow-v2/omniknow-backend:latest .

# Configure Docker for GCR
gcloud auth configure-docker

# Push
docker push gcr.io/omniknow-v2/omniknow-backend:latest
```

### 3. Deploy to Cloud Run

```bash
gcloud run deploy omniknow-backend \
  --image gcr.io/omniknow-v2/omniknow-backend:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "ENVIRONMENT=production,VECTOR_STORE_TYPE=pinecone" \
  --set-secrets "GEMINI_API_KEY=gemini-key:latest,PINECONE_API_KEY=pinecone-key:latest"
```

### 4. Setup Secrets (GCP Secret Manager)

```bash
# Create secrets
echo -n "your-gemini-key" | gcloud secrets create gemini-key --data-file=-
echo -n "your-pinecone-key" | gcloud secrets create pinecone-key --data-file=-

# Grant access
gcloud secrets add-iam-policy-binding gemini-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 5. Verify Deployment

```bash
# Get service URL
gcloud run services describe omniknow-backend \
  --region us-central1 \
  --format 'value(status.url)'

# Test
curl https://<SERVICE-URL>/health
```

### 6. Setup CI/CD (GitHub Actions)

1. Create Service Account:

```bash
gcloud iam service-accounts create github-actions \
  --display-name "GitHub Actions"

gcloud projects add-iam-policy-binding omniknow-v2 \
  --member="serviceAccount:github-actions@omniknow-v2.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

2. Generate Key:

```bash
gcloud iam service-accounts keys create key.json \
  --iam-account github-actions@omniknow-v2.iam.gserviceaccount.com
```

3. Add `GCP_SA_KEY` to GitHub Secrets (contents of `key.json`)
4. Push to `main` triggers deployment

---

## GCP Deployment (GKE)

### 1. Create GKE Cluster

```bash
gcloud container clusters create omniknow-cluster \
  --region us-central1 \
  --num-nodes 2 \
  --machine-type n1-standard-2
```

### 2. Deploy

```bash
# Create namespace
kubectl create namespace omniknow

# Create secrets dynamically
kubectl create secret generic omniknow-secrets -n omniknow \
  --from-literal=GEMINI_API_KEY=your-key \
  --from-literal=PINECONE_API_KEY=your-key \
  --from-literal=GOOGLE_SEARCH_API_KEY=your-key \
  --from-literal=GOOGLE_CSE_ID=your-id

# Apply manifests
kubectl apply -f kubernetes-gcp/configmap.yaml
kubectl apply -f kubernetes-gcp/backend-deployment.yaml
kubectl apply -f kubernetes-gcp/backend-service.yaml
```

---

## Environment Variables Reference

### Local (.env)

```bash
ENVIRONMENT=local
VECTOR_STORE_TYPE=chroma
GEMINI_API_KEY=<key>
GOOGLE_SEARCH_API_KEY=<key>
GOOGLE_CSE_ID=<id>
BACKEND_URL=http://localhost:8000
```

### AWS Cloud (.env.cloud)

```bash
ENVIRONMENT=production
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=<key>
GEMINI_API_KEY=<key>
S3_BUCKET_NAME=omniknow-uploads
S3_REGION=us-east-1
```

### GCP Cloud (.env.gcp)

```bash
ENVIRONMENT=production
VECTOR_STORE_TYPE=pinecone
PINECONE_API_KEY=<key>
GEMINI_API_KEY=<key>
GCS_BUCKET_NAME=omniknow-uploads-gcp
GCS_REGION=us-central1
```

---

## Troubleshooting

### Backend Won’t Start

```bash
# Check logs
docker-compose logs backend

# Verify environment
docker-compose exec backend env | grep GEMINI_API_KEY
```

### Kubernetes Pod CrashLoopBackOff

```bash
kubectl describe pod <pod-name> -n omniknow
kubectl logs <pod-name> -n omniknow
```

### Cloud Run Cold Starts

- Increase minimum instances: `--min-instances=1`
- Use CPU always-allocated: `--cpu-boost`

### Vector Store Connection Errors

- Verify Pinecone API key
- Check Pinecone index exists
- Confirm index dimension matches (768 for all-mpnet-base-v2)

---

## Monitoring

### Prometheus Metrics

Available at: `http://<api-endpoint>/metrics`

### Health Check

```bash
curl http://<api-endpoint>/health
```

Response:

```json
{
  "status": "healthy",
  "environment": "production",
  "vector_store": "pinecone"
}
```

---

## Scaling

### AWS EKS & GCP GKE (Kubernetes)

The project uses a **Horizontal Pod Autoscaler (HPA)** that is applied automatically via CI/CD pipelines. The HPA monitors CPU utilization and scales pods between 2-10 replicas based on demand.

**View autoscaler status:**
```bash
kubectl get hpa -n omniknow
kubectl describe hpa omniknow-backend-hpa -n omniknow
```

**How it works:**

- **Target CPU:** 70% utilization
- **Min pods:** 2
- **Max pods:** 10
- **Scale-up:** Immediate when CPU exceeds 70%
- **Scale-down:** Waits 5 minutes before reducing pods (prevents flapping)

### GCP Cloud Run

Cloud Run uses **serverless autoscaling** configured via deployment flags:

```bash
gcloud run services update omniknow-backend \
  --region us-central1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80
```

- Scales to zero when idle (cost-efficient)
- Scales up automatically based on request concurrency

---

## Security Best Practices

1. **Never commit secrets** to Git
2. Use **IAM roles** instead of access keys when possible
3. Enable **VPC networking** for production
4. Implement **rate limiting** at ingress level
5. Use **HTTPS only** with valid certificates
6. Regularly **rotate API keys**
7. Enable **CloudWatch/Stackdriver logging**

---

## Cost Optimization

### AWS

- Use Spot instances for EKS nodes
- Enable S3 Intelligent-Tiering
- Use NAT Gateway only if needed

### GCP Cloud Run

- Use min-instances=0 for non-production environments
- Enable CPU allocation only during request processing
- Set appropriate concurrency limits

### GCP GKE

- Use Preemptible VMs (up to 80% discount)
- Enable cluster autoscaling to scale nodes to zero during low traffic
- Use regional clusters only if high availability is critical

---

## Support

- **Documentation:** See the [`docs/`](../docs/) folder and the [README.md](../README.md)
- **Issues:** GitHub Issues
- **API Docs:** `http://<endpoint>/docs`