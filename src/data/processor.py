"""
Data processor for regime detection features
Handles feature engineering and technical indicator calculation
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """
    Processes market data and generates features for regime detection.
    Calculates technical indicators and derived metrics.
    """
    
    def __init__(
        self,
        rsi_period: int = 14,
        volatility_window: int = 20,
        momentum_period: int = 10,
        ma_short: int = 20,
        ma_long: int = 50,
        volume_ma_period: int = 20
    ):
        """
        Initialize data processor.
        
        Args:
            rsi_period: Period for RSI calculation
            volatility_window: Window for volatility calculation
            momentum_period: Period for momentum calculation
            ma_short: Short moving average period
            ma_long: Long moving average period
            volume_ma_period: Volume moving average period
        """
        self.rsi_period = rsi_period
        self.volatility_window = volatility_window
        self.momentum_period = momentum_period
        self.ma_short = ma_short
        self.ma_long = ma_long
        self.volume_ma_period = volume_ma_period
    
    def calculate_returns(self, prices: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate daily returns from price data.
        
        Args:
            prices: DataFrame with price data
            
        Returns:
            DataFrame with daily returns
        """
        return prices.pct_change().dropna()
    
    def calculate_cumulative_returns(
        self,
        prices: pd.DataFrame,
        period: int = 1
    ) -> pd.DataFrame:
        """
        Calculate cumulative returns over period.
        
        Args:
            prices: DataFrame with price data
            period: Number of days for cumulative return
            
        Returns:
            DataFrame with cumulative returns
        """
        return prices.pct_change(period).dropna()
    
    def calculate_rsi(
        self,
        prices: pd.Series,
        period: Optional[int] = None
    ) -> pd.Series:
        """
        Calculate Relative Strength Index.
        
        Args:
            prices: Price series
            period: RSI period (default: self.rsi_period)
            
        Returns:
            Series with RSI values
        """
        if period is None:
            period = self.rsi_period
            
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gain = gains.rolling(window=period).mean()
        avg_loss = losses.rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_volatility(
        self,
        returns: pd.Series,
        window: Optional[int] = None
    ) -> pd.Series:
        """
        Calculate rolling volatility.
        
        Args:
            returns: Returns series
            window: Window size (default: self.volatility_window)
            
        Returns:
            Series with volatility values
        """
        if window is None:
            window = self.volatility_window
            
        return returns.rolling(window=window).std() * np.sqrt(252)
    
    def calculate_momentum(
        self,
        prices: pd.Series,
        period: Optional[int] = None
    ) -> pd.Series:
        """
        Calculate price momentum.
        
        Args:
            prices: Price series
            period: Period for momentum (default: self.momentum_period)
            
        Returns:
            Series with momentum values
        """
        if period is None:
            period = self.momentum_period
            
        return prices.pct_change(period)
    
    def calculate_moving_average(
        self,
        prices: pd.Series,
        period: int
    ) -> pd.Series:
        """
        Calculate simple moving average.
        
        Args:
            prices: Price series
            period: MA period
            
        Returns:
            Series with MA values
        """
        return prices.rolling(window=period).mean()
    
    def calculate_ema(
        self,
        prices: pd.Series,
        period: int
    ) -> pd.Series:
        """
        Calculate exponential moving average.
        
        Args:
            prices: Price series
            period: EMA period
            
        Returns:
            Series with EMA values
        """
        return prices.ewm(span=period, adjust=False).mean()
    
    def calculate_volume_ratio(
        self,
        volume: pd.Series,
        window: Optional[int] = None
    ) -> pd.Series:
        """
        Calculate volume relative to moving average.
        
        Args:
            volume: Volume series
            window: Window size (default: self.volume_ma_period)
            
        Returns:
            Series with volume ratio
        """
        if window is None:
            window = self.volume_ma_period
            
        volume_ma = volume.rolling(window=window).mean()
        return volume / volume_ma
    
    def calculate_bollinger_bands(
        self,
        prices: pd.Series,
        period: int = 20,
        num_std: float = 2.0
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate Bollinger Bands.
        
        Args:
            prices: Price series
            period: MA period
            num_std: Number of standard deviations
            
        Returns:
            Tuple of (upper_band, middle_band, lower_band)
        """
        middle = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        
        upper = middle + (std * num_std)
        lower = middle - (std * num_std)
        
        return upper, middle, lower
    
    def calculate_macd(
        self,
        prices: pd.Series,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD indicator.
        
        Args:
            prices: Price series
            fast: Fast EMA period
            slow: Slow EMA period
            signal: Signal line period
            
        Returns:
            Tuple of (macd, signal, histogram)
        """
        ema_fast = prices.ewm(span=fast, adjust=False).mean()
        ema_slow = prices.ewm(span=slow, adjust=False).mean()
        
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return macd, signal_line, histogram
    
    def calculate_atr(
        self,
        high: pd.Series,
        low: pd.Series,
        close: pd.Series,
        period: int = 14
    ) -> pd.Series:
        """
        Calculate Average True Range.
        
        Args:
            high: High price series
            low: Low price series
            close: Close price series
            period: ATR period
            
        Returns:
            Series with ATR values
        """
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        
        return atr
    
    def create_features(
        self,
        prices: pd.DataFrame,
        volumes: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Create comprehensive feature set for regime detection.
        
        Args:
            prices: DataFrame with price data
            volumes: Optional DataFrame with volume data
            
        Returns:
            DataFrame with engineered features
        """
        features = pd.DataFrame(index=prices.index)
        
        # Calculate returns
        returns = self.calculate_returns(prices)
        
        # Process each ticker
        for ticker in prices.columns:
            price = prices[ticker]
            
            # RSI
            features[f'{ticker}_rsi'] = self.calculate_rsi(price)
            
            # Volatility
            features[f'{ticker}_volatility'] = self.calculate_volatility(
                returns[ticker] if ticker in returns.columns else price.pct_change()
            )
            
            # Momentum
            features[f'{ticker}_momentum'] = self.calculate_momentum(price)
            
            # Moving averages
            features[f'{ticker}_ma_short'] = self.calculate_moving_average(
                price, self.ma_short
            )
            features[f'{ticker}_ma_long'] = self.calculate_moving_average(
                price, self.ma_long
            )
            
            # Price relative to MA
            features[f'{ticker}_price_ma_ratio'] = price / features[f'{ticker}_ma_short']
            
            # Volume features
            if volumes is not None and ticker in volumes.columns:
                features[f'{ticker}_volume_ratio'] = self.calculate_volume_ratio(
                    volumes[ticker]
                )
        
        # Aggregate features across all tickers
        feature_cols = [col for col in features.columns if '_rsi' in col]
        if feature_cols:
            features['avg_rsi'] = features[feature_cols].mean(axis=1)
            
        feature_cols = [col for col in features.columns if '_volatility' in col]
        if feature_cols:
            features['avg_volatility'] = features[feature_cols].mean(axis=1)
            
        feature_cols = [col for col in features.columns if '_momentum' in col]
        if feature_cols:
            features['avg_momentum'] = features[feature_cols].mean(axis=1)
        
        features = features.dropna()
        
        return features
    
    def normalize_features(
        self,
        features: pd.DataFrame,
        method: str = "zscore"
    ) -> pd.DataFrame:
        """
        Normalize features using specified method.
        
        Args:
            features: DataFrame with features
            method: Normalization method ("zscore" or "minmax")
            
        Returns:
            DataFrame with normalized features
        """
        if method == "zscore":
            return (features - features.mean()) / features.std()
        elif method == "minmax":
            return (features - features.min()) / (features.max() - features.min())
        else:
            logger.warning(f"Unknown normalization method: {method}")
            return features
    
    def handle_missing_data(
        self,
        data: pd.DataFrame,
        method: str = "forward_fill"
    ) -> pd.DataFrame:
        """
        Handle missing data in dataset.
        
        Args:
            data: DataFrame with data
            method: Method to handle missing data
            
        Returns:
            DataFrame with missing data handled
        """
        if method == "forward_fill":
            return data.ffill()
        elif method == "backward_fill":
            return data.bfill()
        elif method == "drop":
            return data.dropna()
        elif method == "interpolate":
            return data.interpolate(method='linear')
        else:
            logger.warning(f"Unknown method: {method}")
            return data


def create_features(
    prices: pd.DataFrame,
    volumes: Optional[pd.DataFrame] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Convenience function to create features.
    
    Args:
        prices: DataFrame with price data
        volumes: Optional DataFrame with volume data
        **kwargs: Additional arguments for DataProcessor
        
    Returns:
        DataFrame with engineered features
    """
    processor = DataProcessor(**kwargs)
    return processor.create_features(prices, volumes)