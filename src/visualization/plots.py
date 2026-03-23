"""
Plotting utilities for regime detection visualization
Creates interactive Plotly charts
"""

import pandas as pd
import numpy as np
from typing import Optional, Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

# Try to import plotly
try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("Plotly not available. Install with: pip install plotly")


class RegimePlotter:
    """
    Creates interactive visualizations for regime detection results.
    """
    
    # Default regime colors
    REGIME_COLORS = {
        0: "#00FF00",  # Green - Risk-On
        1: "#FF0000",  # Red - Carry Unwind
        2: "#FFFF00"   # Yellow - Stagflation
    }
    
    # Regime labels
    REGIME_LABELS = {
        0: "Risk-On",
        1: "Carry Unwind", 
        2: "Stagflation"
    }
    
    def __init__(
        self,
        template: str = "plotly_dark",
        height: int = 600,
        width: int = 1000
    ):
        """
        Initialize plotter.
        
        Args:
            template: Plotly template
            height: Default figure height
            width: Default figure width
        """
        if not PLOTLY_AVAILABLE:
            raise ImportError("Plotly is required for visualization")
            
        self.template = template
        self.height = height
        self.width = width
        
    def plot_prices_with_regimes(
        self,
        prices: pd.DataFrame,
        regimes: np.ndarray,
        title: str = "BIST100 Prices with Regime Detection"
    ) -> go.Figure:
        """
        Plot price data with regime overlay.
        
        Args:
            prices: Price DataFrame
            regimes: Regime labels
            title: Plot title
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Plot price lines for each ticker
        for col in prices.columns:
            fig.add_trace(go.Scatter(
                x=prices.index,
                y=prices[col],
                mode='lines',
                name=col,
                line=dict(width=1),
                opacity=0.7
            ))
        
        # Add regime background shading
        unique_regimes = np.unique(regimes)
        
        for regime in unique_regimes:
            mask = regimes == regime
            regime_dates = prices.index[mask]
            
            if len(regime_dates) > 0:
                fig.add_vrect(
                    x0=regime_dates[0],
                    x1=regime_dates[-1],
                    fillcolor=self.REGIME_COLORS.get(regime, "#888888"),
                    opacity=0.15,
                    layer="below",
                    line_width=0,
                    annotation_text=self.REGIME_LABELS.get(regime, f"Regime {regime}"),
                    annotation_position="top left"
                )
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Price",
            template=self.template,
            height=self.height,
            width=self.width,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        
        return fig
    
    def plot_regime_timeline(
        self,
        regimes: np.ndarray,
        dates: pd.DatetimeIndex,
        title: str = "Regime Timeline"
    ) -> go.Figure:
        """
        Plot regime timeline.
        
        Args:
            regimes: Regime labels
            dates: Date index
            title: Plot title
            
        Returns:
            Plotly figure
        """
        fig = go.Figure()
        
        # Create colored line for regimes
        fig.add_trace(go.Scatter(
            x=dates,
            y=regimes,
            mode='markers+lines',
            marker=dict(
                size=8,
                color=[self.REGIME_COLORS.get(r, "#888888") for r in regimes]
            ),
            line=dict(color='white', width=1),
            name="Regime"
        ))
        
        # Add regime labels as annotations
        unique_regimes = np.unique(regimes)
        
        for regime in unique_regimes:
            mask = regimes == regime
            regime_dates = dates[mask]
            
            if len(regime_dates) > 0:
                mid_idx = len(regime_dates) // 2
                fig.add_annotation(
                    x=regime_dates.iloc[mid_idx],
                    y=regime,
                    text=self.REGIME_LABELS.get(regime, f"Regime {regime}"),
                    showarrow=False,
                    font=dict(color=self.REGIME_COLORS.get(regime, "white"))
                )
        
        fig.update_layout(
            title=title,
            xaxis_title="Date",
            yaxis_title="Regime",
            yaxis=dict(
                tickmode='array',
                tickvals=list(unique_regimes),
                ticktext=[self.REGIME_LABELS.get(r, f"Regime {r}") for r in unique_regimes]
            ),
            template=self.template,
            height=self.height,
            width=self.width
        )
        
        return fig
    
    def plot_transition_matrix(
        self,
        transition_matrix: pd.DataFrame,
        title: str = "Regime Transition Matrix"
    ) -> go.Figure:
        """
        Plot regime transition matrix as heatmap.
        
        Args:
            transition_matrix: Transition probability matrix
            title: Plot title
            
        Returns:
            Plotly figure
        """
        fig = go.Figure(data=go.Heatmap(
            z=transition_matrix.values,
            x=[self.REGIME_LABELS.get(i, f"Regime {i}") for i in transition_matrix.columns],
            y=[self.REGIME_LABELS.get(i, f"Regime {i}") for i in transition_matrix.index],
            colorscale='RdYlGn',
            text=np.round(transition_matrix.values, 3),
            texttemplate='%{text}',
            showscale=True
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="To Regime",
            yaxis_title="From Regime",
            template=self.template,
            height=self.height,
            width=self.width
        )
        
        return fig
    
    def plot_regime_distribution(
        self,
        regimes: np.ndarray,
        title: str = "Regime Distribution"
    ) -> go.Figure:
        """
        Plot regime distribution pie chart.
        
        Args:
            regimes: Regime labels
            title: Plot title
            
        Returns:
            Plotly figure
        """
        unique, counts = np.unique(regimes, return_counts=True)
        
        labels = [self.REGIME_LABELS.get(u, f"Regime {u}") for u in unique]
        colors = [self.REGIME_COLORS.get(u, "#888888") for u in unique]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=counts,
            marker=dict(colors=colors),
            textinfo='label+percent',
            hole=0.3
        )])
        
        fig.update_layout(
            title=title,
            template=self.template,
            height=self.height,
            width=self.width
        )
        
        return fig
    
    def plot_feature_heatmap(
        self,
        features: pd.DataFrame,
        regimes: np.ndarray,
        title: str = "Feature Heatmap by Regime"
    ) -> go.Figure:
        """
        Plot feature averages by regime as heatmap.
        
        Args:
            features: Feature DataFrame
            regimes: Regime labels
            title: Plot title
            
        Returns:
            Plotly figure
        """
        # Calculate mean features by regime
        regime_means = pd.DataFrame()
        
        for regime in np.unique(regimes):
            mask = regimes == regime
            regime_features = features[mask].mean()
            regime_means[self.REGIME_LABELS.get(regime, f"Regime {regime}")] = regime_features
        
        # Normalize for better visualization
        regime_means_norm = (regime_means - regime_means.min()) / (regime_means.max() - regime_means.min() + 1e-10)
        
        fig = go.Figure(data=go.Heatmap(
            z=regime_means_norm.values,
            x=regime_means.columns,
            y=regime_means.index,
            colorscale='Viridis',
            showscale=True
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Regime",
            yaxis_title="Feature",
            template=self.template,
            height=self.height,
            width=self.width
        )
        
        return fig
    
    def plot_sector_performance(
        self,
        returns: pd.DataFrame,
        regimes: np.ndarray,
        title: str = "Sector Performance by Regime"
    ) -> go.Figure:
        """
        Plot sector/asset performance by regime.
        
        Args:
            returns: Returns DataFrame
            regimes: Regime labels
            title: Plot title
            
        Returns:
            Plotly figure
        """
        # Calculate mean returns by regime
        regime_returns = {}
        
        for regime in np.unique(regimes):
            mask = regimes == regime
            regime_returns[self.REGIME_LABELS.get(regime, f"Regime {regime}")] = returns[mask].mean()
        
        regime_df = pd.DataFrame(regime_returns)
        
        fig = go.Figure()
        
        for col in regime_df.columns:
            fig.add_trace(go.Bar(
                name=col,
                x=regime_df.index,
                y=regime_df[col]
            ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Regime",
            yaxis_title="Average Return",
            barmode='group',
            template=self.template,
            height=self.height,
            width=self.width
        )
        
        return fig
    
    def create_dashboard(
        self,
        prices: pd.DataFrame,
        features: pd.DataFrame,
        regimes: np.ndarray,
        transition_matrix: Optional[pd.DataFrame] = None
    ) -> go.Figure:
        """
        Create comprehensive dashboard.
        
        Args:
            prices: Price DataFrame
            features: Feature DataFrame
            regimes: Regime labels
            transition_matrix: Optional transition matrix
            
        Returns:
            Plotly figure with subplots
        """
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Prices with Regimes",
                "Regime Timeline",
                "Regime Distribution",
                "Transition Matrix" if transition_matrix is not None else "Feature Heatmap"
            ),
            specs=[
                [{"type": "scatter"}, {"type": "scatter"}],
                [{"type": "pie"}, {"type": "heatmap"}]
            ],
            vertical_spacing=0.15,
            horizontal_spacing=0.1
        )
        
        # Prices with regimes
        for col in prices.columns:
            fig.add_trace(
                go.Scatter(
                    x=prices.index,
                    y=prices[col],
                    mode='lines',
                    name=col,
                    line=dict(width=1),
                    opacity=0.7,
                    showlegend=False
                ),
                row=1, col=1
            )
        
        # Regime timeline
        fig.add_trace(
            go.Scatter(
                x=prices.index,
                y=regimes,
                mode='markers+lines',
                marker=dict(
                    size=6,
                    color=[self.REGIME_COLORS.get(r, "#888888") for r in regimes]
                ),
                line=dict(color='white', width=1),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Distribution pie chart
        unique, counts = np.unique(regimes, return_counts=True)
        fig.add_trace(
            go.Pie(
                labels=[self.REGIME_LABELS.get(u, f"Regime {u}") for u in unique],
                values=counts,
                marker=dict(colors=[self.REGIME_COLORS.get(u, "#888888") for u in unique]),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Transition matrix or feature heatmap
        if transition_matrix is not None:
            fig.add_trace(
                go.Heatmap(
                    z=transition_matrix.values,
                    colorscale='RdYlGn',
                    showscale=False
                ),
                row=2, col=2
            )
        else:
            # Use feature heatmap as fallback
            regime_means = pd.DataFrame()
            for regime in np.unique(regimes):
                mask = regimes == regime
                regime_means[self.REGIME_LABELS.get(regime, f"Regime {regime}")] = features[mask].mean()
            
            fig.add_trace(
                go.Heatmap(
                    z=regime_means.values,
                    colorscale='Viridis',
                    showscale=False,
                    x=regime_means.columns,
                    y=regime_means.index
                ),
                row=2, col=2
            )
        
        fig.update_layout(
            title="Regime Detection Dashboard",
            template=self.template,
            height=self.height * 2,
            width=self.width
        )
        
        return fig


def create_regime_plot(
    data_type: str,
    *args,
    **kwargs
) -> go.Figure:
    """
    Convenience function to create specific plot types.
    
    Args:
        data_type: Type of plot ("prices", "timeline", "transition", "distribution", "heatmap")
        *args: Arguments for specific plot
        **kwargs: Keyword arguments
        
    Returns:
        Plotly figure
    """
    plotter = RegimePlotter()
    
    plot_types = {
        "prices": plotter.plot_prices_with_regimes,
        "timeline": plotter.plot_regime_timeline,
        "transition": plotter.plot_transition_matrix,
        "distribution": plotter.plot_regime_distribution,
        "heatmap": plotter.plot_feature_heatmap,
        "sector": plotter.plot_sector_performance
    }
    
    if data_type not in plot_types:
        raise ValueError(f"Unknown plot type: {data_type}")
    
    return plot_types[data_type](*args, **kwargs)