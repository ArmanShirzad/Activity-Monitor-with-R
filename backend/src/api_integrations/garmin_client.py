"""
Garmin Connect IQ API Integration
Integration with Garmin devices for activity data retrieval
"""

import requests
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime
import oauthlib.oauth1 as oauth


class GarminClient:
    """
    Client for Garmin Connect API
    https://developer.garmin.com/
    """
    
    BASE_URL = "https://connectapi.garmin.com"
    OAUTH_URL = "https://connect.garmin.com/oauth/request_token"
    
    def __init__(self, consumer_key: str, consumer_secret: str,
                 access_token: str = None, access_token_secret: str = None):
        """
        Initialize Garmin client
        
        Args:
            consumer_key: Garmin Connect IQ consumer key
            consumer_secret: Garmin Connect IQ consumer secret
            access_token: OAuth access token
            access_token_secret: OAuth access token secret
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
        # OAuth1 client
        self.client = oauth.Client(
            oauth.Client(consumer_key, consumer_secret),
            signature_method=oauth.SIGNATURE_HMAC
        )
    
    def _get_oauth_header(self, url: str, method: str = 'GET') -> str:
        """Generate OAuth1 authorization header"""
        oauth_request = oauth.Request.from_consumer_and_token(
            oauth.Client(self.consumer_key, self.consumer_secret),
            token=self.access_token if self.access_token else None
        )
        oauth_request.sign_request(
            oauth.SignatureMethod_HMAC_SHA1(),
            oauth.Client(self.consumer_key, self.consumer_secret),
            self.access_token
        )
        return oauth_request.to_header()['Authorization']
    
    def get_daily_summary(self, date: str) -> Dict:
        """
        Get daily activity summary
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Dictionary with daily summary
        """
        url = f"{self.BASE_URL}/wellness-service/wellness/dailySummary/{date}"
        headers = {
            'Authorization': self._get_oauth_header(url),
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def get_daily_steps(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Get daily step data for date range
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            List of daily step summaries
        """
        url = f"{self.BASE_URL}/wellness-service/wellness/dailySummaryChart"
        params = {
            'startDate': start_date,
            'endDate': end_date
        }
        
        headers = {
            'Authorization': self._get_oauth_header(url),
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_intraday_activity(self, date: str) -> List[Dict]:
        """
        Get intraday activity data (minute-by-minute)
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            List of minute-level activity data
        """
        url = f"{self.BASE_URL}/wellness-service/wellness/intraday/{date}"
        headers = {
            'Authorization': self._get_oauth_header(url),
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def convert_to_activity_format(self, date: str, data: List[Dict]) -> pd.DataFrame:
        """
        Convert Garmin data to standard activity format
        
        Args:
            date: Date of data
            data: Raw Garmin intraday data
            
        Returns:
            DataFrame with columns [steps, date, interval]
        """
        intervals = []
        
        for entry in data:
            timestamp = entry.get('timestamp')
            steps = entry.get('steps', 0)
            
            if timestamp:
                # Parse timestamp and calculate interval
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                # Convert to minutes since midnight
                interval = dt.hour * 60 + dt.minute
                
                # Round to nearest 5-minute interval
                interval_5min = (interval // 5) * 5
                
                intervals.append({
                    'interval': interval_5min,
                    'steps': steps,
                    'date': pd.to_datetime(date)
                })
        
        df = pd.DataFrame(intervals)
        
        # Aggregate by 5-minute intervals
        if not df.empty:
            df = df.groupby('interval')['steps'].sum().reset_index()
            df['date'] = pd.to_datetime(date)
        
        return df[['steps', 'date', 'interval']] if not df.empty else pd.DataFrame({
            'steps': [0],
            'date': [pd.to_datetime(date)],
            'interval': [0]
        })
    
    def get_user_info(self) -> Dict:
        """Get Garmin user information"""
        url = f"{self.BASE_URL}/user-service/user/user-info"
        headers = {
            'Authorization': self._get_oauth_header(url),
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

