"""
Fitbit API Integration
Integration with Fitbit Web API for activity data retrieval
"""

import requests
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta
import time


class FitbitClient:
    """
    Client for Fitbit Web API integration
    https://dev.fitbit.com/build/reference/web-api/
    """
    
    BASE_URL = "https://api.fitbit.com/1"
    
    def __init__(self, access_token: str, refresh_token: str, 
                 client_id: str, client_secret: str):
        """
        Initialize Fitbit client
        
        Args:
            access_token: OAuth access token
            refresh_token: OAuth refresh token
            client_id: Fitbit app client ID
            client_secret: Fitbit app client secret
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.client_id = client_id
        self.client_secret = client_secret
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/json'
        }
    
    def refresh_access_token(self) -> bool:
        """Refresh expired access token"""
        url = "https://api.fitbit.com/oauth2/token"
        
        auth_string = f"{self.client_id}:{self.client_secret}"
        import base64
        auth_header = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            self.refresh_token = token_data['refresh_token']
            return True
        
        return False
    
    def _make_request_with_retry(self, url: str, max_retries: int = 2, delay: float = 5.0) -> requests.Response:
        """
        Make HTTP request with basic retry logic
        Note: Rate limits are server-side and cannot be bypassed with retries
        
        Args:
            url: URL to request
            max_retries: Maximum number of retries (limited to avoid wasting time)
            delay: Delay between retries (seconds)
            
        Returns:
            Response object
        """
        for attempt in range(max_retries):
            response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 401:
                # Token expired, refresh and retry once
                if self.refresh_access_token():
                    response = requests.get(url, headers=self._get_headers())
            
            if response.status_code == 429:
                # Rate limited - this is server-side, retrying won't help much
                # Only retry once with a short delay in case it's a temporary spike
                if attempt < max_retries - 1:
                    time.sleep(delay)
                    continue
                else:
                    # Rate limit is real - raise error immediately
                    response.raise_for_status()
            
            if response.status_code == 200:
                return response
            
            # For other errors, raise immediately
            if response.status_code not in [429, 401]:
                response.raise_for_status()
        
        response.raise_for_status()
        return response
    
    def get_daily_activity_summary(self, date: str, include_intraday: bool = False) -> Dict:
        """
        Get daily activity summary with optional intraday step data
        
        Args:
            date: Date in format 'YYYY-MM-DD'
            include_intraday: Whether to fetch detailed intraday data (uses more API calls)
            
        Returns:
            Dictionary with activity data
        """
        # Get daily summary with retry logic
        url = f"{self.BASE_URL}/user/-/activities/date/{date}.json"
        response = self._make_request_with_retry(url)
        daily_data = response.json()
        
        # Only fetch intraday data if requested (to save API calls)
        if include_intraday:
            # Wait longer between requests to avoid rate limits
            time.sleep(2.0)  # Increased delay
            intraday_url = f"{self.BASE_URL}/user/-/activities/steps/date/{date}/1d/1min.json"
            try:
                intraday_response = self._make_request_with_retry(intraday_url)
                if intraday_response.status_code == 200:
                    intraday_data = intraday_response.json()
                    # Merge intraday data into daily data
                    if 'activities-steps-intraday' in intraday_data:
                        daily_data['activities-steps-intraday'] = intraday_data['activities-steps-intraday']
            except requests.exceptions.HTTPError as e:
                # If intraday fails due to rate limit, continue with daily summary only
                if "429" in str(e) or "Rate limit" in str(e):
                    print(f"Warning: Could not fetch intraday data for {date} due to rate limits. Using daily summary only.")
                else:
                    raise
        
        return daily_data
    
    def get_activity_time_series_batch(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get activity time series data for a date range (more efficient than daily calls)
        Note: This endpoint also counts toward rate limits
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of daily activity summaries
        """
        # Use time-series API which is more efficient for ranges
        # But still subject to rate limits
        url = f"{self.BASE_URL}/user/-/activities/steps/date/{start_date}/{end_date}.json"
        try:
            response = self._make_request_with_retry(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('activities-steps', [])
        except requests.exceptions.HTTPError as e:
            if "429" in str(e) or "Rate limit" in str(e):
                # Return empty list if rate limited - will fall back to daily calls
                return []
            raise
        return []
    
    def get_heart_rate_data(self, date: str) -> Dict:
        """Get heart rate data for a specific date"""
        url = f"{self.BASE_URL}/user/-/activities/heart/date/{date}/1d/1sec.json"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 401:
            if self.refresh_access_token():
                response = requests.get(url, headers=self._get_headers())
        
        response.raise_for_status()
        return response.json()
    
    def get_activity_time_series(self, start_date: str, end_date: str, 
                                 resource: str = 'steps') -> List[Dict]:
        """
        Get activity time series data
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            resource: Resource type (steps, distance, floors, caloriesBurned)
            
        Returns:
            List of activity data points
        """
        url = f"{self.BASE_URL}/user/-/activities/{resource}/date/{start_date}/{end_date}.json"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 401:
            if self.refresh_access_token():
                response = requests.get(url, headers=self._get_headers())
        
        response.raise_for_status()
        return response.json()[f'activities-{resource}']
    
    def convert_to_activity_format(self, date: str, data: Dict) -> pd.DataFrame:
        """
        Convert Fitbit data to standard activity format
        Compatible with ActivityAnalyzer
        
        Args:
            date: Date of data
            data: Raw Fitbit data
            
        Returns:
            DataFrame with columns [steps, date, interval]
        """
        # Extract 5-minute interval data from Fitbit minute-by-minute data
        intervals = []
        
        # Fitbit provides minute-by-minute data, convert to 5-minute intervals
        if 'activities-steps-intraday' in data:
            intraday = data['activities-steps-intraday']['dataset']
            
            interval_minutes = []
            for entry in intraday:
                time_str = entry['time']
                hour, minute = map(int, time_str.split(':'))
                interval = hour * 60 + minute  # Convert to minutes since midnight
                
                # Group into 5-minute intervals
                interval_5min = (interval // 5) * 5
                
                interval_minutes.append({
                    'interval': interval_5min,
                    'steps': entry['value']
                })
            
            # Aggregate by 5-minute intervals
            df = pd.DataFrame(interval_minutes)
            df = df.groupby('interval')['steps'].sum().reset_index()
            
            df['date'] = pd.to_datetime(date)
            df = df[['steps', 'date', 'interval']]
            
            return df
        
        # Fallback: get daily summary
        summary = data.get('summary', {})
        total_steps = summary.get('steps', 0)
        
        return pd.DataFrame({
            'steps': [total_steps],
            'date': [pd.to_datetime(date)],
            'interval': [0]
        })
    
    def get_user_profile(self) -> Dict:
        """Get Fitbit user profile information"""
        url = f"{self.BASE_URL}/user/-/profile.json"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 401:
            if self.refresh_access_token():
                response = requests.get(url, headers=self._get_headers())
        
        response.raise_for_status()
        return response.json()['user']

