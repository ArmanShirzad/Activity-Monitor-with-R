# Deployment Guide - Marketplace Edition

This guide covers deploying the Activity Monitor platform to various marketplaces and cloud providers.

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Marketplace Submission](#marketplace-submission)
6. [API Configuration](#api-configuration)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Local Setup

```bash
# Clone repository
git clone https://github.com/yourusername/activity-monitor-marketplace
cd activity-monitor-marketplace

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp env.example .env
# Edit .env with your API keys

# Frontend setup
cd ../frontend
npm install

# Start services
docker-compose up -d
```

## 🔧 Local Development

### Backend

```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run dev
```

## 🐳 Docker Deployment

### Single Command Deployment

```bash
docker-compose up -d
```

### Individual Services

```bash
# Backend only
docker build -t activitymonitor-backend ./backend
docker run -p 8000:8000 activitymonitor-backend

# Frontend only
docker build -t activitymonitor-frontend ./frontend
docker run -p 3000:3000 activitymonitor-frontend
```

## ☁️ Cloud Deployment

### AWS (Elastic Beanstalk)

```bash
# Install EB CLI
pip install awsebcli

# Initialize
cd backend
eb init -p python-3.11 activitymonitor

# Create environment
eb create activitymonitor-env

# Deploy
eb deploy
```

### AWS (Lambda - Serverless)

```bash
# Package for Lambda
cd backend
zip -r lambda-package.zip . -x "*.git*" "*venv*"

# Deploy with SAM or Serverless Framework
```

### Google Cloud Platform (Cloud Run)

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/activitymonitor

# Deploy
gcloud run deploy activitymonitor \
  --image gcr.io/PROJECT_ID/activitymonitor \
  --platform managed \
  --region us-central1
```

### Azure (App Service)

```bash
# Login
az login

# Create resource group
az group create --name activitymonitor-rg --location eastus

# Create app service
az webapp up --name activitymonitor --resource-group activitymonitor-rg --runtime "PYTHON:3.11"
```

## 📱 Marketplace Submission

### Apple App Store (iOS)

1. **Prepare App**
   - Create iOS app using React Native or Ionic
   - Implement HealthKit integration
   - Add App Store assets (screenshots, icons)

2. **Required Documents**
   - App icon (1024x1024px)
   - Screenshots (multiple device sizes)
   - Privacy policy URL
   - App description and keywords

3. **Submission**
   - Use Xcode to build and upload
   - Complete App Store Connect form
   - Submit for review

**Pricing**: $99/year developer program

### Google Play Store (Android)

1. **Prepare App**
   - Build Android APK/AAB
   - Implement Google Fit integration
   - Add required permissions

2. **Required Assets**
   - High-res icon (512x512px)
   - Feature graphic (1024x500px)
   - Screenshots (phone and tablet)
   - Promo video (optional)

3. **Submission**
   - Upload via Google Play Console
   - Complete store listing
   - Set up pricing and distribution
   - Submit for review

**Pricing**: $25 one-time fee

### Garmin Connect IQ Store

1. **Develop App**
   - Use Connect IQ SDK
   - Create app or watch face
   - Test on simulator and devices

2. **Submission**
   - Package app with `bar` file
   - Submit via Connect IQ Manager
   - Complete app metadata
   - Wait for review (2-5 days)

**Pricing**: Free to develop and publish

### Fitbit App Gallery (Legacy)

1. **Note**: Limited support on newer devices
2. **Use Fitbit Web API** for data integration
3. **Publish as web dashboard** instead

## 🔑 API Configuration

### Obtain API Keys

#### Fitbit

1. Go to https://dev.fitbit.com
2. Create new app
3. Get Client ID and Client Secret
4. Configure OAuth 2.0 redirect URLs

#### Garmin

1. Register at https://developer.garmin.com
2. Create new app
3. Get Consumer Key and Consumer Secret
4. Configure OAuth 1.0 credentials

#### Google Fit

1. Go to Google Cloud Console
2. Create new project
3. Enable Google Fit API
4. Create OAuth 2.0 credentials

#### Strava

1. Go to https://www.strava.com/settings/api
2. Create new application
3. Get Client ID and Client Secret

### Environment Variables

Create `backend/.env`:

```env
# Fitbit
FITBIT_CLIENT_ID=your_client_id
FITBIT_CLIENT_SECRET=your_secret

# Garmin
GARMIN_CONSUMER_KEY=your_key
GARMIN_CONSUMER_SECRET=your_secret

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/activitymonitor

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your_secret_key_here
```

## 🔐 Security & Compliance

### GDPR Compliance

- ✅ Data encryption at rest
- ✅ Data encryption in transit (HTTPS)
- ✅ User consent management
- ✅ Right to deletion
- ✅ Data export functionality
- ✅ Privacy policy required

### HIPAA Compliance (Enterprise)

- ✅ Encrypted database
- ✅ Audit logging
- ✅ Access controls
- ✅ Business Associate Agreement

### Security Best Practices

```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Never commit secrets
SECRET_KEY = os.getenv('SECRET_KEY')

# Use HTTPS everywhere
# Implement rate limiting
# Add authentication middleware
```

## 📊 Monitoring & Analytics

### Application Monitoring

```bash
# Add Sentry for error tracking
pip install sentry-sdk

# Add to main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### Analytics

- Google Analytics
- Mixpanel
- Amplitude

## 💰 Monetization Setup

### Subscription Management

Implement with:
- Stripe for payments
- PayPal for payments
- In-app purchases (App Store/Play Store)

### Pricing Tiers

```python
TIERS = {
    'free': {
        'features': ['basic_stats', 'daily_summary'],
        'api_limit': 100
    },
    'premium': {
        'features': ['all_free', 'advanced_analytics', 'historical_data'],
        'api_limit': 1000
    },
    'pro': {
        'features': ['all_premium', 'ai_insights', 'api_access'],
        'api_limit': 10000
    }
}
```

## 🧪 Testing

### Run Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [AWS Documentation](https://docs.aws.amazon.com/)
- [Google Cloud Documentation](https://cloud.google.com/docs)

## 🆘 Support

For issues or questions:
- GitHub Issues: Report bugs
- Email: support@activitymonitor.dev
- Documentation: https://docs.activitymonitor.dev

