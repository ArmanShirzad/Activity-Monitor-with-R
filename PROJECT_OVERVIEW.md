# Activity Monitor Project

## What This Project Is

A production-ready platform that connects multiple fitness devices and provides statistical analysis of your activity data. You can:
1. Connect your Fitbit, Garmin, Apple Health, or Google Fit account
2. View your activity data in one unified dashboard
3. Get statistical insights and visualizations of your fitness patterns
4. Deploy locally with Docker or to AWS/Cloud

## What You Get

A complete web application with:
- **Backend API** (FastAPI/Python) - Handles data from fitness platforms
- **Frontend Dashboard** (React) - Beautiful UI for viewing your stats
- **Database** (PostgreSQL) - Stores your activity history
- **Cache** (Redis) - Fast data retrieval
- **Statistical Analysis** - Same R-based algorithms in Python

## Simple Flow

```
Your Fitness Device (Fitbit/Garmin/etc.)
    ↓
Activity Monitor Platform
    ↓
Statistical Analysis & Visualization
    ↓
Beautiful Dashboard (Web UI)
    ↓
You understand your fitness patterns
```

## Quick Start (3 Commands)

```bash
# 1. Start all services with Docker
docker compose up -d

# 2. Visit the dashboard
# Open http://localhost:3000 in your browser

# 3. Connect your fitness platform
# Click on Fitbit, Garmin, or other platform to connect
```

That's it. You get a full analytics dashboard with statistical insights about your activity patterns.

## What This Solves

- You have data from multiple fitness devices.
- You want to see all your data in one place.
- You want statistical analysis (not just basic charts).
- You want to deploy a complete analytics platform.

## Real-World Use

You use Fitbit during the week, Garmin on weekends, and want to see:
- Your step patterns across both devices
- Statistical analysis of weekday vs weekend activity
- Peak activity times throughout the day
- Data quality metrics and missing data detection
- All of this in one unified dashboard

## Key Features

1. **Multi-Platform Support** - Connect Fitbit, Garmin, Apple Health, Google Fit
2. **Statistical Analysis** - Mean, median, pattern detection, missing data imputation
3. **Beautiful Charts** - Interactive visualizations of your activity patterns
4. **Docker Ready** - Deploy locally or to any cloud platform
5. **API Access** - Developer-friendly REST API for integrations

## Components

```
Activity Monitor
├── Backend (FastAPI)
│   ├── Connects to fitness APIs
│   ├── Performs statistical analysis
│   └── Serves data via REST API
├── Frontend (React)
│   ├── Platform selector
│   ├── Activity dashboard
│   └── Interactive charts
├── Database (PostgreSQL)
│   └── Stores activity history
└── Cache (Redis)
    └── Fast data retrieval
```

## Deployment Options

**Local Development**
```bash
docker compose up -d
# Visit http://localhost:3000
```

**Cloud Deployment**
- Deploy to AWS, Google Cloud, Azure
- Use provided Dockerfiles
- See DEPLOYMENT.md for detailed instructions

**What You Need**
- Docker installed on your machine
- Fitness platform API credentials (optional for testing)
- Optional: Cloud account for cloud deployment

## Architecture

```
┌─────────────┐
│   Fitbit    │
│   Garmin    │──────┐
│ Apple Health│      │
│  Google Fit │      │
└─────────────┘      │
                     ↓
              ┌──────────────┐
              │   Backend    │
              │   (FastAPI)  │────────┐
              └──────────────┘        │
                     ↓                │
              ┌──────────────┐        │
              │  PostgreSQL  │        │
              └──────────────┘        ↓
                     ↓         ┌──────────────┐
              ┌──────────────┐ │   Frontend   │
              │    Redis     │ │    (React)   │
              └──────────────┘ └──────────────┘
```

## Typical Workflow

1. User opens dashboard at http://localhost:3000
2. Selects fitness platform (e.g., Fitbit)
3. Connects account via OAuth
4. Platform fetches activity data from Fitbit API
5. Backend performs statistical analysis
6. Frontend displays charts and insights
7. User explores patterns in their activity data

## Sample Output

After connecting your fitness platform, you'll see:
- **Daily Statistics** - Mean steps, median steps, total activity
- **Peak Activity** - When you're most active during the day
- **Weekday Patterns** - How weekend activity differs from weekdays
- **Data Quality** - Missing data detection and completeness metrics
- **Interactive Charts** - Visual representation of all your activity data

## Next Steps

1. **Start the platform** - `docker compose up -d`
2. **Visit dashboard** - http://localhost:3000
3. **Connect a platform** - Click on your fitness device
4. **View your data** - See statistical insights and charts
5. **Explore patterns** - Understand your fitness behavior

For detailed deployment instructions, see `DEPLOYMENT.md`
For marketplace submission guide, see `README-MARKETPLACE.md`

