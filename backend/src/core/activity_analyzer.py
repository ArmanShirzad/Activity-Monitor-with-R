"""
Activity Analyzer - Core statistical analysis engine
Converted from R analysis to Python/pandas

This module replicates the R analysis from the original project:
- Daily step aggregation
- Mean/median calculations
- Missing value imputation
- Weekday/weekend pattern detection
- Time-interval analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class ActivityAnalyzer:
    """
    Core activity data analyzer
    Replicates R-based statistical analysis
    """
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with activity data
        
        Args:
            data: DataFrame with columns ['steps', 'date', 'interval']
        """
        self.data = data.copy()
        self.data['date'] = pd.to_datetime(self.data['date'])
    
    def calculate_daily_totals(self) -> pd.DataFrame:
        """
        Calculate total steps per day
        Equivalent to: aggregate(steps~date, data_activity, sum, na.rm=TRUE)
        
        Returns:
            DataFrame with date and total steps
        """
        totals = self.data.groupby('date')['steps'].sum().reset_index()
        totals.columns = ['date', 'steps']
        return totals
    
    def calculate_daily_statistics(self) -> Dict[str, float]:
        """
        Calculate mean and median of daily totals
        
        Returns:
            Dictionary with mean_steps and median_steps
        """
        daily_totals = self.calculate_daily_totals()
        
        return {
            'mean_steps': float(daily_totals['steps'].mean()),
            'median_steps': float(daily_totals['steps'].median()),
            'min_steps': float(daily_totals['steps'].min()),
            'max_steps': float(daily_totals['steps'].max()),
            'std_steps': float(daily_totals['steps'].std())
        }
    
    def calculate_interval_means(self) -> pd.DataFrame:
        """
        Calculate mean steps per time interval
        
        Returns:
            DataFrame with interval and mean steps
        """
        interval_means = self.data.groupby('interval')['steps'].mean().reset_index()
        interval_means.columns = ['interval', 'steps']
        return interval_means
    
    def find_peak_activity_interval(self) -> Tuple[int, float]:
        """
        Find the 5-minute interval with highest average activity
        
        Returns:
            Tuple of (interval, steps)
        """
        interval_means = self.calculate_interval_means()
        max_idx = interval_means['steps'].idxmax()
        
        return (
            int(interval_means.loc[max_idx, 'interval']),
            float(interval_means.loc[max_idx, 'steps'])
        )
    
    def impute_missing_values(self) -> pd.DataFrame:
        """
        Replace missing step values with interval mean
        Equivalent to R imputation logic
        
        Returns:
            DataFrame with imputed values
        """
        imputed_data = self.data.copy()
        interval_means = self.calculate_interval_means()
        
        # Create lookup dictionary
        mean_by_interval = dict(zip(interval_means['interval'], 
                                   interval_means['steps']))
        
        # Impute missing values
        imputed_data['steps'] = imputed_data.apply(
            lambda row: mean_by_interval.get(row['interval'], 0)
            if pd.isna(row['steps'])
            else row['steps'],
            axis=1
        )
        
        return imputed_data
    
    def analyze_weekday_patterns(self) -> Dict[str, pd.DataFrame]:
        """
        Analyze weekday vs weekend activity patterns
        
        Returns:
            Dictionary with 'weekday' and 'weekend' DataFrames
        """
        data = self.data.copy()
        
        # Add weekday/weekend classification
        data['day_type'] = data['date'].dt.dayofweek.apply(
            lambda x: 'weekday' if x < 5 else 'weekend'
        )
        
        # Separate weekday and weekend data
        weekday_data = data[data['day_type'] == 'weekday']
        weekend_data = data[data['day_type'] == 'weekend']
        
        # Calculate interval means for each
        weekday_means = weekday_data.groupby('interval')['steps'].mean().reset_index()
        weekday_means.columns = ['interval', 'steps']
        
        weekend_means = weekend_data.groupby('interval')['steps'].mean().reset_index()
        weekend_means.columns = ['interval', 'steps']
        
        return {
            'weekday': weekday_means,
            'weekend': weekend_means,
            'weekday_total_avg': float(weekday_data['steps'].mean()),
            'weekend_total_avg': float(weekend_data['steps'].mean())
        }
    
    def get_missing_data_summary(self) -> Dict[str, int]:
        """
        Summarize missing data
        
        Returns:
            Dictionary with counts of missing data
        """
        total_rows = len(self.data)
        missing_steps = self.data['steps'].isna().sum()
        missing_dates = self.data['date'].isna().sum()
        missing_intervals = self.data['interval'].isna().sum()
        
        # Count completely missing days
        daily_data = self.data.groupby('date').agg({
            'steps': lambda x: x.isna().all()
        })
        missing_days = int(daily_data['steps'].sum())
        
        return {
            'total_rows': int(total_rows),
            'missing_steps': int(missing_steps),
            'missing_intervals': int(missing_intervals),
            'missing_days': missing_days,
            'data_completeness': float((1 - missing_steps / total_rows) * 100) if total_rows > 0 else 0.0
        }
    
    def generate_summary_report(self) -> Dict:
        """
        Generate comprehensive analysis report
        
        Returns:
            Dictionary with all analysis results
        """
        daily_stats = self.calculate_daily_statistics()
        interval_means = self.calculate_interval_means()
        peak_interval, peak_value = self.find_peak_activity_interval()
        weekday_patterns = self.analyze_weekday_patterns()
        missing_summary = self.get_missing_data_summary()
        
        return {
            'daily_statistics': daily_stats,
            'peak_activity': {
                'interval': int(peak_interval),
                'average_steps': float(peak_value)
            },
            'weekday_patterns': {
                'weekday_avg': float(weekday_patterns['weekday_total_avg']),
                'weekend_avg': float(weekday_patterns['weekend_total_avg']),
                'weekday_intervals': [
                    {'interval': int(row['interval']), 'steps': float(row['steps'])}
                    for _, row in weekday_patterns['weekday'].iterrows()
                ],
                'weekend_intervals': [
                    {'interval': int(row['interval']), 'steps': float(row['steps'])}
                    for _, row in weekday_patterns['weekend'].iterrows()
                ]
            },
            'data_quality': missing_summary,
            'time_span': {
                'start_date': self.data['date'].min().isoformat(),
                'end_date': self.data['date'].max().isoformat(),
                'total_days': int((self.data['date'].max() - self.data['date'].min()).days + 1)
            }
        }

