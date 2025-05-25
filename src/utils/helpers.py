"""
Helper functions for the stock analysis system.
"""

import datetime

def get_date_n_days_ago(n):
    """
    Get the date n days ago from today.
    
    Args:
        n (int): Number of days to go back
        
    Returns:
        str: Date in YYYY-MM-DD format
    """
    today = datetime.datetime.now()
    past_date = today - datetime.datetime.timedelta(days=n)
    return past_date.strftime('%Y-%m-%d')

def format_percentage(value):
    """
    Format a decimal value as a percentage with sign.
    
    Args:
        value (float): Value to format
        
    Returns:
        str: Formatted percentage
    """
    return f"{'+' if value > 0 else ''}{value:.2f}%"