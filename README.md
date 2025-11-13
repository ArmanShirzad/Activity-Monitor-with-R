# Activity Monitor with R
targeted for commercial use cases later.
Personal Activity Monitoring Project  
Arman Shirzad  
07/15/2023

## Synopsis

Activity monitoring devices, such as Fitbit, Nike Fuelband, and Jawbone Up, have become increasingly popular and allow individuals to collect a vast amount of personal movement data. This data can be used to enhance one's health, identify patterns in their behavior, or simply out of interest in technology. However, despite the abundance of data, it remains underutilized due to difficulties in obtaining raw data and the lack of statistical methods and software for processing and interpreting the data.

In this project, we will analyze data from a personal activity monitoring device recording the number of steps taken in 5-minute intervals each day for two months (October and November 2012) from an anonymous individual. We will use statistical methods and software to process and interpret the data, providing insights into the individual's activity patterns during this period. The project will involve data cleaning, exploratory data analysis, and statistical modeling to identify patterns and trends in the data.

The project aims to demonstrate the value of personal activity monitoring data in providing insights into one's behavior and health patterns. It will also showcase the importance of statistical methods and software in processing and interpreting this data, providing a foundation for future research and analysis in this field. The data used in this project is available for download from the provided link, and the results will be presented in a report.

## Project Status

This project has been converted from R to a production-ready web application with:

- **Backend API** (FastAPI/Python) - Handles data from fitness platforms
- **Frontend Dashboard** (React) - Web UI for viewing activity statistics
- **Database** (PostgreSQL) - Stores activity history
- **Cache** (Redis) - Fast data retrieval
- **Statistical Analysis** - R-based algorithms converted to Python

## Quick Start

```bash
# Start all services with Docker
docker compose up -d

# Visit the dashboard
# Open http://localhost:3000 in your browser
```

## Features

- Multi-platform support (Fitbit, Garmin, Apple Health, Google Fit)
- OAuth 2.0 authentication
- Statistical analysis (mean, median, pattern detection)
- Interactive visualizations
- Docker containerization

## Documentation

- `QUICKSTART.md` - Quick start guide
- `DEPLOYMENT.md` - Deployment instructions
- `README-MARKETPLACE.md` - Marketplace submission guide
- `PROJECT_SUMMARY.md` - Full feature list
- `PROJECT_OVERVIEW.md` - Project overview

## License

See LICENSE file for details.

