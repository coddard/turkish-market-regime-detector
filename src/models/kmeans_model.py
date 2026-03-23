"""
K-Means model for regime detection
Uses clustering to identify market regimes
"""

import pandas as pd
import numpy as np
from typing import Optional
import logging

from .base import RegimeModelBase

logger = logging.getLogger(__name__)


class KMeansRegimeModel(RegimeModelBase):
    """
    K-Means clustering based regime detection model.
    Identifies market regimes by clustering feature vectors.
    """
    
    def __init__(
        self,
        n_regimes: int = 3,
        random_state: int = 42,
        max_iter: int = 300,
        n_init: int = 10,
        init: str = "k-means++"
    ):
        """
        Initialize K-Means regime model.
        
        Args:
            n_regimes: Number of regimes to detect
            random_state: Random seed
            max_iter: Maximum iterations
            n_init: Number of initializations
            init: Initialization method
        """
        super().__init__(n_regimes=n_regimes, random_state=random_state)
        
        self.max_iter = max_iter
        self.n_init = n_init
        self.init = init
        self.model = None
        self.cluster_centers_ = None
        
    def _import_sklearn(self):
        """Import sklearn with proper error handling"""
        try:
            from sklearn.cluster import KMeans
            return KMeans
        except ImportError:
            logger.error("scikit-learn not installed")
            raise ImportError("scikit-learn is required. Install with: pip install scikit-learn")
    
    def fit(self, X: pd.DataFrame) -> "KMeansRegimeModel":
        """
        Fit K-Means model to data.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            self
        """
        if not self.validate_input(X):
            raise ValueError("Invalid input data")
        
        KMeans = self._import_sklearn()
        
        self.model = KMeans(
            n_clusters=self.n_regimes,
            random_state=self.random_state,
            max_iter=self.max_iter,
            n_init=self.n_init,
            init=self.init
        )
        
        self.model.fit(X.values)
        self.cluster_centers_ = self.model.cluster_centers_
        self.feature_names = X.columns.tolist()
        self.is_fitted = True
        
        logger.info(f"K-Means fitted with {self.n_regimes} clusters")
        
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict regime labels.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of regime labels
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
            
        if not self.validate_input(X):
            raise ValueError("Invalid input data")
            
        predictions = self.model.predict(X.values)
        
        return predictions
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict regime probabilities (based on distance to cluster centers).
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of regime probabilities
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        # Calculate distances to each cluster center
        distances = self._calculate_distances(X)
        
        # Convert distances to probabilities using softmax-like transformation
        # Closer clusters have higher probability
        inv_distances = 1 / (distances + 1e-10)
        probs = inv_distances / inv_distances.sum(axis=1, keepdims=True)
        
        return probs
    
    def _calculate_distances(self, X: pd.DataFrame) -> np.ndarray:
        """
        Calculate distance from each sample to each cluster center.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Distance matrix
        """
        X_values = X.values
        
        distances = np.zeros((len(X_values), self.n_regimes))
        
        for i, center in enumerate(self.cluster_centers_):
            distances[:, i] = np.sqrt(np.sum((X_values - center) ** 2, axis=1))
        
        return distances
    
    def get_cluster_centers(self) -> pd.DataFrame:
        """
        Get cluster centers as DataFrame.
        
        Returns:
            DataFrame with cluster centers
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted")
            
        return pd.DataFrame(
            self.cluster_centers_,
            columns=self.feature_names
        )
    
    def get_inertia(self) -> float:
        """
        Get within-cluster sum of squares.
        
        Returns:
            Inertia value
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted")
            
        return self.model.inertia_
    
    def get_regime_characteristics(
        self,
        X: pd.DataFrame,
        regime_labels: Optional[np.ndarray] = None
    ) -> dict:
        """
        Get characteristics of each regime.
        
        Args:
            X: Feature DataFrame
            regime_labels: Optional pre-computed labels
            
        Returns:
            Dictionary with regime characteristics
        """
        if regime_labels is None:
            regime_labels = self.predict(X)
        
        characteristics = {}
        
        for regime_id in range(self.n_regimes):
            mask = regime_labels == regime_id
            regime_data = X[mask]
            
            if len(regime_data) == 0:
                continue
                
            # Calculate characteristics
            characteristics[regime_id] = {
                "n_samples": int(mask.sum()),
                "percentage": float(mask.sum() / len(regime_labels) * 100),
                "mean": regime_data.mean().to_dict(),
                "std": regime_data.std().to_dict(),
                "min": regime_data.min().to_dict(),
                "max": regime_data.max().to_dict()
            }
        
        return characteristics
    
    def relabel_regimes(
        self,
        X: pd.DataFrame,
        method: str = "auto"
    ) -> np.ndarray:
        """
        Relabel regimes based on characteristic (e.g., volatility).
        
        Args:
            X: Feature DataFrame
            method: Relabeling method
            
        Returns:
            Relabeled predictions
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted")
        
        predictions = self.predict(X)
        
        # Get regime characteristics
        characteristics = self.get_regime_characteristics(X, predictions)
        
        if method == "auto":
            # Order by average volatility (low to high)
            # Lower volatility = Risk-On, Higher = Stagflation
            volatility_order = {}
            
            for regime_id, chars in characteristics.items():
                # Use first available feature's std as proxy
                if "mean" in chars and chars["mean"]:
                    first_feature = list(chars["mean"].keys())[0]
                    volatility_order[regime_id] = chars["mean"][first_feature]
            
            # Sort by volatility
            sorted_regimes = sorted(volatility_order.items(), key=lambda x: x[1])
            
            # Create mapping
            relabel_map = {
                old_label: new_label 
                for new_label, (old_label, _) in enumerate(sorted_regimes)
            }
            
            return np.array([relabel_map[p] for p in predictions])
        
        return predictions
    
    def get_model_params(self) -> dict:
        """
        Get model parameters.
        
        Returns:
            Dictionary of parameters
        """
        params = super().get_model_params()
        params.update({
            "max_iter": self.max_iter,
            "n_init": self.n_init,
            "init": self.init
        })
        return params


def train_kmeans(
    X: pd.DataFrame,
    n_regimes: int = 3,
    random_state: int = 42,
    **kwargs
) -> KMeansRegimeModel:
    """
    Convenience function to train K-Means regime model.
    
    Args:
        X: Feature DataFrame
        n_regimes: Number of regimes
        random_state: Random seed
        **kwargs: Additional arguments
        
    Returns:
        Fitted KMeansRegimeModel
    """
    model = KMeansRegimeModel(
        n_regimes=n_regimes,
        random_state=random_state,
        **kwargs
    )
    return model.fit(X)