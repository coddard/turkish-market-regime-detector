"""
Comprehensive test suite for Turkish Market Regime Detector
Tests all modular components
"""

import unittest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestConfigModule(unittest.TestCase):
    """Test configuration module"""
    
    def test_regime_labels(self):
        """Test regime labels are defined"""
        from src.config.constants import REGIME_LABELS
        self.assertEqual(len(REGIME_LABELS), 3)
        self.assertIn(0, REGIME_LABELS)
        self.assertIn(1, REGIME_LABELS)
        self.assertIn(2, REGIME_LABELS)
    
    def test_regime_colors(self):
        """Test regime colors are defined"""
        from src.config.constants import REGIME_COLORS
        self.assertEqual(len(REGIME_COLORS), 3)
        for color in REGIME_COLORS.values():
            self.assertIsInstance(color, str)
    
    def test_default_tickers(self):
        """Test default tickers are defined"""
        from src.config.constants import DEFAULT_TICKERS
        self.assertIsInstance(DEFAULT_TICKERS, list)
        self.assertGreater(len(DEFAULT_TICKERS), 0)
        self.assertTrue(all('.IS' in t for t in DEFAULT_TICKERS))
    
    def test_tcmb_policy_decisions(self):
        """Test TCMB policy decisions are defined"""
        from src.config.constants import TCMB_POLICY_DECISIONS
        self.assertIsInstance(TCMB_POLICY_DECISIONS, list)
        self.assertGreater(len(TCMB_POLICY_DECISIONS), 0)
    
    def test_settings_default(self):
        """Test Settings default values"""
        from src.config.settings import Settings
        settings = Settings()
        self.assertEqual(settings.project_name, "Turkish Market Regime Detector")
        self.assertEqual(settings.version, "2.0.0")
        self.assertIn("yfinance_period", settings.data.__dict__)
    
    def test_settings_custom(self):
        """Test Settings custom values"""
        from src.config.settings import Settings, DataSourceConfig
        
        # Create custom settings
        data_config = DataSourceConfig(yfinance_period="1y")
        settings = Settings(
            project_name="Test Project",
            data=data_config
        )
        self.assertEqual(settings.project_name, "Test Project")
        self.assertEqual(settings.data.yfinance_period, "1y")


class TestDataProcessor(unittest.TestCase):
    """Test data processing module"""
    
    def setUp(self):
        """Set up test data"""
        from src.data.processor import DataProcessor
        self.processor = DataProcessor()
        
        # Create sample price data
        np.random.seed(42)
        dates = pd.date_range('2022-01-01', periods=100, freq='D')
        self.prices = pd.DataFrame({
            'THYAO.IS': 100 + np.cumsum(np.random.randn(100) * 2),
            'GARAN.IS': 50 + np.cumsum(np.random.randn(100) * 1),
            'AKBNK.IS': 20 + np.cumsum(np.random.randn(100) * 0.5)
        }, index=dates)
    
    def test_calculate_returns(self):
        """Test return calculation"""
        returns = self.processor.calculate_returns(self.prices)
        self.assertEqual(len(returns), len(self.prices) - 1)
        self.assertTrue(np.all(np.isfinite(returns.values)))
    
    def test_calculate_rsi(self):
        """Test RSI calculation"""
        rsi = self.processor.calculate_rsi(self.prices['THYAO.IS'])
        self.assertEqual(len(rsi), len(self.prices))
        # RSI should be between 0 and 100
        valid_rsi = rsi.dropna()
        self.assertTrue(np.all((valid_rsi >= 0) & (valid_rsi <= 100)))
    
    def test_calculate_volatility(self):
        """Test volatility calculation"""
        returns = self.processor.calculate_returns(self.prices)
        volatility = self.processor.calculate_volatility(returns['THYAO.IS'])
        self.assertEqual(len(volatility), len(returns))
        # Volatility should be non-negative
        self.assertTrue(np.all(volatility.dropna() >= 0))
    
    def test_calculate_momentum(self):
        """Test momentum calculation"""
        momentum = self.processor.calculate_momentum(self.prices['THYAO.IS'])
        self.assertEqual(len(momentum), len(self.prices))
    
    def test_calculate_moving_average(self):
        """Test moving average calculation"""
        ma = self.processor.calculate_moving_average(self.prices['THYAO.IS'], period=20)
        self.assertEqual(len(ma), len(self.prices))
    
    def test_create_features(self):
        """Test feature creation"""
        features = self.processor.create_features(self.prices)
        self.assertIsInstance(features, pd.DataFrame)
        self.assertGreater(len(features.columns), 0)
        self.assertGreater(len(features), 0)
    
    def test_normalize_features_zscore(self):
        """Test z-score normalization"""
        features = self.processor.create_features(self.prices)
        normalized = self.processor.normalize_features(features, method="zscore")
        # Mean should be ~0, std should be ~1
        self.assertTrue(np.allclose(normalized.mean(), 0, atol=0.1))
    
    def test_normalize_features_minmax(self):
        """Test min-max normalization"""
        features = self.processor.create_features(self.prices)
        normalized = self.processor.normalize_features(features, method="minmax")
        # Should be between 0 and 1
        self.assertTrue(np.all((normalized >= 0) & (normalized <= 1)))
    
    def test_handle_missing_data_forward_fill(self):
        """Test forward fill missing data handling"""
        test_df = pd.DataFrame({'A': [1, np.nan, 3], 'B': [4, 5, np.nan]})
        filled = self.processor.handle_missing_data(test_df, method="forward_fill")
        self.assertFalse(filled.isnull().any().any())
    
    def test_handle_missing_data_drop(self):
        """Test drop missing data handling"""
        test_df = pd.DataFrame({'A': [1, np.nan, 3], 'B': [4, 5, np.nan]})
        filled = self.processor.handle_missing_data(test_df, method="drop")
        self.assertFalse(filled.isnull().any().any())


class TestKMeansModel(unittest.TestCase):
    """Test K-Means regime model"""
    
    def setUp(self):
        """Set up test data"""
        from src.models.kmeans_model import KMeansRegimeModel
        self.model = KMeansRegimeModel(n_regimes=3, random_state=42)
        
        # Create sample feature data
        np.random.seed(42)
        n_samples = 100
        n_features = 5
        X = np.random.randn(n_samples, n_features)
        X[:33, :] += 2  # Cluster 1
        X[33:66, :] -= 1  # Cluster 2
        # Cluster 3 is around origin
        
        self.X = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(n_features)])
    
    def test_fit(self):
        """Test model fitting"""
        self.model.fit(self.X)
        self.assertTrue(self.model.is_fitted)
        self.assertIsNotNone(self.model.cluster_centers_)
    
    def test_predict(self):
        """Test prediction"""
        self.model.fit(self.X)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.X))
        self.assertTrue(np.all(np.isin(predictions, [0, 1, 2])))
    
    def test_predict_proba(self):
        """Test probability prediction"""
        self.model.fit(self.X)
        probs = self.model.predict_proba(self.X)
        self.assertEqual(probs.shape, (len(self.X), 3))
        # Probabilities should sum to 1
        self.assertTrue(np.allclose(probs.sum(axis=1), 1))
    
    def test_get_cluster_centers(self):
        """Test getting cluster centers"""
        self.model.fit(self.X)
        centers = self.model.get_cluster_centers()
        self.assertEqual(centers.shape, (3, 5))
    
    def test_get_inertia(self):
        """Test getting inertia"""
        self.model.fit(self.X)
        inertia = self.model.get_inertia()
        self.assertIsInstance(inertia, float)
        self.assertGreater(inertia, 0)
    
    def test_relabel_regimes(self):
        """Test regime relabeling"""
        self.model.fit(self.X)
        predictions = self.model.predict(self.X)
        relabeled = self.model.relabel_regimes(self.X, method="auto")
        self.assertEqual(len(relabeled), len(predictions))
    
    def test_validate_input_empty(self):
        """Test validation with empty input"""
        empty_df = pd.DataFrame()
        self.assertFalse(self.model.validate_input(empty_df))
    
    def test_validate_input_valid(self):
        """Test validation with valid input"""
        self.assertTrue(self.model.validate_input(self.X))


class TestHMMModel(unittest.TestCase):
    """Test HMM regime model"""
    
    def setUp(self):
        """Set up test data"""
        # Check if hmmlearn is available
        try:
            import hmmlearn
        except ImportError:
            self.skipTest("hmmlearn not installed")
            
        from src.models.hmm_model import HMMRegimeModel
        self.model = HMMRegimeModel(n_regimes=3, random_state=42, n_iter=50)
        
        # Create sample time series data
        np.random.seed(42)
        n_samples = 100
        n_features = 3
        
        # Create data with regime-like patterns
        data = []
        for i in range(n_samples):
            if i < 33:
                data.append([2 + np.random.randn() * 0.5, 
                            1 + np.random.randn() * 0.3,
                            0 + np.random.randn() * 0.2])
            elif i < 66:
                data.append([-1 + np.random.randn() * 0.3,
                            0 + np.random.randn() * 0.2,
                            1 + np.random.randn() * 0.1])
            else:
                data.append([0 + np.random.randn() * 0.4,
                            -1 + np.random.randn() * 0.3,
                            0 + np.random.randn() * 0.2])
        
        self.X = pd.DataFrame(data, columns=[f'feature_{i}' for i in range(n_features)])
    
    def test_fit(self):
        """Test model fitting"""
        self.model.fit(self.X)
        self.assertTrue(self.model.is_fitted)
        self.assertIsNotNone(self.model.startprob_)
    
    def test_predict(self):
        """Test prediction"""
        self.model.fit(self.X)
        predictions = self.model.predict(self.X)
        self.assertEqual(len(predictions), len(self.X))
        self.assertTrue(np.all(np.isin(predictions, [0, 1, 2])))
    
    def test_predict_proba(self):
        """Test probability prediction"""
        self.model.fit(self.X)
        probs = self.model.predict_proba(self.X)
        self.assertEqual(probs.shape, (len(self.X), 3))
        # Probabilities should sum to 1
        self.assertTrue(np.allclose(probs.sum(axis=1), 1, atol=0.01))
    
    def test_get_transition_matrix(self):
        """Test getting transition matrix"""
        self.model.fit(self.X)
        tm = self.model.get_transition_matrix()
        self.assertEqual(tm.shape, (3, 3))
        # Rows should sum to 1
        self.assertTrue(np.allclose(tm.sum(axis=1), 1))
    
    def test_get_stationary_distribution(self):
        """Test stationary distribution calculation"""
        self.model.fit(self.X)
        stationary = self.model.get_stationary_distribution()
        self.assertEqual(len(stationary), 3)
        # Should sum to 1
        self.assertTrue(np.isclose(stationary.sum(), 1))
    
    def test_score(self):
        """Test model score"""
        self.model.fit(self.X)
        score = self.model.score(self.X)
        self.assertIsInstance(score, float)


class TestYFinanceFetcher(unittest.TestCase):
    """Test Yahoo Finance data fetcher"""
    
    def setUp(self):
        """Set up test"""
        from src.data.yfinance_fetcher import YFinanceFetcher
        self.fetcher = YFinanceFetcher(period="1y", interval="1d")
    
    def test_init(self):
        """Test initialization"""
        self.assertEqual(self.fetcher.period, "1y")
        self.assertEqual(self.fetcher.interval, "1d")
    
    @patch('src.data.yfinance_fetcher.YFinanceFetcher._import_yfinance')
    def test_default_tickers(self, mock_import):
        """Test default tickers"""
        mock_yf = Mock()
        mock_yf.Ticker.return_value.history.return_value = pd.DataFrame()
        mock_import.return_value = mock_yf
        
        from src.data.yfinance_fetcher import YFinanceFetcher
        fetcher = YFinanceFetcher()
        self.assertIsInstance(fetcher.DEFAULT_TICKERS, list)
        self.assertGreater(len(fetcher.DEFAULT_TICKERS), 0)
    
    def test_proxy_tickers(self):
        """Test proxy tickers"""
        self.assertIn("USDTRY", self.fetcher.PROXY_TICKERS)
        self.assertIn("BIST100", self.fetcher.PROXY_TICKERS)


class TestEVDSFetcher(unittest.TestCase):
    """Test EVDS data fetcher"""
    
    def setUp(self):
        """Set up test"""
        from src.data.evds_fetcher import EVDSFetcher
        self.fetcher = EVDSFetcher()
    
    def test_init(self):
        """Test initialization"""
        self.assertIsNone(self.fetcher.api_key)
    
    def test_series_codes(self):
        """Test series codes are defined"""
        self.assertIn("overnight_rate", self.fetcher.SERIES_CODES)
        self.assertIn("usd_try", self.fetcher.SERIES_CODES)
    
    def test_get_fallback_data(self):
        """Test fallback data"""
        fallback = self.fetcher._get_fallback_data("test_endpoint")
        self.assertEqual(fallback["status"], "fallback")
    
    def test_create_sample_data(self):
        """Test sample data creation"""
        df = self.fetcher._create_sample_data("TP.DK.USD.A", "01-01-2022", "31-12-2022")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)


class TestVisualization(unittest.TestCase):
    """Test visualization module"""
    
    def test_regime_plotter_init(self):
        """Test RegimePlotter initialization"""
        from src.visualization.plots import RegimePlotter
        try:
            plotter = RegimePlotter()
            self.assertEqual(plotter.template, "plotly_dark")
            self.assertEqual(plotter.height, 600)
        except ImportError:
            self.skipTest("Plotly not available")
    
    def test_regime_colors(self):
        """Test regime colors are defined"""
        from src.visualization.plots import RegimePlotter
        plotter = RegimePlotter()
        self.assertIn(0, plotter.REGIME_COLORS)
        self.assertIn(1, plotter.REGIME_COLORS)
        self.assertIn(2, plotter.REGIME_COLORS)
    
    def test_regime_labels(self):
        """Test regime labels are defined"""
        from src.visualization.plots import RegimePlotter
        plotter = RegimePlotter()
        self.assertIn(0, plotter.REGIME_LABELS)
        self.assertIn(1, plotter.REGIME_LABELS)
        self.assertIn(2, plotter.REGIME_LABELS)


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with old API"""
    
    def test_run_analysis_import(self):
        """Test run_analysis can be imported"""
        try:
            from src import run_analysis
            self.assertTrue(callable(run_analysis))
        except ImportError:
            self.fail("run_analysis not importable")
    
    def test_default_tickers_import(self):
        """Test DEFAULT_TICKERS can be imported"""
        try:
            from src import DEFAULT_TICKERS
            self.assertIsInstance(DEFAULT_TICKERS, list)
        except ImportError:
            self.fail("DEFAULT_TICKERS not importable")
    
    def test_regime_labels_import(self):
        """Test REGIME_LABELS can be imported"""
        try:
            from src import REGIME_LABELS
            self.assertIsInstance(REGIME_LABELS, dict)
        except ImportError:
            self.fail("REGIME_LABELS not importable")


if __name__ == '__main__':
    # Run tests with verbosity
    unittest.main(verbosity=2)