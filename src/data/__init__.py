"""
Data module for Turkish Market Regime Detector
Contains data fetching and processing functionality
"""

from .yfinance_fetcher import YFinanceFetcher
from .evds_fetcher import EVDSFetcher
from .processor import DataProcessor

__all__ = [
    "YFinanceFetcher",
    "EVDSFetcher", 
    "DataProcessor"
]