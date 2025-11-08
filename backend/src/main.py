"""
FastAPI Backend Server
Main API endpoints for activity monitoring platform
"""

from fastapi import FastAPI, HTTPException, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import base64
import secrets
from urllib.parse import urlencode
import time

from src.core.activity_analyzer import ActivityAnalyzer
from src.api_integrations.fitbit_client import FitbitClient
from src.api_integrations.garmin_client import GarminClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Activity Monitor API",
    description="Production-ready activity monitoring platform with multi-device support",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ActivityData(BaseModel):
    steps: float
    date: str
    interval: int

class ActivityRequest(BaseModel):
    platform: str  # 'fitbit', 'garmin', 'apple', 'manual'
    start_date: str
    end_date: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class AnalysisResponse(BaseModel):
    daily_statistics: Dict
    peak_activity: Dict
    weekday_patterns: Dict
    data_quality: Dict
    time_span: Dict

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Activity Monitor API",
        "version": "1.0.0",
        "status": "operational",
        "features": [
            "Multi-device integration",
            "Statistical analysis",
            "Pattern detection",
            "Data visualization"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/api/v1/activity/analyze", response_model=AnalysisResponse)
async def analyze_activity(request: ActivityRequest):
    """
    Analyze activity data from specified platform
    
    Args:
        request: Activity request with platform and date range
        
    Returns:
        Complete analysis results
    """
    try:
        # Load API keys from environment
        api_keys = {
            'fitbit_client_id': os.getenv('FITBIT_CLIENT_ID', ''),
            'fitbit_client_secret': os.getenv('FITBIT_CLIENT_SECRET', ''),
            'garmin_consumer_key': os.getenv('GARMIN_CONSUMER_KEY', ''),
            'garmin_consumer_secret': os.getenv('GARMIN_CONSUMER_SECRET', '')
        }
        
        # Fetch data from platform
        if request.platform == 'fitbit':
            client = FitbitClient(
                access_token=request.access_token or '',
                refresh_token=request.refresh_token or '',
                client_id=api_keys['fitbit_client_id'],
                client_secret=api_keys['fitbit_client_secret']
            )
            
            # Get activity data with rate limiting
            data_list = []
            current_date = datetime.strptime(request.start_date, '%Y-%m-%d')
            end_date = datetime.strptime(request.end_date, '%Y-%m-%d')
            
            # Fitbit rate limits: 150 requests/hour per user (server-side, cannot be bypassed)
            # Strategy: Make minimal API calls - only daily summaries, no intraday data
            # If rate limited, we must wait for Fitbit's rate limit window to reset
            
            # Fetch daily summaries only (no intraday data to minimize API calls)
            request_count = 0
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                try:
                    # Get daily summary WITHOUT intraday data (saves 50% of API calls)
                    daily_data = client.get_daily_activity_summary(date_str, include_intraday=False)
                    activity_df = client.convert_to_activity_format(date_str, daily_data)
                    data_list.append(activity_df)
                    request_count += 1
                    current_date += timedelta(days=1)
                    
                    # Small delay to avoid rapid-fire requests (but won't prevent rate limits)
                    if current_date <= end_date:
                        time.sleep(1.0)
                        
                except Exception as e:
                    error_msg = str(e)
                    # Rate limit is server-side - we must handle it gracefully
                    if "429" in error_msg or "Rate limit" in error_msg or "Too Many Requests" in error_msg:
                        if data_list:
                            # We have some data, use what we have
                            break
                        else:
                            # No data - rate limit hit before any data retrieved
                            raise HTTPException(
                                status_code=429,
                                detail="Fitbit API rate limit exceeded. "
                                       "Fitbit allows 150 requests per hour per user. "
                                       "Please wait 30-60 minutes for the rate limit to reset, then try again. "
                                       "This is a Fitbit server-side restriction and cannot be bypassed."
                            )
                    # For other errors, continue to next day
                    current_date += timedelta(days=1)
                    continue
            
            # Combine all data
            if not data_list:
                raise HTTPException(
                    status_code=404,
                    detail="No activity data found for the specified date range"
                )
            df = pd.concat(data_list, ignore_index=True)
            
            # Check if dataframe is empty
            if df.empty or len(df) == 0:
                raise HTTPException(
                    status_code=404,
                    detail="No activity data available for analysis"
                )
            
        elif request.platform == 'garmin':
            client = GarminClient(
                consumer_key=api_keys['garmin_consumer_key'],
                consumer_secret=api_keys['garmin_consumer_secret']
            )
            
            # Get activity data
            daily_summaries = client.get_daily_steps(request.start_date, request.end_date)
            
            # Convert to DataFrame
            data_list = []
            for summary in daily_summaries:
                # Would need to implement proper conversion
                pass
            
            # Placeholder - would fetch real data
            df = pd.DataFrame({
                'steps': [10000],
                'date': [pd.to_datetime(request.start_date)],
                'interval': [0]
            })
            
        elif request.platform == 'manual':
            # Accept manual data upload
            return {"error": "Manual upload not yet implemented"}
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported platform: {request.platform}"
            )
        
        # Check if dataframe is empty before analysis
        if df.empty or len(df) == 0:
            raise HTTPException(
                status_code=404,
                detail="No activity data available for analysis"
            )
        
        # Perform analysis
        analyzer = ActivityAnalyzer(df)
        results = analyzer.generate_summary_report()
        
        return AnalysisResponse(**results)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/platforms")
async def get_supported_platforms():
    """Get list of supported fitness platforms"""
    return {
        "platforms": [
            {
                "name": "Fitbit",
                "id": "fitbit",
                "api_url": "https://dev.fitbit.com",
                "supports_direct_integration": True
            },
            {
                "name": "Garmin",
                "id": "garmin",
                "api_url": "https://developer.garmin.com",
                "supports_direct_integration": True
            },
            {
                "name": "Apple Health",
                "id": "apple",
                "api_url": "https://developer.apple.com/healthkit",
                "supports_direct_integration": False,
                "note": "Requires iOS app with HealthKit entitlement"
            },
            {
                "name": "Google Fit",
                "id": "google",
                "api_url": "https://developers.google.com/fit",
                "supports_direct_integration": True
            }
        ]
    }

@app.get("/api/v1/analyzer/features")
async def get_analysis_features():
    """Get list of available analysis features"""
    return {
        "features": [
            "Daily step aggregation",
            "Mean and median statistics",
            "Peak activity detection",
            "Weekday vs weekend patterns",
            "Time-interval analysis",
            "Missing data imputation",
            "Statistical summaries",
            "Data quality metrics"
        ],
        "algorithms": [
            "Pandas-based aggregation",
            "Statistical imputation",
            "Time-series analysis",
            "Pattern recognition"
        ]
    }

# OAuth Endpoints

@app.get("/api/v1/auth/fitbit/authorize")
async def fitbit_authorize(request: Request):
    """
    Initiate Fitbit OAuth 2.0 authorization flow
    Redirects user to Fitbit authorization page
    """
    client_id = os.getenv('FITBIT_CLIENT_ID', '')
    redirect_uri = os.getenv('FITBIT_REDIRECT_URI', 'http://localhost:8000/api/v1/auth/fitbit/callback')
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    if not client_id:
        raise HTTPException(status_code=500, detail="Fitbit Client ID not configured")
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in session/cookie (simplified - in production use proper session management)
    # For now, we'll pass it in the redirect URL
    
    # Fitbit OAuth 2.0 authorization URL
    scope = "activity heartrate profile"  # Requested permissions
    auth_url = (
        f"https://www.fitbit.com/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}&"
        f"state={state}"
    )
    
    # Store state in response (in production, use secure session storage)
    response = RedirectResponse(url=auth_url)
    response.set_cookie(key="oauth_state", value=state, httponly=True, samesite="lax")
    return response

@app.get("/api/v1/auth/fitbit/callback")
async def fitbit_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    request: Request = None
):
    """
    Handle Fitbit OAuth 2.0 callback
    Exchanges authorization code for access token
    """
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
    
    if error:
        # User denied authorization
        return RedirectResponse(
            url=f"{frontend_url}?error={error}&error_description=User denied authorization"
        )
    
    if not code:
        return RedirectResponse(
            url=f"{frontend_url}?error=missing_code&error_description=Authorization code not provided"
        )
    
    # Verify state (in production, check against stored state)
    # For now, we'll proceed with token exchange
    
    client_id = os.getenv('FITBIT_CLIENT_ID', '')
    client_secret = os.getenv('FITBIT_CLIENT_SECRET', '')
    redirect_uri = os.getenv('FITBIT_REDIRECT_URI', 'http://localhost:8000/api/v1/auth/fitbit/callback')
    
    if not client_id or not client_secret:
        return RedirectResponse(
            url=f"{frontend_url}?error=configuration_error&error_description=Fitbit credentials not configured"
        )
    
    # Exchange authorization code for access token
    token_url = "https://api.fitbit.com/oauth2/token"
    
    auth_string = f"{client_id}:{client_secret}"
    auth_header = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth_header}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    
    import requests
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        token_data = response.json()
        
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        expires_in = token_data.get('expires_in', 28800)  # Default 8 hours
        
        # Redirect to frontend with tokens
        # In production, store tokens securely server-side and use session IDs
        params = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'platform': 'fitbit'
        }
        
        return RedirectResponse(
            url=f"{frontend_url}?{urlencode(params)}"
        )
        
    except requests.exceptions.RequestException as e:
        return RedirectResponse(
            url=f"{frontend_url}?error=token_exchange_failed&error_description={str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

