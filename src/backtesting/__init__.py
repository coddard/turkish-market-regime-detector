"""
Backtesting module for regime-based trading strategies
Allows testing trading strategies based on detected market regimes
"""

from .engine import BacktestEngine, run_backtest
from .strategies import RegimeStrategy, MomentumStrategy

__all__ = [
    "BacktestEngine",
    "run_backtest",
    "RegimeStrategy",
    "MomentumStrategy"
]