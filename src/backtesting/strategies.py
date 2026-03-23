"""
Trading strategies for regime-based backtesting
"""

import pandas as pd
import numpy as np
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class RegimeStrategy:
    """
    Base class for regime-based trading strategies.
    """
    
    def __init__(self, long_regimes=None, short_regimes=None):
        """
        Initialize strategy.
        
        Args:
            long_regimes: List of regimes to go long
            short_regimes: List of regimes to go short
        """
        self.long_regimes = long_regimes or [0]  # Default: Risk-On
        self.short_regimes = short_regimes or [2]  # Default: Stagflation
        
    def generate_signals(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray
    ) -> np.ndarray:
        """
        Generate trading signals.
        
        Args:
            prices: Price data
            regimes: Regime labels
            
        Returns:
            Array of signals (1=long, 0=neutral, -1=short)
        """
        signals = np.zeros(len(regimes))
        
        for i, regime in enumerate(regimes):
            if regime in self.long_regimes:
                signals[i] = 1
            elif regime in self.short_regimes:
                signals[i] = -1
            else:
                signals[i] = 0
                
        return signals


class MomentumStrategy:
    """
    Momentum-based trading strategy.
    Goes long when momentum is positive, short when negative.
    """
    
    def __init__(self, lookback: int = 20, threshold: float = 0.0):
        """
        Initialize momentum strategy.
        
        Args:
            lookback: Lookback period for momentum calculation
            threshold: Threshold for signal generation
        """
        self.lookback = lookback
        self.threshold = threshold
        
    def generate_signals(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray = None
    ) -> np.ndarray:
        """
        Generate momentum-based signals.
        
        Args:
            prices: Price data
            regimes: Optional regime labels
            
        Returns:
            Array of signals
        """
        # Calculate momentum
        momentum = prices.pct_change(self.lookback)
        
        # Average momentum across all assets
        avg_momentum = momentum.mean(axis=1)
        
        # Generate signals
        signals = np.zeros(len(prices))
        signals[avg_momentum > self.threshold] = 1
        signals[avg_momentum < -self.threshold] = -1
        
        return signals


class MeanReversionStrategy:
    """
    Mean reversion strategy.
    Goes long when price is below average, short when above.
    """
    
    def __init__(self, lookback: int = 20, threshold: float = 1.5):
        """
        Initialize mean reversion strategy.
        
        Args:
            lookback: Lookback period
            threshold: Number of standard deviations
        """
        self.lookback = lookback
        self.threshold = threshold
        
    def generate_signals(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray = None
    ) -> np.ndarray:
        """
        Generate mean reversion signals.
        
        Args:
            prices: Price data
            regimes: Optional regime labels
            
        Returns:
            Array of signals
        """
        # Calculate z-score
        mean = prices.rolling(self.lookback).mean()
        std = prices.rolling(self.lookback).std()
        zscore = (prices - mean) / std
        
        # Average z-score
        avg_zscore = zscore.mean(axis=1)
        
        # Generate signals
        signals = np.zeros(len(prices))
        signals[avg_zscore < -self.threshold] = 1
        signals[avg_zscore > self.threshold] = -1
        
        return signals


class RegimeMomentumStrategy:
    """
    Combined regime and momentum strategy.
    Uses regime filters with momentum signals.
    """
    
    def __init__(
        self,
        regime_filter: bool = True,
        momentum_lookback: int = 20
    ):
        """
        Initialize combined strategy.
        
        Args:
            regime_filter: Whether to filter by regime
            momentum_lookback: Momentum lookback period
        """
        self.regime_filter = regime_filter
        self.momentum_lookback = momentum_lookback
        
    def generate_signals(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray
    ) -> np.ndarray:
        """
        Generate regime-filtered momentum signals.
        
        Args:
            prices: Price data
            regimes: Regime labels
            
        Returns:
            Array of signals
        """
        if self.regime_filter:
            # Only trade in Risk-On regime (0)
            base_signals = np.where(regimes == 0, 1, 0)
        else:
            base_signals = np.ones(len(regimes))
            
        # Apply momentum filter
        momentum = prices.pct_change(self.momentum_lookback)
        avg_momentum = momentum.mean(axis=1)
        
        # Combine signals
        signals = base_signals * np.sign(avg_momentum)
        
        return signals


class CarryTradeStrategy:
    """
    Carry trade strategy based on interest rate differentials.
    Long in high yield, short in low yield (simulated).
    """
    
    def __init__(self, yield_threshold: float = 0.02):
        """
        Initialize carry trade strategy.
        
        Args:
            yield_threshold: Minimum yield differential
        """
        self.yield_threshold = yield_threshold
        
    def generate_signals(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray,
        yields: Optional[pd.Series] = None
    ) -> np.ndarray:
        """
        Generate carry trade signals.
        Uses regime as proxy for carry opportunity.
        
        Args:
            prices: Price data
            regimes: Regime labels
            yields: Optional yield series
            
        Returns:
            Array of signals
        """
        # In Risk-On, carry trade is favorable
        # In Carry Unwind, it's unfavorable
        signals = np.zeros(len(regimes))
        
        for i, regime in enumerate(regimes):
            if regime == 0:  # Risk-On
                signals[i] = 1  # Long
            elif regime == 1:  # Carry Unwind
                signals[i] = -1  # Short
            else:
                signals[i] = 0  # Neutral
                
        return signals


# Strategy factory
def get_strategy(name: str, **kwargs) -> Callable:
    """
    Get strategy by name.
    
    Args:
        name: Strategy name
        **kwargs: Strategy parameters
        
    Returns:
        Strategy instance
    """
    strategies = {
        "regime": RegimeStrategy,
        "momentum": MomentumStrategy,
        "mean_reversion": MeanReversionStrategy,
        "regime_momentum": RegimeMomentumStrategy,
        "carry_trade": CarryTradeStrategy
    }
    
    if name not in strategies:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(strategies.keys())}")
        
    return strategies[name](**kwargs)