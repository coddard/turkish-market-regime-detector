"""
Settings class for Turkish Market Regime Detector
Centralized configuration management
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class DataSourceConfig:
    """Configuration for data sources"""
    yfinance_period: str = "2y"
    yfinance_interval: str = "1d"
    evds_api_key: Optional[str] = None
    evds_series_type: str = "BIY01"
    use_cache: bool = True
    cache_ttl: int = 3600  # seconds


@dataclass
class ModelConfig:
    """Configuration for ML models"""
    kmeans_n_clusters: int = 3
    kmeans_random_state: int = 42
    kmeans_max_iter: int = 300
    kmeans_n_init: int = 10
    
    hmm_n_components: int = 3
    hmm_random_state: int = 42
    hmm_n_iter: int = 100
    hmm_covariance_type: str = "full"
    
    test_size: float = 0.2
    random_seed: int = 42


@dataclass
class FeatureConfig:
    """Configuration for feature engineering"""
    rsi_period: int = 14
    volatility_window: int = 20
    momentum_period: int = 10
    ma_short: int = 20
    ma_long: int = 50
    volume_ma_period: int = 20
    
    # Risk thresholds
    rsi_oversold: float = 30
    rsi_overbought: float = 70
    volatility_high: float = 0.03
    volatility_low: float = 0.01


@dataclass
class VisualizationConfig:
    """Configuration for visualizations"""
    template: str = "plotly_dark"
    fig_height: int = 600
    fig_width: int = 1000
    show_grid: bool = True
    export_html: bool = True
    export_path: str = "./visualizations"


@dataclass
class Settings:
    """
    Central settings class for the regime detector.
    Combines all configuration options in one place.
    """
    # Project info
    project_name: str = "Turkish Market Regime Detector"
    version: str = "2.0.0"
    author: str = "Giga Potato"
    
    # Data configuration
    data: DataSourceConfig = field(default_factory=DataSourceConfig)
    
    # Model configuration
    model: ModelConfig = field(default_factory=ModelConfig)
    
    # Feature configuration
    features: FeatureConfig = field(default_factory=FeatureConfig)
    
    # Visualization configuration
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)
    
    # Analysis settings
    default_tickers: List[str] = field(default_factory=lambda: [
        "THYAO.IS", "EREGL.IS", "ASELS.IS", "SISE.IS", "KCHOL.IS",
        "AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "HALKB.IS",
        "BIMAS.IS", "SASA.IS", "KMPUR.IS", "PETKM.IS", "TUPRS.IS",
        "FROTO.IS", "SOKM.IS", "HEKTS.IS", "AKSA.IS", "ENKAI.IS"
    ])
    
    # Analysis period
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    
    # Logging
    verbose: bool = True
    log_level: str = "INFO"
    
    # Output settings
    save_results: bool = True
    results_path: str = "./results"
    
    def __post_init__(self):
        """Set default dates if not provided"""
        if self.start_date is None:
            self.start_date = "2022-01-01"
        if self.end_date is None:
            self.end_date = datetime.now().strftime("%Y-%m-%d")
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "Settings":
        """Create Settings from dictionary"""
        return cls(**config_dict)
    
    def to_dict(self) -> dict:
        """Convert Settings to dictionary"""
        return {
            "project_name": self.project_name,
            "version": self.version,
            "data": {
                "yfinance_period": self.data.yfinance_period,
                "yfinance_interval": self.data.yfinance_interval,
                "evds_api_key": self.data.evds_api_key,
                "evds_series_type": self.data.evds_series_type,
                "use_cache": self.data.use_cache,
                "cache_ttl": self.data.cache_ttl
            },
            "model": {
                "kmeans_n_clusters": self.model.kmeans_n_clusters,
                "kmeans_random_state": self.model.kmeans_random_state,
                "hmm_n_components": self.model.hmm_n_components,
                "hmm_random_state": self.model.hmm_random_state
            },
            "features": {
                "rsi_period": self.features.rsi_period,
                "volatility_window": self.features.volatility_window,
                "momentum_period": self.features.momentum_period
            },
            "visualization": {
                "template": self.visualization.template,
                "fig_height": self.visualization.fig_height,
                "fig_width": self.visualization.fig_width
            }
        }


# Default settings instance
default_settings = Settings()
