"""
Turkish Market Regime Detector
Market regime detection for BIST100 using KMeans & HMM
Integrated with TCMB monetary policy data

Version 2.0 - Modular Structure
"""

__version__ = "2.0.0"
__author__ = "Giga Potato"
__license__ = "MIT"

# Configuration
from .config.settings import Settings
from .config.constants import (
    REGIME_LABELS,
    REGIME_COLORS,
    DEFAULT_TICKERS,
    TCMB_POLICY_DECISIONS,
    FEATURE_PARAMS,
    MODEL_PARAMS,
    PLOTLY_TEMPLATE,
    RISK_THRESHOLDS
)

# Data fetching
from .data.yfinance_fetcher import YFinanceFetcher, fetch_yfinance_data
from .data.evds_fetcher import EVDSFetcher, fetch_evds_data
from .data.processor import DataProcessor, create_features

# Models
from .models.base import RegimeModelBase
from .models.kmeans_model import KMeansRegimeModel, train_kmeans
from .models.hmm_model import HMMRegimeModel, train_hmm

# Visualization
from .visualization.plots import RegimePlotter, create_regime_plot
from .visualization.export import export_plot, save_all_plots, export_results

__all__ = [
    # Version
    "__version__",
    
    # Config
    "Settings",
    "REGIME_LABELS",
    "REGIME_COLORS", 
    "DEFAULT_TICKERS",
    "TCMB_POLICY_DECISIONS",
    "FEATURE_PARAMS",
    "MODEL_PARAMS",
    "PLOTLY_TEMPLATE",
    "RISK_THRESHOLDS",
    
    # Data
    "YFinanceFetcher",
    "fetch_yfinance_data",
    "EVDSFetcher",
    "fetch_evds_data",
    "DataProcessor",
    "create_features",
    
    # Models
    "RegimeModelBase",
    "KMeansRegimeModel",
    "train_kmeans",
    "HMMRegimeModel",
    "train_hmm",
    
    # Visualization
    "RegimePlotter",
    "create_regime_plot",
    "export_plot",
    "save_all_plots",
    "export_results"
]


# Backward compatibility with old API
def run_analysis(tickers=None, period="2y", n_regimes=3, use_hmm=False):
    """
    Backward compatible analysis function.
    
    Args:
        tickers: List of tickers (default: DEFAULT_TICKERS)
        period: Data period
        n_regimes: Number of regimes
        use_hmm: Use HMM instead of K-Means
        
    Returns:
        Dictionary with results
    """
    if tickers is None:
        tickers = DEFAULT_TICKERS
    
    # Fetch data
    fetcher = YFinanceFetcher(period=period)
    prices = fetcher.fetch_multiple_tickers(tickers)
    
    # Create features
    processor = DataProcessor()
    features = processor.create_features(prices)
    features_norm = processor.normalize_features(features)
    
    # Train model
    if use_hmm:
        model = HMMRegimeModel(n_regimes=n_regimes)
    else:
        model = KMeansRegimeModel(n_regimes=n_regimes)
    
    model.fit(features_norm)
    regimes = model.predict(features_norm)
    
    # Get transition matrix
    if hasattr(model, 'get_transition_matrix'):
        transition_matrix = model.get_transition_matrix()
    else:
        transition_matrix = None
    
    return {
        "prices": prices,
        "features": features,
        "regimes": regimes,
        "model": model,
        "transition_matrix": transition_matrix
    }