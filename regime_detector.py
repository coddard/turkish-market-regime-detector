#!/usr/bin/env python3
"""
BIST100 Rejim Tespiti + TCMB Politika Entegrasyonu
Author: Giga Potato
Description: Market regime detection for BIST100 using KMeans & HMM, integrated with TCMB monetary policy data
"""

import os
import sys
import time
import datetime
from typing import Tuple, Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Try-except blocks for library imports
try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(f"Error importing pandas/numpy: {e}")
    print("Installing pandas and numpy...")
    os.system(f"{sys.executable} -m pip install pandas numpy")
    import pandas as pd
    import numpy as np

try:
    import yfinance as yf
except ImportError as e:
    print(f"Error importing yfinance: {e}")
    print("Installing yfinance...")
    os.system(f"{sys.executable} -m pip install yfinance")
    import yfinance as yf

try:
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score, confusion_matrix, cohen_kappa_score
except ImportError as e:
    print(f"Error importing scikit-learn: {e}")
    print("Installing scikit-learn...")
    os.system(f"{sys.executable} -m pip install scikit-learn")
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score, confusion_matrix, cohen_kappa_score

try:
    from hmmlearn.hmm import GaussianHMM
except ImportError as e:
    print(f"Error importing hmmlearn: {e}")
    print("Installing hmmlearn...")
    os.system(f"{sys.executable} -m pip install hmmlearn")
    from hmmlearn.hmm import GaussianHMM

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
except ImportError as e:
    print(f"Error importing matplotlib/seaborn: {e}")
    print("Installing matplotlib and seaborn...")
    os.system(f"{sys.executable} -m pip install matplotlib seaborn")
    import matplotlib.pyplot as plt
    import seaborn as sns

try:
    import plotly.graph_objects as go
    import plotly.express as px
except ImportError as e:
    print(f"Error importing plotly: {e}")
    print("Installing plotly...")
    os.system(f"{sys.executable} -m pip install plotly")
    import plotly.graph_objects as go
    import plotly.express as px

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Error importing requests/BeautifulSoup: {e}")
    print("Installing requests and beautifulsoup4...")
    os.system(f"{sys.executable} -m pip install requests beautifulsoup4")
    import requests
    from bs4 import BeautifulSoup

# Environment variables (from .env file)
try:
    from dotenv import load_dotenv
    load_dotenv()
    EVDS_KEY = os.getenv("EVDS_KEY")
except ImportError:
    print("dotenv not installed, using manual input")
    EVDS_KEY = "eIemA4MUnI"  # Default key for demo purposes

# Global constants
REGIME_LABELS = {
    0: "Risk-On",
    1: "Carry Unwind", 
    2: "Stagflation Sideways"
}

REGIME_COLORS = {
    "Risk-On": "#10b981",  # Green
    "Carry Unwind": "#ef4444",  # Red
    "Stagflation Sideways": "#3b82f6"  # Blue
}

# TCMB PPK Kararları (2020-2025)
TCMB_POLICY_DECISIONS = [
    {"date": "2020-01-16", "policy_rate": 12.00, "change_bps": 0},
    {"date": "2020-02-20", "policy_rate": 11.25, "change_bps": -75},
    {"date": "2020-03-19", "policy_rate": 9.75, "change_bps": -150},
    {"date": "2020-04-23", "policy_rate": 8.25, "change_bps": -150},
    {"date": "2020-05-21", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-06-18", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-07-23", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-08-27", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-09-24", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-10-22", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-11-19", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2020-12-17", "policy_rate": 8.25, "change_bps": 0},
    {"date": "2021-01-21", "policy_rate": 17.00, "change_bps": 875},
    {"date": "2021-02-18", "policy_rate": 17.00, "change_bps": 0},
    {"date": "2021-03-18", "policy_rate": 19.00, "change_bps": 200},
    {"date": "2021-04-15", "policy_rate": 19.00, "change_bps": 0},
    {"date": "2021-05-13", "policy_rate": 19.00, "change_bps": 0},
    {"date": "2021-06-17", "policy_rate": 19.00, "change_bps": 0},
    {"date": "2021-07-22", "policy_rate": 19.00, "change_bps": 0},
    {"date": "2021-08-19", "policy_rate": 19.00, "change_bps": 0},
    {"date": "2021-09-23", "policy_rate": 18.00, "change_bps": -100},
    {"date": "2021-10-21", "policy_rate": 16.00, "change_bps": -200},
    {"date": "2021-11-18", "policy_rate": 15.00, "change_bps": -100},
    {"date": "2021-12-16", "policy_rate": 14.00, "change_bps": -100},
    {"date": "2022-01-20", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-02-17", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-03-17", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-04-14", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-05-26", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-06-23", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-07-21", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-08-25", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-09-22", "policy_rate": 14.00, "change_bps": 0},
    {"date": "2022-10-27", "policy_rate": 15.00, "change_bps": 100},
    {"date": "2022-11-24", "policy_rate": 24.00, "change_bps": 900},
    {"date": "2022-12-22", "policy_rate": 9.00, "change_bps": -1500},
    {"date": "2023-01-19", "policy_rate": 9.00, "change_bps": 0},
    {"date": "2023-02-23", "policy_rate": 9.00, "change_bps": 0},
    {"date": "2023-03-23", "policy_rate": 8.50, "change_bps": -50},
    {"date": "2023-04-27", "policy_rate": 8.50, "change_bps": 0},
    {"date": "2023-05-25", "policy_rate": 8.50, "change_bps": 0},
    {"date": "2023-06-22", "policy_rate": 8.50, "change_bps": 0},
    {"date": "2023-07-20", "policy_rate": 15.00, "change_bps": 650},
    {"date": "2023-08-24", "policy_rate": 25.00, "change_bps": 1000},
    {"date": "2023-09-21", "policy_rate": 30.00, "change_bps": 500},
    {"date": "2023-10-26", "policy_rate": 35.00, "change_bps": 500},
    {"date": "2023-11-23", "policy_rate": 40.00, "change_bps": 500},
    {"date": "2023-12-21", "policy_rate": 42.50, "change_bps": 250},
    {"date": "2024-01-18", "policy_rate": 45.00, "change_bps": 250},
    {"date": "2024-02-15", "policy_rate": 45.00, "change_bps": 0},
    {"date": "2024-03-21", "policy_rate": 42.50, "change_bps": -250},
    {"date": "2024-04-18", "policy_rate": 40.00, "change_bps": -250},
    {"date": "2024-05-23", "policy_rate": 37.50, "change_bps": -250},
    {"date": "2024-06-20", "policy_rate": 35.00, "change_bps": -250},
    {"date": "2024-07-18", "policy_rate": 32.50, "change_bps": -250},
    {"date": "2024-08-22", "policy_rate": 30.00, "change_bps": -250},
    {"date": "2024-09-19", "policy_rate": 27.50, "change_bps": -250},
    {"date": "2024-10-24", "policy_rate": 25.00, "change_bps": -250},
    {"date": "2024-11-21", "policy_rate": 22.50, "change_bps": -250},
    {"date": "2024-12-19", "policy_rate": 20.00, "change_bps": -250},
    {"date": "2025-01-16", "policy_rate": 17.50, "change_bps": -250}
]

def fetch_yfinance_data(
    tickers: List[str],
    period: str = "5y",
    interval: str = "1d",
    max_retries: int = 3
) -> Dict[str, pd.DataFrame]:
    """
    Fetches historical price data from Yahoo Finance with retry mechanism.
    
    Args:
        tickers: List of tickers to fetch
        period: Data period (e.g., "5y" for 5 years)
        interval: Data interval (e.g., "1d" for daily)
        max_retries: Maximum number of retry attempts
    
    Returns:
        Dictionary of DataFrames with price data
    """
    data = {}
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        
        for attempt in range(max_retries):
            try:
                df = yf.download(ticker, period=period, interval=interval)
                
                if df.empty:
                    raise ValueError(f"Empty data for {ticker}")
                
                # Check and handle NaNs
                na_count = df.isna().sum().sum()
                if na_count > 0:
                    print(f"Warning: {na_count} NaN values found in {ticker} data")
                    df = df.fillna(method='ffill').fillna(method='bfill')
                
                data[ticker] = df
                print(f"Successfully fetched {len(df)} records for {ticker}")
                time.sleep(0.5)  # Rate limiting
                break
            
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed for {ticker}: {e}")
                if attempt == max_retries - 1:
                    print(f"Failed to fetch data for {ticker}")
                    data[ticker] = pd.DataFrame()
                time.sleep(2)  # Wait before retrying
    
    return data

def fetch_evds_data(
    api_key: str,
    start_date: str = "01-01-2020",
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetches TCMB policy rate data from EVDS API.
    
    Args:
        api_key: EVDS API key from https://evds2.tcmb.gov.tr/
        start_date: Start date in DD-MM-YYYY format
        end_date: End date in DD-MM-YYYY format (defaults to today)
    
    Returns:
        DataFrame with policy rate data
    """
    if end_date is None:
        end_date = datetime.datetime.now().strftime("%d-%m-%Y")
    
    url = (
        f"https://evds2.tcmb.gov.tr/service/evds/"
        f"?type=json&key={api_key}"
        f"&dataGroup=TP.MK.PRK&freq=d"
        f"&startDate={start_date}&endDate={end_date}"
    )
    
    try:
        print("Fetching TCMB policy rate data from EVDS...")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            
            if "items" in data:
                df = pd.DataFrame(data["items"])
                df["Tarih"] = pd.to_datetime(df["Tarih"], format="%d-%m-%Y")
                df = df.set_index("Tarih")
                df.columns = ["policy_rate"]
                df["policy_rate"] = pd.to_numeric(df["policy_rate"], errors="coerce")
                
                # Forward fill to get daily frequency
                df = df.asfreq("D").ffill()
                
                print(f"Successfully fetched {len(df)} policy rate records")
                return df
            else:
                print("Warning: No data items found in EVDS response")
                return pd.DataFrame()
        
        else:
            print(f"Error fetching EVDS data: Status code {response.status_code}")
            print(f"Response: {response.text}")
            return pd.DataFrame()
    
    except Exception as e:
        print(f"Error fetching EVDS data: {e}")
        
        # Fallback to hardcoded data if API fails
        print("Using hardcoded TCMB policy rate data...")
        policy_df = pd.DataFrame(TCMB_POLICY_DECISIONS)
        policy_df["date"] = pd.to_datetime(policy_df["date"])
        policy_df = policy_df.set_index("date")[["policy_rate"]]
        policy_df = policy_df.asfreq("D").ffill()
        
        return policy_df

def calculate_rsi(prices: pd.Series, window: int = 14) -> pd.Series:
    """
    Calculates Relative Strength Index (RSI).
    
    Args:
        prices: Price series
        window: Lookback period
    
    Returns:
        RSI series
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def create_features(
    price_data: Dict[str, pd.DataFrame],
    policy_data: pd.DataFrame
) -> pd.DataFrame:
    """
    Creates features for regime detection.
    
    Args:
        price_data: Dictionary of price data DataFrames
        policy_data: Policy rate DataFrame
    
    Returns:
        Features DataFrame
    """
    print("Creating features...")
    
    # Check required tickers are available
    required_tickers = ["XU100.IS", "XBANK.IS", "XUSIN.IS", "USDTRY=X", "EEM"]
    for ticker in required_tickers:
        if ticker not in price_data or price_data[ticker].empty:
            raise ValueError(f"Gerekli hisse senedi verisi bulunamadı: {ticker}")
    
    # Get closing prices (ensure they're 1D)
    bist_close = price_data["XU100.IS"]["Close"].squeeze() if "Close" in price_data["XU100.IS"].columns else price_data["XU100.IS"].squeeze()
    banka_close = price_data["XBANK.IS"]["Close"].squeeze() if "Close" in price_data["XBANK.IS"].columns else price_data["XBANK.IS"].squeeze()
    sinai_close = price_data["XUSIN.IS"]["Close"].squeeze() if "Close" in price_data["XUSIN.IS"].columns else price_data["XUSIN.IS"].squeeze()
    usdtry_close = price_data["USDTRY=X"]["Close"].squeeze() if "Close" in price_data["USDTRY=X"].columns else price_data["USDTRY=X"].squeeze()
    eem_close = price_data["EEM"]["Close"].squeeze() if "Close" in price_data["EEM"].columns else price_data["EEM"].squeeze()
    
    # Handle gold data - use USDTRY as proxy if gold not available
    if "GOLDS.IS" in price_data and not price_data["GOLDS.IS"].empty and "Close" in price_data["GOLDS.IS"].columns:
        gold_close = price_data["GOLDS.IS"]["Close"].squeeze()
    else:
        print("Warning: GOLDS.IS data not available, using USDTRY as proxy")
        gold_close = pd.Series(index=bist_close.index, data=0)
    
    # Create features DataFrame with common dates
    features = pd.DataFrame({
        "bist_close": bist_close,
        "banka_close": banka_close, 
        "sinai_close": sinai_close,
        "usdtry_close": usdtry_close,
        "gold_close": gold_close,
        "eem_close": eem_close
    }).dropna()
    
    # Check if we have data to work with
    if len(features) == 0:
        raise ValueError("Yeterli sayıda veri noktası bulunamadı.")
    
    # Calculate returns
    features["bist_return"] = features["bist_close"].pct_change() * 100
    features["banka_return"] = features["banka_close"].pct_change() * 100
    features["sinai_return"] = features["sinai_close"].pct_change() * 100
    features["usdtry_change"] = features["usdtry_close"].pct_change() * 100
    features["msci_em_alpha"] = features["bist_return"] - features["eem_close"].pct_change() * 100
    
    # Volatility (21-day realized)
    features["bist_volatility"] = features["bist_return"].rolling(window=21).std() * np.sqrt(252)
    features["usdtry_volatility"] = features["usdtry_change"].rolling(window=21).std() * np.sqrt(252)
    
    # RSI
    features["rsi"] = calculate_rsi(features["bist_close"])
    
    # Moving average ratio
    features["ma50"] = features["bist_close"].rolling(window=50).mean()
    features["ma200"] = features["bist_close"].rolling(window=200).mean()
    features["ma_ratio"] = features["ma50"] / features["ma200"]
    
    # Policy rate features
    policy_data = policy_data.reindex(features.index).ffill()
    features["policy_rate"] = policy_data["policy_rate"]
    features["rate_momentum"] = features["policy_rate"].diff(63)  # 3-month momentum
    features["real_return"] = features["bist_return"] - features["policy_rate"].pct_change() * 100
    
    # Drop NaNs from rolling calculations
    features = features.dropna()
    
    print(f"Created {len(features)} feature vectors with {len(features.columns)} features")
    print(f"NaN values after cleaning: {features.isna().sum().sum()}")
    
    return features

def train_kmeans(
    features: pd.DataFrame,
    features_list: Optional[List[str]] = None,
    n_clusters: int = 3,
    random_state: int = 42
) -> Tuple[KMeans, pd.DataFrame, pd.Series]:
    """
    Trains KMeans model for regime detection.
    
    Args:
        features: Features DataFrame
        features_list: List of features to use (defaults to all numeric features)
        n_clusters: Number of clusters
        random_state: Random state
    
    Returns:
        Trained KMeans model, scaled features, regime labels
    """
    print("Training KMeans model...")
    
    if features_list is None:
        # Use selected features for clustering
        features_list = [
            "bist_return", "bist_volatility", "usdtry_change", 
            "usdtry_volatility", "rsi", "ma_ratio", "rate_momentum", "real_return"
        ]
    
    # Check if we have data to train on
    if len(features) == 0:
        raise ValueError("Eğitim için yeterli veri noktası bulunamadı.")
    
    # Check if all required features are present
    missing_features = [f for f in features_list if f not in features.columns]
    if missing_features:
        raise ValueError(f"Eksik özellikler: {', '.join(missing_features)}")
    
    # Scale features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features[features_list])
    
    # Train KMeans
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=10
    )
    kmeans.fit(scaled_features)
    
    # Calculate cluster quality
    silhouette = silhouette_score(scaled_features, kmeans.labels_)
    print(f"KMeans Silhouette Score: {silhouette:.3f}")
    
    # Label clusters based on characteristics
    regime_labels = pd.Series(kmeans.labels_, index=features.index, name="kmeans_regime")
    regime_means = features.groupby(regime_labels)[features_list].mean()
    
    # Determine regime types
    regime_mapping = {}
    
    # Risk-On: Highest average return + low USDTRY volatility
    candidate_risk_on = regime_means.sort_values(
        by=["bist_return", "usdtry_volatility"],
        ascending=[False, True]
    ).index[0]
    
    # Carry Unwind: Lowest average return + high USDTRY volatility
    candidate_carry_unwind = regime_means.sort_values(
        by=["bist_return", "usdtry_volatility"],
        ascending=[True, False]
    ).index[0]
    
    # Stagflation Sideways: Remaining cluster
    candidate_stagflation = [c for c in range(n_clusters) 
                          if c not in [candidate_risk_on, candidate_carry_unwind]][0]
    
    regime_mapping = {
        candidate_risk_on: "Risk-On",
        candidate_carry_unwind: "Carry Unwind",
        candidate_stagflation: "Stagflation Sideways"
    }
    
    regime_labels = regime_labels.map(regime_mapping)
    
    print("KMeans regime distribution:")
    print(regime_labels.value_counts(normalize=True))
    
    return kmeans, scaler, features_list, regime_labels

def train_hmm(
    features: pd.DataFrame,
    features_list: List[str],
    scaler: StandardScaler,
    n_components: int = 3,
    random_state: int = 42
) -> Tuple[GaussianHMM, pd.Series]:
    """
    Trains Gaussian HMM model for regime detection.
    
    Args:
        features: Features DataFrame
        features_list: List of features to use
        scaler: Fitted scaler
        n_components: Number of HMM components
        random_state: Random state
    
    Returns:
        Trained HMM model, regime labels
    """
    print("Training Gaussian HMM model...")
    
    scaled_features = scaler.transform(features[features_list])
    
    # Train HMM
    hmm = GaussianHMM(
        n_components=n_components,
        covariance_type='full',
        n_iter=1000,
        random_state=random_state
    )
    hmm.fit(scaled_features)
    
    # Predict states
    states = hmm.predict(scaled_features)
    regime_labels = pd.Series(states, index=features.index, name="hmm_regime")
    
    print("HMM transition matrix:")
    print(hmm.transmat_)
    
    print("\nHMM state distribution:")
    print(regime_labels.value_counts(normalize=True))
    
    return hmm, regime_labels

def map_hmm_states_to_regimes(
    hmm_states: pd.Series,
    kmeans_regimes: pd.Series,
    features: pd.DataFrame,
    features_list: List[str]
) -> pd.Series:
    """
    Maps HMM state indices to regime labels using Euclidean distance.
    
    Args:
        hmm_states: HMM state predictions
        kmeans_regimes: KMeans regime labels
        features: Features DataFrame
        features_list: List of features used
    
    Returns:
        HMM states mapped to regime labels
    """
    print("Mapping HMM states to regime labels...")
    
    state_to_regime = {}
    
    for state in sorted(hmm_states.unique()):
        state_mask = hmm_states == state
        state_features = features[features_list][state_mask]
        
        regime_dists = {}
        for regime in REGIME_LABELS.values():
            regime_mask = kmeans_regimes == regime
            regime_features = features[features_list][regime_mask]
            
            dist = np.linalg.norm(
                state_features.mean() - regime_features.mean()
            )
            regime_dists[regime] = dist
        
        # Find closest regime
        state_to_regime[state] = min(regime_dists, key=regime_dists.get)
        print(f"State {state} → {state_to_regime[state]} (distance: {regime_dists[state_to_regime[state]]:.3f})")
    
    return hmm_states.map(state_to_regime)

def analyze_policy_impact(
    features: pd.DataFrame,
    regimes: pd.Series,
    policy_decisions: List[Dict] = None
) -> pd.DataFrame:
    """
    Analyzes the impact of TCMB policy decisions on regime transitions.
    
    Args:
        features: Features DataFrame
        regimes: Regime labels
        policy_decisions: List of TCMB policy decisions
    
    Returns:
        Analysis results DataFrame
    """
    if policy_decisions is None:
        policy_decisions = TCMB_POLICY_DECISIONS
    
    print("Analyzing TCMB policy impact...")
    
    results = []
    
    for decision in policy_decisions:
        date = pd.to_datetime(decision["date"])
        
        # Check if date is within our data range
        if date < features.index[0] or date > features.index[-1]:
            continue
            
        # Find previous and next days with data
        prev_5d = date - pd.Timedelta(days=5)
        next_5d = date + pd.Timedelta(days=5)
        
        mask_before = (features.index >= prev_5d) & (features.index < date)
        mask_after = (features.index > date) & (features.index <= next_5d)
        
        if mask_before.sum() < 3 or mask_after.sum() < 3:
            continue
        
        regimes_before = regimes[mask_before]
        regimes_after = regimes[mask_after]
        
        # Calculate regime distribution
        before_dist = regimes_before.value_counts(normalize=True).reindex(REGIME_LABELS.values())
        after_dist = regimes_after.value_counts(normalize=True).reindex(REGIME_LABELS.values())
        
        # Most common regime before and after
        most_common_before = regimes_before.mode().iloc[0]
        most_common_after = regimes_after.mode().iloc[0]
        
        # Transition
        transition = f"{most_common_before} → {most_common_after}"
        
        results.append({
            "date": date,
            "policy_rate": decision["policy_rate"],
            "change_bps": decision["change_bps"],
            "change_type": "Increase" if decision["change_bps"] > 0 else "Decrease" if decision["change_bps"] < 0 else "Hold",
            "prev_regime": most_common_before,
            "next_regime": most_common_after,
            "transition": transition,
            **{f"before_{regime}": before_dist.get(regime, 0) for regime in REGIME_LABELS.values()},
            **{f"after_{regime}": after_dist.get(regime, 0) for regime in REGIME_LABELS.values()}
        })
    
    return pd.DataFrame(results)

def create_main_regime_plot(
    features: pd.DataFrame,
    regimes: pd.Series,
    policy_decisions: List[Dict] = None
) -> go.Figure:
    """
    Creates interactive Plotly chart with price and regime visualization.
    
    Args:
        features: Features DataFrame
        regimes: Regime labels
        policy_decisions: List of TCMB policy decisions
    
    Returns:
        Plotly figure
    """
    if policy_decisions is None:
        policy_decisions = TCMB_POLICY_DECISIONS
    
    print("Creating main regime plot...")
    
    fig = go.Figure()
    
    # Price line
    fig.add_trace(go.Scatter(
        x=features.index,
        y=features["bist_close"],
        mode='lines',
        name='BIST100',
        line=dict(width=2, color="#1f2937")
    ))
    
    # Regime background
    for regime in REGIME_LABELS.values():
        regime_mask = regimes == regime
        regime_data = features[regime_mask]
        
        if len(regime_data) > 0:
            fig.add_trace(go.Scatter(
                x=regime_data.index,
                y=[0, features["bist_close"].max()],
                mode='lines',
                name=regime,
                line=dict(width=0),
                fill='tozeroy',
                fillcolor=REGIME_COLORS[regime],
                opacity=0.2
            ))
    
    # Policy decision markers
    policy_dates = []
    policy_colors = []
    policy_texts = []
    
    for decision in policy_decisions:
        date = pd.to_datetime(decision["date"])
        if date >= features.index[0] and date <= features.index[-1]:
            policy_dates.append(date)
            policy_colors.append(
                "#ef4444" if decision["change_bps"] > 0 else
                "#10b981" if decision["change_bps"] < 0 else
                "#6b7280"
            )
            policy_texts.append(
                f"{decision['date']}: {decision['policy_rate']:.2f}% "
                f"({decision['change_bps']:+}bps)"
            )
    
    for date, color, text in zip(policy_dates, policy_colors, policy_texts):
        fig.add_vline(
            x=date,
            line=dict(width=2, color=color, dash='dot')
        )
        # Add annotation separately to avoid timestamp issues
        fig.add_annotation(
            x=date,
            y=features["bist_close"].max(),
            text=text,
            showarrow=True,
            font=dict(size=10),
            yanchor='bottom',
            arrowhead=2
        )
    
    fig.update_layout(
        title="BIST100 Rejim Tespiti",
        yaxis_title="Fiyat (TL)",
        legend_title="Rejimler",
        hovermode="x unified",
        template="plotly_white",
        height=700
    )
    
    fig.update_xaxes(title="Tarih")
    
    return fig

def create_regime_statistics_heatmap(
    features: pd.DataFrame,
    regimes: pd.Series,
    features_to_analyze: Optional[List[str]] = None
) -> go.Figure:
    """
    Creates regime statistics heatmap.
    
    Args:
        features: Features DataFrame
        regimes: Regime labels
        features_to_analyze: List of features to include
    
    Returns:
        Plotly figure
    """
    print("Creating regime statistics heatmap...")
    
    if features_to_analyze is None:
        features_to_analyze = [
            "bist_return", "bist_volatility", "usdtry_change", "rsi", "ma_ratio"
        ]
    
    regime_stats = features.groupby(regimes)[features_to_analyze].mean()
    
    # Convert to annualized returns for better interpretability
    if "bist_return" in regime_stats.columns:
        regime_stats["bist_return"] *= 252
    
    # Calculate additional statistics
    regime_stats["days_count"] = regimes.value_counts().reindex(regime_stats.index)
    regime_stats["days_pct"] = (regime_stats["days_count"] / len(features)) * 100
    
    # Calculate Sharpe ratio (rf=0)
    regime_sharpe = features.groupby(regimes)["bist_return"].mean() / features.groupby(regimes)["bist_return"].std()
    regime_stats["sharpe_ratio"] = regime_sharpe * np.sqrt(252)
    
    # Format for display
    regime_stats_formatted = regime_stats.round(3)
    
    # Create heatmap
    fig = px.imshow(
        regime_stats_formatted,
        labels=dict(color="Değer"),
        x=regime_stats_formatted.columns,
        y=regime_stats_formatted.index,
        color_continuous_scale="viridis"
    )
    
    fig.update_layout(
        title="Rejim Bazlı İstatistikler",
        height=600,
        template="plotly_white"
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_transition_matrix_heatmap(
    hmm_model: GaussianHMM,
    regime_map: Dict[int, str]
) -> go.Figure:
    """
    Creates HMM transition matrix heatmap.
    
    Args:
        hmm_model: Trained HMM model
        regime_map: Mapping from HMM state to regime label
    
    Returns:
        Plotly figure
    """
    print("Creating transition matrix heatmap...")
    
    # Create transition matrix with state indices first
    transition_df = pd.DataFrame(
        hmm_model.transmat_,
        index=[f"State {i}" for i in range(len(hmm_model.transmat_))],
        columns=[f"State {i}" for i in range(len(hmm_model.transmat_))]
    )
    
    # Add regime labels to state names
    for i in range(len(hmm_model.transmat_)):
        transition_df = transition_df.rename(
            index={f"State {i}": f"State {i} ({regime_map.get(i, 'Unknown')})"},
            columns={f"State {i}": f"State {i} ({regime_map.get(i, 'Unknown')})"}
        )
    
    fig = px.imshow(
        transition_df,
        labels=dict(color="Olasılık"),
        x=transition_df.columns,
        y=transition_df.index,
        color_continuous_scale="Blues",
        text_auto=".2%"
    )
    
    fig.update_layout(
        title="Rejim Geçiş Matrisi (HMM)",
        height=600,
        template="plotly_white"
    )
    
    fig.update_xaxes(tickangle=45)
    
    return fig

def create_sector_performance_plot(
    features: pd.DataFrame,
    regimes: pd.Series
) -> go.Figure:
    """
    Creates sector performance comparison chart.
    
    Args:
        features: Features DataFrame
        regimes: Regime labels
    
    Returns:
        Plotly figure
    """
    print("Creating sector performance plot...")
    
    # Calculate annualized returns for sectors
    sector_returns = {
        "BIST100": features.groupby(regimes)["bist_return"].mean() * 252,
        "BIST Banka": features.groupby(regimes)["banka_return"].mean() * 252,
        "BIST Sınai": features.groupby(regimes)["sinai_return"].mean() * 252
    }
    
    returns_df = pd.DataFrame(sector_returns)
    
    fig = go.Figure()
    
    for sector in returns_df.columns:
        fig.add_trace(go.Bar(
            x=returns_df.index,
            y=returns_df[sector],
            name=sector
        ))
    
    fig.update_layout(
        title="Sektörel Performans (Yıllık Ortalama)",
        yaxis_title="Yıllık Getiri (%)",
        barmode="group",
        height=600,
        template="plotly_white"
    )
    
    return fig

def get_current_regime(
    features: pd.DataFrame,
    scaler: StandardScaler,
    kmeans_model: KMeans,
    hmm_model: GaussianHMM,
    features_list: List[str],
    regime_map: Dict[int, str],
    policy_decisions: List[Dict] = None
) -> Dict:
    """
    Gets current regime prediction and transition probabilities.
    
    Args:
        features: Features DataFrame
        scaler: Fitted scaler
        kmeans_model: Trained KMeans model
        hmm_model: Trained HMM model
        features_list: List of features used
        regime_map: Mapping from HMM state to regime label
        policy_decisions: List of TCMB policy decisions
    
    Returns:
        Current regime information
    """
    if policy_decisions is None:
        policy_decisions = TCMB_POLICY_DECISIONS
    
    print("Getting current regime...")
    
    # Get last available data point
    last_point = features.iloc[-1:][features_list]
    last_date = features.index[-1]
    
    # KMeans prediction
    scaled_last = scaler.transform(last_point)
    kmeans_pred = kmeans_model.predict(scaled_last)[0]
    
    # Map KMeans label to regime name
    temp_df = pd.DataFrame({"kmeans_label": [kmeans_pred]})
    # Need to reverse the regime mapping from KMeans training
    # For now, use HMM which should have direct mapping
    
    # HMM prediction
    full_scaled = scaler.transform(features[features_list])
    current_state = hmm_model.predict(full_scaled)[-1]
    current_regime = regime_map[current_state]
    
    # Transition probability from current state
    transition_probs = hmm_model.transmat_[current_state]
    transition_df = pd.DataFrame({
        "regime": [regime_map[i] for i in range(len(transition_probs))],
        "probability": transition_probs
    }).set_index("regime")
    
    # Time spent in current regime
    regime_series = pd.Series([regime_map[s] for s in hmm_model.predict(full_scaled)], index=features.index)
    current_regime_mask = (regime_series == current_regime)
    
    # Find current regime duration
    duration = 0
    for date in reversed(features.index):
        if current_regime_mask[date]:
            duration += 1
        else:
            break
    
    # Last policy decision
    policy_df = pd.DataFrame(policy_decisions)
    policy_df["date"] = pd.to_datetime(policy_df["date"])
    policy_df = policy_df[policy_df["date"] <= last_date]
    
    if not policy_df.empty:
        last_policy = policy_df.sort_values("date").iloc[-1]
    else:
        last_policy = None
    
    return {
        "date": last_date.strftime("%Y-%m-%d"),
        "regime": current_regime,
        "duration_days": duration,
        "transition_probabilities": transition_df.to_dict()["probability"],
        "last_policy": last_policy
    }

def run_analysis(
    tickers: Optional[List[str]] = None,
    period: str = "5y"
) -> Dict:
    """
    Runs complete analysis pipeline.
    
    Args:
        tickers: List of tickers to analyze (defaults to BIST100, Banka, Sınai)
        period: Data period
    
    Returns:
        Dictionary containing all results
    """
    print("=== BIST100 Rejim Tespiti ===\n")
    
    # Validate inputs
    print("=== Giriş Doğrulama ===")
    
    # Validate period format
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
    if period not in valid_periods and not (period.endswith("d") and period[:-1].isdigit() and int(period[:-1]) > 0):
        raise ValueError(f"Geçersiz dönem formatı: '{period}'. Geçerli formatlar: {', '.join(valid_periods)} veya sayı+d (örn: 180d)")
    
    # Check if period is too short for feature engineering (minimum 200 days needed for reliable results)
    if period.endswith("d"):
        days = int(period[:-1])
        if days < 200:
            print(f"⚠️ Uyarı: {days} günlük dönem özellik mühendisliği için yeterli değil. Minimum 200 gün önerilir.")
    elif period in ["1d", "5d", "1mo", "3mo", "6mo"]:
        print("⚠️ Uyarı: Kısa dönemler (≤ 6 ay) özellik mühendisliği için yeterli değil. Minimum 2 yıllık veri önerilir.")
    
    # Validate tickers
    if tickers is None:
        tickers = [
            "XU100.IS", "XBANK.IS", "XUSIN.IS",
            "USDTRY=X", "GOLDS.IS", "EEM"
        ]
    elif len(tickers) == 0:
        raise ValueError("En az bir hisse senedi sembolü girilmelidir.")
    elif not all(isinstance(ticker, str) and len(ticker.strip()) > 0 for ticker in tickers):
        raise ValueError("Tüm hisse senedi sembolleri geçerli stringler olmalıdır.")
    
    print(f"✅ Giriş doğrulama başarılı")
    print(f"📅 Analiz dönemi: {period}")
    print(f"📈 Hisse sembolleri: {', '.join(tickers)}")
    
    # Step 1: Fetch data
    print("\n=== Veri Toplama ===")
    price_data = fetch_yfinance_data(tickers, period=period)
    policy_data = fetch_evds_data(EVDS_KEY)
    
    # Step 2: Create features
    print("\n=== Özellik Mühendisliği ===")
    features = create_features(price_data, policy_data)
    
    # Step 3: Train KMeans
    print("\n=== KMeans Modeli ===")
    kmeans, scaler, features_list, kmeans_regimes = train_kmeans(features)
    
    # Step 4: Train HMM
    print("\n=== Gaussian HMM Modeli ===")
    hmm, hmm_states = train_hmm(features, features_list, scaler)
    
    # Step 5: Map HMM states to regimes
    print("\n=== HMM Rejim Eşleştirme ===")
    hmm_regimes = map_hmm_states_to_regimes(
        hmm_states, kmeans_regimes, features, features_list
    )
    
    # Step 6: Analyze policy impact
    print("\n=== TCMB Politika Etkileri ===")
    policy_analysis = analyze_policy_impact(features, hmm_regimes)
    
    # Step 7: Calculate agreement metrics
    print("\n=== Model Uyumluluğu ===")
    print(f"Cohen's Kappa: {cohen_kappa_score(kmeans_regimes, hmm_regimes):.3f}")
    
    confusion = confusion_matrix(kmeans_regimes, hmm_regimes)
    confusion_df = pd.DataFrame(
        confusion,
        index=REGIME_LABELS.values(),
        columns=REGIME_LABELS.values()
    )
    print("\nConfusion Matrix:")
    print(confusion_df)
    
    # Step 8: Current regime analysis
    print("\n=== Güncel Rejim Analizi ===")
    # Create correct regime mapping from HMM state to label
    # First, get all unique HMM states and their corresponding regime labels
    state_regime_map = {}
    for state in sorted(hmm_states.unique()):
        mask = hmm_states == state
        most_common_regime = hmm_regimes[mask].mode().iloc[0] if mask.sum() > 0 else "Unknown"
        state_regime_map[state] = most_common_regime
    
    current_info = get_current_regime(
        features, scaler, kmeans, hmm, features_list,
        state_regime_map,
        TCMB_POLICY_DECISIONS
    )
    
    print_current_regime_info(current_info)
    
    # Step 9: Create visualizations
    print("\n=== Görselleştirme ===")
    fig_main = create_main_regime_plot(features, hmm_regimes)
    fig_stats = create_regime_statistics_heatmap(features, hmm_regimes)
    # Use the same state-to-regime map created earlier
    fig_transition = create_transition_matrix_heatmap(
        hmm,
        state_regime_map
    )
    fig_sector = create_sector_performance_plot(features, hmm_regimes)
    
    return {
        "features": features,
        "kmeans": {"model": kmeans, "regimes": kmeans_regimes},
        "hmm": {"model": hmm, "regimes": hmm_regimes},
        "policy_analysis": policy_analysis,
        "current_regime": current_info,
        "visualizations": {
            "main_plot": fig_main,
            "stats_heatmap": fig_stats,
            "transition_matrix": fig_transition,
            "sector_performance": fig_sector
        }
    }

def print_current_regime_info(current_info: Dict):
    """
    Prints current regime information in a readable format.
    
    Args:
        current_info: Current regime information dictionary
    """
    print(f"📅 Tarih: {current_info['date']}")
    print(f"🎯 Güncel Rejim: {current_info['regime']}")
    print(f"⏱️ Rejim Süresi: {current_info['duration_days']} gün")
    
    print("\n🔄 Geçiş Olasılıkları:")
    for regime, prob in current_info['transition_probabilities'].items():
        if regime != current_info['regime']:
            print(f"  → {regime}: {prob:.1%}")
    
    if current_info['last_policy'] is not None:
        change_text = f"{current_info['last_policy']['change_bps']:+} bps"
        print(f"\n💵 Son TCMB Faiz Kararı: {current_info['last_policy']['policy_rate']:.2f}% "
              f"({change_text}) on {pd.to_datetime(current_info['last_policy']['date']).strftime('%Y-%m-%d')}")
    else:
        print("\n💵 Son TCMB Faiz Kararı: Veri bulunamadı")

def save_figures(
    visualizations: Dict[str, go.Figure],
    output_dir: str = "visualizations"
):
    """
    Saves all Plotly figures to HTML files.
    
    Args:
        visualizations: Dictionary of Plotly figures
        output_dir: Output directory
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for name, fig in visualizations.items():
        filename = f"{name}.html"
        filepath = os.path.join(output_dir, filename)
        fig.write_html(filepath)
        print(f"Kaydedildi: {filepath}")

if __name__ == "__main__":
    print("BIST100 Rejim Tespiti Uygulaması")
    print("=" * 50)
    
    try:
        # Run complete analysis
        results = run_analysis()
        
        # Save visualizations
        save_figures(results["visualizations"])
        
        print("\n✅ Analiz tamamlandı!")
        print(f"📊 Görselleştirmeler: {os.path.abspath('visualizations')}")
        
        # Display current regime in bold
        print("\n" + "=" * 50)
        print("🎯 GÜNCEL REJIM BİLGİSİ")
        print("=" * 50)
        print_current_regime_info(results["current_regime"])
    
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        import traceback
        print(f"\nDetaylı Hata İzleri:\n{traceback.format_exc()}")
