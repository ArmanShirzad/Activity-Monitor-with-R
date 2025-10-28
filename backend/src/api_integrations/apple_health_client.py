"""
Apple HealthKit Integration
Integration with Apple Health data through HealthKit API
Note: iOS app required for HealthKit access
"""

import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime


class AppleHealthClient:
    """
    Client for Apple HealthKit data processing
    Note: HealthKit is iOS-only, requires app with HealthKit entitlements
    This module processes exported HealthKit data (XML or CSV)
    """
    
    def __init__(self, health_data_file: Optional[str] = None):
        """
        Initialize Apple Health client
        
        Args:
            health_data_file: Path to exported HealthKit XML or CSV file
        """
        self.health_data = None
        if health_data_file:
            self.load_health_data(health_data_file)
    
    def load_health_data(self, file_path: str):
        """Load HealthKit exported data"""
        if file_path.endswith('.csv'):
            self.health_data = pd.read_csv(file_path)
        elif file_path.endswith('.xml'):
            # Parse HealthKit XML export
            import xml.etree.ElementTree as ET
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            records = []
            for record in root.findall('.//Record'):
                record_data = record.attrib.copy()
                records.append(record_data)
            
            self.health_data = pd.DataFrame(records)
    
    def get_step_data(self, start_date: Optional[str] = None, 
                     end_date: Optional[str] = None) -> pd.DataFrame:
        """
        Extract step count data from HealthKit export
        
        Args:
            start_date: Start date filter (YYYY-MM-DD)
            end_date: End date filter (YYYY-MM-DD)
            
        Returns:
            DataFrame with step data
        """
        if self.health_data is None:
            return pd.DataFrame()
        
        # Filter step count records
        step_data = self.health_data[
            self.health_data['type'] == 'HKQuantityTypeIdentifierStepCount'
        ].copy()
        
        if 'startDate' in step_data.columns:
            step_data['startDate'] = pd.to_datetime(step_data['startDate'])
            
            if start_date:
                step_data = step_data[step_data['startDate'] >= start_date]
            if end_date:
                step_data = step_data[step_data['startDate'] <= end_date]
        
        return step_data
    
    def convert_to_activity_format(self, step_data: pd.DataFrame) -> pd.DataFrame:
        """
        Convert HealthKit step data to standard activity format
        
        Args:
            step_data: HealthKit step data DataFrame
            
        Returns:
            DataFrame with columns [steps, date, interval]
        """
        if step_data.empty:
            return pd.DataFrame({
                'steps': [0],
                'date': [pd.to_datetime('2024-01-01')],
                'interval': [0]
            })
        
        # Extract date and interval
        intervals = []
        
        for _, row in step_data.iterrows():
            date_str = row['startDate']
            steps = float(row.get('value', 0))
            
            if isinstance(date_str, str):
                dt = pd.to_datetime(date_str)
            else:
                dt = date_str
            
            # Calculate interval in minutes since midnight
            interval = dt.hour * 60 + dt.minute
            
            # Round to 5-minute interval
            interval_5min = (interval // 5) * 5
            
            intervals.append({
                'date': dt.normalize(),
                'interval': interval_5min,
                'steps': steps
            })
        
        df = pd.DataFrame(intervals)
        
        # Aggregate by 5-minute intervals per day
        if not df.empty:
            df = df.groupby(['date', 'interval'])['steps'].sum().reset_index()
        
        return df[['steps', 'date', 'interval']] if not df.empty else pd.DataFrame({
            'steps': [0],
            'date': [pd.to_datetime('2024-01-01')],
            'interval': [0]
        })
    
    def get_daily_summary(self, date: str) -> Dict:
        """
        Get daily activity summary
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            Dictionary with daily summary
        """
        step_data = self.get_step_data(start_date=date, end_date=date)
        
        if step_data.empty:
            return {
                'date': date,
                'total_steps': 0,
                'active_minutes': 0
            }
        
        total_steps = step_data['value'].sum()
        
        return {
            'date': date,
            'total_steps': int(total_steps),
            'active_minutes': len(step_data)
        }

