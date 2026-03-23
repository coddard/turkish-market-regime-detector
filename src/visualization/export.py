"""
Export utilities for saving plots and results
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def export_plot(fig, filename: str, output_dir: str = "./visualizations") -> str:
    """
    Export plot to HTML file.
    
    Args:
        fig: Plotly figure
        filename: Output filename
        output_dir: Output directory
        
    Returns:
        Path to saved file
    """
    try:
        import plotly
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Save figure
        filepath = os.path.join(output_dir, filename)
        fig.write_html(filepath)
        
        logger.info(f"Plot saved to: {filepath}")
        return filepath
        
    except ImportError:
        logger.warning("Plotly not available for export")
        return ""
    except Exception as e:
        logger.error(f"Error saving plot: {str(e)}")
        return ""


def save_all_plots(
    plotter,
    prices,
    features,
    regimes,
    transition_matrix=None,
    output_dir: str = "./visualizations"
) -> dict:
    """
    Save all plots to files.
    
    Args:
        plotter: RegimePlotter instance
        prices: Price DataFrame
        features: Feature DataFrame
        regimes: Regime labels
        transition_matrix: Optional transition matrix
        output_dir: Output directory
        
    Returns:
        Dictionary with saved file paths
    """
    saved_files = {}
    
    # Create main plot
    try:
        fig = plotter.plot_prices_with_regimes(prices, regimes)
        saved_files["main_plot"] = export_plot(fig, "main_plot.html", output_dir)
    except Exception as e:
        logger.error(f"Error creating main plot: {str(e)}")
    
    # Create timeline
    try:
        fig = plotter.plot_regime_timeline(regimes, prices.index)
        saved_files["timeline"] = export_plot(fig, "timeline.html", output_dir)
    except Exception as e:
        logger.error(f"Error creating timeline: {str(e)}")
    
    # Create transition matrix
    if transition_matrix is not None:
        try:
            fig = plotter.plot_transition_matrix(transition_matrix)
            saved_files["transition"] = export_plot(fig, "transition_matrix.html", output_dir)
        except Exception as e:
            logger.error(f"Error creating transition matrix: {str(e)}")
    
    # Create distribution
    try:
        fig = plotter.plot_regime_distribution(regimes)
        saved_files["distribution"] = export_plot(fig, "regime_distribution.html", output_dir)
    except Exception as e:
        logger.error(f"Error creating distribution: {str(e)}")
    
    # Create heatmap
    try:
        fig = plotter.plot_feature_heatmap(features, regimes)
        saved_files["heatmap"] = export_plot(fig, "stats_heatmap.html", output_dir)
    except Exception as e:
        logger.error(f"Error creating heatmap: {str(e)}")
    
    return saved_files


def export_results(
    results: dict,
    filename: str = "results.csv",
    output_dir: str = "./results"
) -> str:
    """
    Export results to CSV.
    
    Args:
        results: Results dictionary
        filename: Output filename
        output_dir: Output directory
        
    Returns:
        Path to saved file
    """
    import pandas as pd
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        # Convert to DataFrame if needed
        if isinstance(results, dict):
            df = pd.DataFrame(results)
        else:
            df = results
            
        df.to_csv(filepath, index=True)
        
        logger.info(f"Results saved to: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")
        return ""


def create_colab_notebook(
    output_path: str = "bist100_regime_detector_colab.ipynb"
) -> str:
    """
    Create a Colab-compatible notebook.
    
    Args:
        output_path: Output path for notebook
        
    Returns:
        Path to created notebook
    """
    import json
    
    # Notebook structure
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Turkish Market Regime Detector\n",
                    "## Google Colab Compatible Version\n",
                    "\n",
                    "This notebook detects market regimes in BIST100 using K-Means and Hidden Markov Models."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Install dependencies\n",
                    "!pip install yfinance pandas numpy scikit-learn hmmlearn plotly -q"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Import libraries\n",
                    "import sys\n",
                    "sys.path.append('/content/src')\n",
                    "\n",
                    "from src.data.yfinance_fetcher import YFinanceFetcher\n",
                    "from src.data.processor import DataProcessor\n",
                    "from src.models.kmeans_model import KMeansRegimeModel\n",
                    "from src.models.hmm_model import HMMRegimeModel\n",
                    "from src.visualization.plots import RegimePlotter\n",
                    "import pandas as pd\n",
                    "import numpy as np"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Fetch data\n",
                    "fetcher = YFinanceFetcher()\n",
                    "tickers = [\"THYAO.IS\", \"GARAN.IS\", \"AKBNK.IS\", \"SISE.IS\", \"ASELS.IS\"]\n",
                    "prices = fetcher.fetch_multiple_tickers(tickers)\n",
                    "print(f\"Fetched {len(prices)} rows of data\")\n",
                    "prices.head()"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Create features and train model\n",
                    "processor = DataProcessor()\n",
                    "features = processor.create_features(prices)\n",
                    "features_norm = processor.normalize_features(features)\n",
                    "\n",
                    "# Train K-Means\n",
                    "kmeans = KMeansRegimeModel(n_regimes=3)\n",
                    "kmeans.fit(features_norm)\n",
                    "regimes = kmeans.predict(features_norm)\n",
                    "\n",
                    "print(f\"Regime distribution: {pd.Series(regimes).value_counts().to_dict()}\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Create visualization\n",
                    "plotter = RegimePlotter()\n",
                    "fig = plotter.plot_prices_with_regimes(prices, regimes)\n",
                    "fig.show()"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Save notebook
    with open(output_path, 'w') as f:
        json.dump(notebook, f, indent=2)
    
    logger.info(f"Colab notebook created at: {output_path}")
    return output_path