"""
Constants for Turkish Market Regime Detector
Extracted from original regime_detector.py
"""

# Regime labels for market states
REGIME_LABELS = {
    0: "Risk-On (Yüksek Risk)",
    1: "Carry Unwind (Taşıma Ters)",
    2: "Stagflation Sideways (Durgunluk)"
}

# Color mapping for regime visualization
REGIME_COLORS = {
    0: "#00FF00",  # Green - Risk-On
    1: "#FF0000",  # Red - Carry Unwind
    2: "#FFFF00"   # Yellow - Stagflation Sideways
}

# Default BIST100 tickers for analysis
DEFAULT_TICKERS = [
    "THYAO.IS", "EREGL.IS", "ASELS.IS", "SISE.IS", "KCHOL.IS",
    "AKBNK.IS", "GARAN.IS", "ISCTR.IS", "YKBNK.IS", "HALKB.IS",
    "BIMAS.IS", "SASA.IS", "KMPUR.IS", "PETKM.IS", "TUPRS.IS",
    "FROTO.IS", "SOKM.IS", "HEKTS.IS", "AKSA.IS", "ENKAI.IS"
]

# TCMB (Central Bank of Turkey) policy decisions
TCMB_POLICY_DECISIONS = [
    {"date": "2022-09-21", "rate_change": -100, "description": "Faiz indirimi - 100 bps"},
    {"date": "2022-10-20", "rate_change": -150, "description": "Faiz indirimi - 150 bps"},
    {"date": "2022-11-24", "rate_change": -150, "description": "Faiz indirimi - 150 bps"},
    {"date": "2022-12-22", "rate_change": -100, "description": "Faiz indirimi - 100 bps"},
    {"date": "2023-01-19", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2023-02-23", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2023-03-23", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2023-05-25", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2023-06-22", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2023-08-24", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2023-09-21", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2023-10-26", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2023-11-30", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2023-12-21", "rate_change": 250, "description": "Faiz artışı - 250 bps"},
    {"date": "2024-01-25", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-02-22", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-03-21", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-04-25", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-05-23", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-06-27", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-07-25", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-08-22", "rate_change": 0, "description": "Faiz sabit bırakıldı"},
    {"date": "2024-09-19", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2024-10-24", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2024-11-21", "rate_change": -50, "description": "Faiz indirimi - 50 bps"},
    {"date": "2024-12-19", "rate_change": -50, "description": "Faiz indirimi - 50 bps"}
]

# Feature engineering parameters
FEATURE_PARAMS = {
    "rsi_period": 14,
    "volatility_window": 20,
    "momentum_period": 10,
    "ma_short": 20,
    "ma_long": 50,
    "volume_ma_period": 20
}

# Model parameters
MODEL_PARAMS = {
    "kmeans_n_clusters": 3,
    "kmeans_random_state": 42,
    "hmm_n_components": 3,
    "hmm_random_state": 42,
    "hmm_n_iter": 100
}

# Visualization settings
PLOTLY_TEMPLATE = "plotly_dark"
DEFAULT_FIG_HEIGHT = 600
DEFAULT_FIG_WIDTH = 1000

# Data source settings
DATA_SOURCES = {
    "yfinance": {
        "default_period": "2y",
        "default_interval": "1d"
    },
    "evds": {
        "api_base_url": "https://evds.tcmb.gov.tr/service/evds/",
        "series_type": "BIY01"
    }
}

# Risk metrics thresholds
RISK_THRESHOLDS = {
    "rsi_oversold": 30,
    "rsi_overbought": 70,
    "volatility_high": 0.03,
    "volatility_low": 0.01,
    "momentum_strong": 0.05,
    "momentum_weak": -0.05
}
