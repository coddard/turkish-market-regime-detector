"""
Backtesting engine for regime-based trading strategies
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Trade:
    """Trade record"""
    entry_date: str
    entry_price: float
    exit_date: Optional[str] = None
    exit_price: Optional[float] = None
    position: str = "long"  # "long" or "short"
    pnl: float = 0.0


@dataclass
class BacktestResult:
    """Backtest result summary"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    total_return: float
    annual_return: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    avg_win: float
    avg_loss: float
    trades: List[Trade]


class BacktestEngine:
    """
    Engine for backtesting regime-based strategies.
    """
    
    def __init__(
        self,
        initial_capital: float = 100000.0,
        commission: float = 0.001,
        slippage: float = 0.0005
    ):
        """
        Initialize backtest engine.
        
        Args:
            initial_capital: Starting capital
            commission: Commission rate (e.g., 0.001 = 0.1%)
            slippage: Slippage rate
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.trades: List[Trade] = []
        self.portfolio_value = initial_capital
        
    def run_strategy(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray,
        strategy_func
    ) -> BacktestResult:
        """
        Run backtest with given strategy.
        
        Args:
            prices: Price data
            regimes: Regime labels
            strategy_func: Function that returns signals
            
        Returns:
            BacktestResult
        """
        self.trades = []
        self.portfolio_value = self.initial_capital
        
        # Get signals from strategy
        signals = strategy_func(prices, regimes)
        
        # Simulate trading
        position = 0  # 0 = no position, 1 = long, -1 = short
        entry_price = 0
        
        for i in range(len(prices) - 1):
            date = prices.index[i]
            price = prices.iloc[i]['Close'] if 'Close' in prices.columns else prices.iloc[i].mean()
            
            signal = signals[i]
            
            # Entry signal
            if signal == 1 and position == 0:
                # Buy/Long
                entry_price = price * (1 + self.slippage)
                entry_price += entry_price * self.commission
                position = 1
                trade = Trade(
                    entry_date=str(date.date()),
                    entry_price=entry_price,
                    position="long"
                )
                self.trades.append(trade)
                
            elif signal == -1 and position == 0:
                # Sell/Short
                entry_price = price * (1 - self.slippage)
                entry_price -= entry_price * self.commission
                position = -1
                trade = Trade(
                    entry_date=str(date.date()),
                    entry_price=entry_price,
                    position="short"
                )
                self.trades.append(trade)
                
            # Exit signal or end of data
            elif (signal == 0 and position != 0) or (i == len(prices) - 2):
                if position != 0:
                    exit_price = price * (1 - self.slippage) if position == 1 else price * (1 + self.slippage)
                    exit_price -= exit_price * self.commission
                    
                    # Calculate PnL
                    if position == 1:
                        pnl = (exit_price - entry_price) / entry_price
                    else:
                        pnl = (entry_price - exit_price) / entry_price
                    
                    # Update portfolio
                    self.portfolio_value *= (1 + pnl)
                    
                    # Update trade
                    self.trades[-1].exit_date = str(date.date())
                    self.trades[-1].exit_price = exit_price
                    self.trades[-1].pnl = pnl
                    
                    position = 0
        
        # Calculate metrics
        return self._calculate_metrics(prices.index)
    
    def _calculate_metrics(self, dates) -> BacktestResult:
        """Calculate backtest metrics"""
        winning_trades = [t for t in self.trades if t.pnl > 0]
        losing_trades = [t for t in self.trades if t.pnl <= 0]
        
        total_return = (self.portfolio_value - self.initial_capital) / self.initial_capital
        
        # Annual return (assuming 252 trading days)
        n_years = len(dates) / 252
        annual_return = (1 + total_return) ** (1 / n_years) - 1 if n_years > 0 else 0
        
        # Sharpe ratio (simplified)
        if winning_trades and losing_trades:
            returns = [t.pnl for t in self.trades]
            sharpe = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
        else:
            sharpe = 0
        
        # Max drawdown
        cumulative = self._calculate_cumulative_returns()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()
        
        return BacktestResult(
            total_trades=len(self.trades),
            winning_trades=len(winning_trades),
            losing_trades=len(losing_trades),
            total_return=total_return,
            annual_return=annual_return,
            sharpe_ratio=sharpe,
            max_drawdown=max_drawdown,
            win_rate=len(winning_trades) / len(self.trades) if self.trades else 0,
            avg_win=np.mean([t.pnl for t in winning_trades]) if winning_trades else 0,
            avg_loss=np.mean([t.pnl for t in losing_trades]) if losing_trades else 0,
            trades=self.trades
        )
    
    def _calculate_cumulative_returns(self) -> pd.Series:
        """Calculate cumulative returns"""
        returns = []
        value = self.initial_capital
        
        for trade in self.trades:
            if trade.pnl != 0:
                value *= (1 + trade.pnl)
                returns.append(value)
        
        return pd.Series(returns)
    
    def get_results_dataframe(self) -> pd.DataFrame:
        """Get trades as DataFrame"""
        if not self.trades:
            return pd.DataFrame()
            
        return pd.DataFrame([
            {
                'entry_date': t.entry_date,
                'exit_date': t.exit_date,
                'position': t.position,
                'entry_price': t.entry_price,
                'exit_price': t.exit_price,
                'pnl': t.pnl,
                'pnl_pct': f"{t.pnl * 100:.2f}%"
            }
            for t in self.trades
        ])


def run_backtest(
    prices: pd.DataFrame,
    regimes: np.ndarray,
    strategy: str = "regime",
    initial_capital: float = 100000.0
) -> BacktestResult:
    """
    Convenience function to run backtest.
    
    Args:
        prices: Price DataFrame
        regimes: Regime labels
        strategy: Strategy name ("regime", "momentum", "buy_hold")
        initial_capital: Starting capital
        
    Returns:
        BacktestResult
    """
    engine = BacktestEngine(initial_capital=initial_capital)
    
    if strategy == "regime":
        # Buy in Risk-On, sell in others
        def regime_strategy(prices, regimes):
            signals = np.zeros(len(regimes))
            for i in range(len(regimes)):
                if regimes[i] == 0:  # Risk-On
                    signals[i] = 1
                elif regimes[i] == 2:  # Stagflation
                    signals[i] = -1
                else:
                    signals[i] = 0
            return signals
            
        return engine.run_strategy(prices, regimes, regime_strategy)
        
    elif strategy == "momentum":
        # Buy when momentum is positive
        def momentum_strategy(prices, regimes):
            returns = prices.pct_change()
            signals = np.sign(returns.mean(axis=1))
            return signals.fillna(0).values
            
        return engine.run_strategy(prices, regimes, momentum_strategy)
        
    elif strategy == "buy_hold":
        # Always hold
        def buy_hold_strategy(prices, regimes):
            return np.ones(len(regimes))
            
        return engine.run_strategy(prices, regimes, buy_hold_strategy)
        
    else:
        raise ValueError(f"Unknown strategy: {strategy}")


def print_backtest_results(result: BacktestResult):
    """Print backtest results in readable format"""
    print("\n" + "="*50)
    print("BACKTEST SONUÇLARI")
    print("="*50)
    print(f"Toplam İşlem: {result.total_trades}")
    print(f"Kazanan: {result.winning_trades}")
    print(f"Kaybeden: {result.losing_trades}")
    print(f"Win Rate: {result.win_rate:.2%}")
    print(f"Ortalama Kazanç: {result.avg_win:.2%}")
    print(f"Ortalama Kayıp: {result.avg_loss:.2%}")
    print("-"*50)
    print(f"Toplam Getiri: {result.total_return:.2%}")
    print(f"Yıllık Getiri: {result.annual_return:.2%}")
    print(f"Sharpe Oranı: {result.sharpe_ratio:.2f}")
    print(f"Max Drawdown: {result.max_drawdown:.2%}")
    print("="*50)