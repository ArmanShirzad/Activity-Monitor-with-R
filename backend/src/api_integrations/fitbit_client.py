"""
Fitbit API Integration
Integration with Fitbit Web API for activity data retrieval
"""

import requests
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime, timedelta


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
    
    def get_daily_activity_summary(self, date: str) -> Dict:
        """
        Get daily activity summary for a specific date
        
        Args:
            date: Date in format 'YYYY-MM-DD'
            
        Returns:
            Dictionary with activity data
        """
        url = f"{self.BASE_URL}/user/-/activities/date/{date}.json"
        response = requests.get(url, headers=self._get_headers())
        
        if response.status_code == 401:
            # Token expired, refresh and retry
            if self.refresh_access_token():
                response = requests.get(url, headers=self._get_headers())
        
        response.raise_for_status()
        return response.json()
    
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

