"""
Yahoo Finance data fetcher for Turkish Market Regime Detector
Provides functionality to fetch BIST100 and other Turkish market data
"""

import pandas as pd
import numpy as np
from typing import Optional, List, Union
import logging

logger = logging.getLogger(__name__)


class YFinanceFetcher:
    """
    Fetches market data from Yahoo Finance for Turkish equities.
    Handles BIST100 stocks and forex pairs.
    """
    
    # Common BIST100 tickers
    DEFAULT_TICKERS = [
        "THYAO.IS", "EREGL.IS", "ASELS.IS", "SISE.IS", "KCHOL.IS",
        "AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "HALKB.IS",
        "BIMAS.IS", "SASA.IS", "KMPUR.IS", "PETKM.IS", "TUPRS.IS",
        "FROTO.IS", "SOKM.IS", "HEKTS.IS", "AKSA.IS", "ENKAI.IS"
    ]
    
    # Alternative tickers for proxy data
    PROXY_TICKERS = {
        "USDTRY": "TRY=X",  # USD/TRY exchange rate
        "EURTRY": "EURTRY=X",  # EUR/TRY
        "BIST100": "^XU100",  # BIST100 index
        "SP500": "^GSPC",  # S&P 500 (for global risk sentiment)
        "NASDAQ": "^IXIC"  # NASDAQ (for tech risk sentiment)
    }
    
    def __init__(
        self,
        period: str = "2y",
        interval: str = "1d",
        proxy_ticker: str = "USDTRY=X"
    ):
        """
        Initialize YFinance fetcher.
        
        Args:
            period: Data period (e.g., "1y", "2y", "5y")
            interval: Data interval (e.g., "1d", "1wk", "1mo")
            proxy_ticker: Default proxy ticker for market data
        """
        self.period = period
        self.interval = interval
        self.proxy_ticker = proxy_ticker
        
    def _import_yfinance(self):
        """Import yfinance with proper error handling"""
        try:
            import yfinance as yf
            return yf
        except ImportError:
            logger.error("yfinance not installed. Run: pip install yfinance")
            raise ImportError("yfinance is required. Install with: pip install yfinance")
    
    def fetch_ticker_data(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch data for a single ticker.
        
        Args:
            ticker: Yahoo Finance ticker symbol
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            DataFrame with OHLCV data
        """
        yf = self._import_yfinance()
        
        try:
            stock = yf.Ticker(ticker)
            
            if start_date and end_date:
                df = stock.history(start=start_date, end=end_date)
            else:
                df = stock.history(period=self.period)
            
            if df.empty:
                logger.warning(f"No data returned for ticker: {ticker}")
                
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {ticker}: {str(e)}")
            return pd.DataFrame()
    
    def fetch_multiple_tickers(
        self,
        tickers: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        progress: bool = True
    ) -> pd.DataFrame:
        """
        Fetch data for multiple tickers and combine.
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date
            end_date: End date
            progress: Show progress
            
        Returns:
            Combined DataFrame with all ticker data
        """
        all_data = {}
        
        for i, ticker in enumerate(tickers):
            if progress:
                print(f"Fetching {ticker} ({i+1}/{len(tickers)})...")
            
            df = self.fetch_ticker_data(ticker, start_date, end_date)
            
            if not df.empty:
                all_data[ticker] = df['Close']
                
        if not all_data:
            logger.warning("No data fetched for any ticker")
            return pd.DataFrame()
            
        combined = pd.DataFrame(all_data)
        combined = combined.dropna()
        
        return combined
    
    def fetch_proxy_data(
        self,
        proxy_type: str = "USDTRY"
    ) -> pd.DataFrame:
        """
        Fetch proxy data (forex, indices) for regime detection.
        
        Args:
            proxy_type: Type of proxy data to fetch
            
        Returns:
            DataFrame with proxy data
        """
        ticker = self.PROXY_TICKERS.get(proxy_type, self.proxy_ticker)
        return self.fetch_ticker_data(ticker)
    
    def fetch_market_breadth(
        self,
        tickers: Optional[List[str]] = None
    ) -> dict:
        """
        Calculate market breadth metrics.
        
        Args:
            tickers: List of tickers to analyze
            
        Returns:
            Dictionary with breadth metrics
        """
        if tickers is None:
            tickers = self.DEFAULT_TICKERS
            
        data = self.fetch_multiple_tickers(tickers, progress=False)
        
        if data.empty:
            return {}
        
        # Calculate daily returns
        returns = data.pct_change().dropna()
        
        # Breadth metrics
        breadth = {
            "advance_decline": (returns > 0).sum() - (returns < 0).sum(),
            "advance_count": (returns > 0).sum(),
            "decline_count": (returns < 0).sum(),
            "avg_return": returns.mean().mean(),
            "median_return": returns.median().median(),
            "volatility": returns.std().mean()
        }
        
        return breadth
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get current/last price for a ticker.
        
        Args:
            ticker: Yahoo Finance ticker
            
        Returns:
            Current price or None
        """
        data = self.fetch_ticker_data(ticker)
        
        if not data.empty:
            return float(data['Close'].iloc[-1])
        return None
    
    def fetch_fundamental_data(self, ticker: str) -> dict:
        """
        Fetch fundamental data for a ticker.
        
        Args:
            ticker: Yahoo Finance ticker
            
        Returns:
            Dictionary with fundamental metrics
        """
        yf = self._import_yfinance()
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            fundamentals = {
                "market_cap": info.get("marketCap"),
                "pe_ratio": info.get("trailingPE"),
                "dividend_yield": info.get("dividendYield"),
                "beta": info.get("beta"),
                "52w_high": info.get("fiftyTwoWeekHigh"),
                "52w_low": info.get("fiftyTwoWeekLow"),
                "volume": info.get("volume"),
                "avg_volume": info.get("averageVolume")
            }
            
            return fundamentals
            
        except Exception as e:
            logger.error(f"Error fetching fundamentals for {ticker}: {str(e)}")
            return {}
    
    def download_batch(
        self,
        tickers: List[str],
        filename: str = "batch_data.csv"
    ) -> pd.DataFrame:
        """
        Download batch data and save to CSV.
        
        Args:
            tickers: List of tickers
            filename: Output filename
            
        Returns:
            DataFrame with downloaded data
        """
        data = self.fetch_multiple_tickers(tickers, progress=True)
        
        if not data.empty:
            data.to_csv(filename)
            logger.info(f"Data saved to {filename}")
            
        return data


def fetch_yfinance_data(
    tickers: List[str],
    period: str = "2y",
    interval: str = "1d"
) -> pd.DataFrame:
    """
    Convenience function to fetch Yahoo Finance data.
    
    Args:
        tickers: List of ticker symbols
        period: Data period
        interval: Data interval
        
    Returns:
        Combined DataFrame
    """
    fetcher = YFinanceFetcher(period=period, interval=interval)
    return fetcher.fetch_multiple_tickers(tickers)