# Quick Start Guide - Activity Monitor Marketplace Edition

Get started in 5 minutes! 🚀

---

## Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Docker** (optional) - [Download](https://www.docker.com/)

---

## Option 1: Local Development (Quickest)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/activity-monitor-marketplace.git
cd activity-monitor-marketplace
```

### Step 2: Start Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn src.main:app --reload
```

Backend will be available at: http://localhost:8000

API docs: http://localhost:8000/docs

### Step 3: Start Frontend

```bash
# In new terminal
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## Option 2: Docker (Recommended)

### Start Everything

```bash
# In project root
docker-compose up -d
```

This starts:
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- Backend API (port 8000)
- Frontend dashboard (port 3000)

### Stop Everything

```bash
docker-compose down
```

---

## 🔑 Get API Keys (Optional for Testing)

To use real device integrations:

### Fitbit

1. Go to https://dev.fitbit.com
2. Register app
3. Get Client ID & Secret

### Garmin

1. Go to https://developer.garmin.com
2. Register app
3. Get Consumer Key & Secret

### Add to Environment

```bash
cd backend
cp env.example .env
# Edit .env with your keys
```

---

## 🧪 Test With Sample Data

You can test without API keys using the original data:

```bash
cd backend
python

>>> import pandas as pd
>>> from src.core.activity_analyzer import ActivityAnalyzer
>>> 
>>> # Load your original data
>>> data = pd.read_csv('activity.csv')
>>> analyzer = ActivityAnalyzer(data)
>>> 
>>> # Run analysis
>>> results = analyzer.generate_summary_report()
>>> print(results)
```

---

## 📱 Test API

### Health Check

```bash
curl http://localhost:8000/health
```

### Get Supported Platforms

```bash
curl http://localhost:8000/api/v1/platforms
```

### Analyze Activity

```bash
curl -X POST http://localhost:8000/api/v1/activity/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "platform": "manual",
    "start_date": "2022-10-01",
    "end_date": "2022-11-30"
  }'
```

---

## 🎨 View Dashboard

1. Open http://localhost:3000
2. Select a platform (currently shows UI)
3. Connect with API credentials
4. View analytics dashboard

---

## 🐛 Troubleshooting

### Port Already in Use

**Backend (8000)**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Frontend (3000)**
```bash
# Find process
lsof -i :3000

# Kill process
kill -9 <PID>
```

### Docker Issues

```bash
# Clean up
docker-compose down -v

# Rebuild
docker-compose build --no-cache

# Restart
docker-compose up -d
```

### Module Not Found

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

---

## 📚 Next Steps

1. **Read** `DEPLOYMENT.md` for cloud deployment
2. **Read** `README-MARKETPLACE.md` for marketplace submission
3. **Read** `PROJECT_SUMMARY.md` for full feature list

---

## 🆘 Need Help?

- **Documentation**: See DEPLOYMENT.md
- **Issues**: Check GitHub Issues
- **Email**: support@activitymonitor.dev

---

**You're all set! Start building your marketplace-ready activity monitor! 🎉**

