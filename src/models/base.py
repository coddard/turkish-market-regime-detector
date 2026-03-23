"""
Base model class for regime detection
Provides common interface for all regime detection models
"""

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict, Any
import logging

logger = logging.getLogger(__name__)


class RegimeModelBase(ABC):
    """
    Abstract base class for regime detection models.
    All models should inherit from this class.
    """
    
    def __init__(self, n_regimes: int = 3, random_state: int = 42):
        """
        Initialize base model.
        
        Args:
            n_regimes: Number of market regimes to detect
            random_state: Random seed for reproducibility
        """
        self.n_regimes = n_regimes
        self.random_state = random_state
        self.is_fitted = False
        self.feature_names = None
        
    @abstractmethod
    def fit(self, X: pd.DataFrame) -> "RegimeModelBase":
        """
        Fit the model to training data.
        
        Args:
            X: Feature DataFrame
            Returns:
                self
        """
        pass
    
    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict regime labels for data.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of regime labels
        """
        pass
    
    @abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict regime probabilities.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of regime probabilities
        """
        pass
    
    def fit_predict(
        self,
        X: pd.DataFrame
    ) -> Tuple["RegimeModelBase", np.ndarray]:
        """
        Fit model and return predictions.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Tuple of (fitted model, predictions)
        """
        self.fit(X)
        predictions = self.predict(X)
        return self, predictions
    
    def get_regime_summary(
        self,
        X: pd.DataFrame,
        predictions: np.ndarray
    ) -> Dict[str, Any]:
        """
        Get summary statistics for each regime.
        
        Args:
            X: Feature DataFrame
            predictions: Regime predictions
            
        Returns:
            Dictionary with regime statistics
        """
        summary = {}
        
        for regime in range(self.n_regimes):
            mask = predictions == regime
            regime_data = X[mask]
            
            if len(regime_data) > 0:
                summary[regime] = {
                    "count": int(mask.sum()),
                    "percentage": float(mask.sum() / len(predictions) * 100),
                    "mean_features": regime_data.mean().to_dict(),
                    "std_features": regime_data.std().to_dict()
                }
        
        return summary
    
    def get_transition_matrix(
        self,
        predictions: np.ndarray
    ) -> pd.DataFrame:
        """
        Calculate regime transition matrix.
        
        Args:
            predictions: Regime predictions
            
        Returns:
            DataFrame with transition probabilities
        """
        n = len(predictions)
        transitions = np.zeros((self.n_regimes, self.n_regimes))
        
        for i in range(n - 1):
            from_regime = predictions[i]
            to_regime = predictions[i + 1]
            transitions[from_regime, to_regime] += 1
        
        # Normalize by row
        row_sums = transitions.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums > 0, row_sums, 1)  # Avoid division by zero
        transition_probs = transitions / row_sums
        
        return pd.DataFrame(
            transition_probs,
            index=range(self.n_regimes),
            columns=range(self.n_regimes)
        )
    
    def validate_input(self, X: pd.DataFrame) -> bool:
        """
        Validate input data.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            True if valid, False otherwise
        """
        if X.empty:
            logger.error("Input DataFrame is empty")
            return False
            
        if X.isnull().all().all():
            logger.error("Input DataFrame contains only NaN values")
            return False
            
        # Check for infinite values
        if np.isinf(X.values).any():
            logger.error("Input DataFrame contains infinite values")
            return False
            
        return True
    
    def get_model_params(self) -> Dict[str, Any]:
        """
        Get model parameters.
        
        Returns:
            Dictionary of model parameters
        """
        return {
            "n_regimes": self.n_regimes,
            "random_state": self.random_state,
            "is_fitted": self.is_fitted
        }
    
    def set_params(self, **params) -> "RegimeModelBase":
        """
        Set model parameters.
        
        Args:
            **params: Model parameters
            
        Returns:
            self
        """
        for key, value in params.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                logger.warning(f"Unknown parameter: {key}")
                
        return self