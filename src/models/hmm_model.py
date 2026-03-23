"""
Hidden Markov Model for regime detection
Models market regimes as hidden states with observable features
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple
import logging

from .base import RegimeModelBase

logger = logging.getLogger(__name__)


class HMMRegimeModel(RegimeModelBase):
    """
    Gaussian Hidden Markov Model for regime detection.
    Models regime transitions as a Markov process.
    """
    
    def __init__(
        self,
        n_regimes: int = 3,
        random_state: int = 42,
        n_iter: int = 100,
        covariance_type: str = "full"
    ):
        """
        Initialize HMM regime model.
        
        Args:
            n_regimes: Number of hidden states (regimes)
            random_state: Random seed
            n_iter: Maximum iterations for training
            covariance_type: Covariance type ("full", "tied", "diag", "spherical")
        """
        super().__init__(n_regimes=n_regimes, random_state=random_state)
        
        self.n_iter = n_iter
        self.covariance_type = covariance_type
        self.model = None
        self.startprob_ = None
        self.transmat_ = None
        self.means_ = None
        self.covars_ = None
        
    def _import_hmmlearn(self):
        """Import hmmlearn with proper error handling"""
        try:
            from hmmlearn import hmm
            return hmm
        except ImportError:
            logger.error("hmmlearn not installed")
            raise ImportError("hmmlearn is required. Install with: pip install hmmlearn")
    
    def fit(self, X: pd.DataFrame) -> "HMMRegimeModel":
        """
        Fit HMM model to data.
        
        Args:
            X: Feature DataFrame (time series)
            
        Returns:
            self
        """
        if not self.validate_input(X):
            raise ValueError("Invalid input data")
        
        hmm = self._import_sklearn()
        
        # Handle covariance type
        if self.covariance_type == "tied":
            cov_type = "tied"
        elif self.covariance_type == "spherical":
            cov_type = "spherical"
        elif self.covariance_type == "diag":
            cov_type = "diag"
        else:
            cov_type = "full"
        
        self.model = hmm.GaussianHMM(
            n_components=self.n_regimes,
            covariance_type=cov_type,
            n_iter=self.n_iter,
            random_state=self.random_state
        )
        
        # Fit model
        X_values = X.values
        self.model.fit(X_values)
        
        # Store model parameters
        self.startprob_ = self.model.startprob_
        self.transmat_ = self.model.transmat_
        self.means_ = self.model.means_
        self.covars_ = self.model.covars_
        self.feature_names = X.columns.tolist()
        self.is_fitted = True
        
        logger.info(f"HMM fitted with {self.n_regimes} states")
        
        return self
    
    def _import_sklearn(self):
        """Import hmmlearn - different from sklearn"""
        hmm = self._import_hmmlearn()
        return hmm
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict most likely regime sequence (Viterbi decoding).
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of regime labels
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
            
        if not self.validate_input(X):
            raise ValueError("Invalid input data")
        
        # Use Viterbi decoding for most likely sequence
        predictions, _ = self.model.decode(X.values, algorithm="viterbi")
        
        return predictions
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict posterior probability of each regime.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Array of regime probabilities
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        # Get posterior probabilities
        return self.model.predict_proba(X.values)
    
    def predict_single(self, X: np.ndarray) -> Tuple[int, np.ndarray]:
        """
        Predict regime for a single observation.
        
        Args:
            X: Feature array (1D or 2D)
            
        Returns:
            Tuple of (predicted regime, probabilities)
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        # Ensure 2D
        if X.ndim == 1:
            X = X.reshape(1, -1)
        
        # Predict
        proba = self.model.predict_proba(X)
        predicted = proba.argmax(axis=1)
        
        return predicted[0], proba[0]
    
    def sample(
        self,
        n_samples: int,
        current_state: Optional[int] = None
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate samples from the model.
        
        Args:
            n_samples: Number of samples to generate
            current_state: Starting state (None for random)
            
        Returns:
            Tuple of (samples, states)
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        if current_state is None:
            # Start from random initial state
            current_state = np.random.choice(self.n_regimes)
        
        return self.model.sample(n_samples, current_state)
    
    def get_transition_matrix(self) -> pd.DataFrame:
        """
        Get regime transition probability matrix.
        
        Returns:
            DataFrame with transition probabilities
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        return pd.DataFrame(
            self.transmat_,
            index=range(self.n_regimes),
            columns=range(self.n_regimes)
        )
    
    def get_stationary_distribution(self) -> np.ndarray:
        """
        Calculate stationary distribution of regimes.
        
        Returns:
            Array with stationary probabilities
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        # Solve (P - I)v = 0
        transmat = self.transmat_
        
        # Add constraint that probabilities sum to 1
        A = transmat.T - np.eye(self.n_regimes)
        A[-1, :] = np.ones(self.n_regimes)
        b = np.zeros(self.n_regimes)
        b[-1] = 1
        
        stationary = np.linalg.solve(A, b)
        
        return stationary
    
    def get_regime_means(self) -> pd.DataFrame:
        """
        Get mean values for each regime.
        
        Returns:
            DataFrame with regime means
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        return pd.DataFrame(
            self.means_,
            index=range(self.n_regimes),
            columns=self.feature_names
        )
    
    def get_regime_covariances(self) -> dict:
        """
        Get covariance matrices for each regime.
        
        Returns:
            Dictionary of covariance matrices
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        covariances = {}
        
        for i in range(self.n_regimes):
            covariances[i] = self.covars_[i] if self.covariance_type == "full" else self.covars_
        
        return covariances
    
    def score(self, X: pd.DataFrame) -> float:
        """
        Compute model score (log-likelihood per sample).
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Log-likelihood score
        """
        if not self.is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")
        
        return self.model.score(X.values)
    
    def get_model_params(self) -> dict:
        """
        Get model parameters.
        
        Returns:
            Dictionary of parameters
        """
        params = super().get_model_params()
        params.update({
            "n_iter": self.n_iter,
            "covariance_type": self.covariance_type,
            "startprob": self.startprob_.tolist() if self.startprob_ is not None else None,
            "transmat": self.transmat_.tolist() if self.transmat_ is not None else None
        })
        return params


def train_hmm(
    X: pd.DataFrame,
    n_regimes: int = 3,
    random_state: int = 42,
    **kwargs
) -> HMMRegimeModel:
    """
    Convenience function to train HMM regime model.
    
    Args:
        X: Feature DataFrame (time series)
        n_regimes: Number of regimes
        random_state: Random seed
        **kwargs: Additional arguments
        
    Returns:
        Fitted HMMRegimeModel
    """
    model = HMMRegimeModel(
        n_regimes=n_regimes,
        random_state=random_state,
        **kwargs
    )
    return model.fit(X)