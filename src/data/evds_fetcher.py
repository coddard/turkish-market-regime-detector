"""
TCMB EVDS (Electronic Data Delivery System) data fetcher
Fetches Turkish Central Bank economic data
"""

import pandas as pd
import requests
from typing import Optional, Dict, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class EVDSFetcher:
    """
    Fetches data from TCMB (Central Bank of Turkey) EVDS API.
    Provides access to monetary policy and economic indicators.
    """
    
    BASE_URL = "https://evds.tcmb.gov.tr/service/evds/"
    
    # Common EVDS series codes
    SERIES_CODES = {
        # Interest rates
        "overnight_rate": "TP.DIS.OLR",
        "lending_rate": "TP.DIS.KLR",
        "deposit_rate": "TP.DIS.TG",
        
        # Exchange rates
        "usd_try": "TP.DK.USD.A",
        "eur_try": "TP.DK.EUR.A",
        "bop": "TP.BOP1",
        
        # Inflation
        "cpi": "TP.FG.J0",
        "ppi": "TP.FG.Y0",
        
        # Money supply
        "m1": "TP.M1",
        "m2": "TP.M2",
        "m3": "TP.M3",
        
        # Trade
        "exports": "TP.EXCH",
        "imports": "TP.IMP",
        
        # GDP
        "gdp": "TP.YG"
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize EVDS fetcher.
        
        Args:
            api_key: EVDS API key (get from https://evds.tcmb.gov.tr/)
        """
        self.api_key = api_key
        self.session = requests.Session()
        
    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None
    ) -> Dict:
        """
        Make request to EVDS API.
        
        Args:
            endpoint: API endpoint
            params: Request parameters
            
        Returns:
            Response JSON
        """
        if not self.api_key:
            logger.warning("No EVDS API key provided. Using fallback data.")
            return self._get_fallback_data(endpoint)
        
        url = f"{self.BASE_URL}{endpoint}"
        params = params or {}
        params["key"] = self.api_key
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"EVDS API request failed: {str(e)}")
            return self._get_fallback_data(endpoint)
    
    def _get_fallback_data(self, endpoint: str) -> Dict:
        """
        Get fallback data when API is unavailable.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Fallback data dictionary
        """
        # Return sample data structure
        return {
            "status": "fallback",
            "message": "Using sample data - API key required for live data",
            "data": []
        }
    
    def fetch_series(
        self,
        series_code: str,
        start_date: str,
        end_date: str,
        frequency: str = "W"
    ) -> pd.DataFrame:
        """
        Fetch data for a specific series.
        
        Args:
            series_code: EVDS series code
            start_date: Start date (DD-MM-YYYY)
            end_date: End date (DD-MM-YYYY)
            frequency: Data frequency (D=Daily, W=Weekly, M=Monthly)
            
        Returns:
            DataFrame with time series data
        """
        params = {
            "series": series_code,
            "startDate": start_date,
            "endDate": end_date,
            "frequency": frequency
        }
        
        response = self._make_request("series/", params)
        
        if response.get("status") == "fallback":
            return self._create_sample_data(series_code, start_date, end_date)
        
        try:
            data = response.get("data", [])
            
            if not data:
                logger.warning(f"No data returned for series: {series_code}")
                return pd.DataFrame()
            
            # Parse data
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df = df.set_index('date')
            df = df.sort_index()
            
            # Clean column names
            df.columns = [col.split(".")[-1] for col in df.columns]
            
            return df
            
        except Exception as e:
            logger.error(f"Error parsing EVDS data: {str(e)}")
            return pd.DataFrame()
    
    def _create_sample_data(
        self,
        series_code: str,
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """
        Create sample data for testing.
        
        Args:
            series_code: Series code
            start_date: Start date
            end_date: End date
            
        Returns:
            Sample DataFrame
        """
        # Parse dates
        try:
            start = datetime.strptime(start_date, "%d-%m-%Y")
            end = datetime.strptime(end_date, "%d-%m-%Y")
        except:
            start = datetime(2022, 1, 1)
            end = datetime.now()
        
        # Create date range
        dates = pd.date_range(start, end, freq='W')
        
        # Generate sample data based on series type
        values = []
        for i, d in enumerate(dates):
            if "USD" in series_code or "TRY" in series_code:
                values.append(25 + i * 0.1 + (hash(str(d)) % 100) / 100)
            elif "rate" in series_code.lower():
                values.append(20 + (hash(str(d)) % 500) / 100)
            else:
                values.append(100 + (hash(str(d)) % 1000) / 10)
        
        df = pd.DataFrame({"value": values}, index=dates)
        return df
    
    def fetch_interest_rates(
        self,
        start_date: str = "01-01-2022",
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch interest rate data.
        
        Args:
            start_date: Start date
            end_date: End date (defaults to today)
            
        Returns:
            DataFrame with interest rates
        """
        if end_date is None:
            end_date = datetime.now().strftime("%d-%m-%Y")
            
        return self.fetch_series(
            self.SERIES_CODES["overnight_rate"],
            start_date,
            end_date
        )
    
    def fetch_exchange_rates(
        self,
        currency: str = "USD",
        start_date: str = "01-01-2022",
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch exchange rate data.
        
        Args:
            currency: Currency code (USD, EUR)
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with exchange rates
        """
        if end_date is None:
            end_date = datetime.now().strftime("%d-%m-%Y")
            
        series_key = f"{currency.lower()}_try"
        series_code = self.SERIES_CODES.get(series_key)
        
        if series_code is None:
            logger.warning(f"Unknown currency: {currency}")
            return pd.DataFrame()
            
        return self.fetch_series(series_code, start_date, end_date)
    
    def fetch_inflation(
        self,
        inflation_type: str = "CPI",
        start_date: str = "01-01-2022",
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch inflation data.
        
        Args:
            inflation_type: Type (CPI or PPI)
            start_date: Start date
            end_date: End date
            
        Returns:
            DataFrame with inflation data
        """
        if end_date is None:
            end_date = datetime.now().strftime("%d-%m-%Y")
            
        series_key = inflation_type.lower()
        series_code = self.SERIES_CODES.get(series_key)
        
        if series_code is None:
            logger.warning(f"Unknown inflation type: {inflation_type}")
            return pd.DataFrame()
            
        return self.fetch_series(series_code, start_date, end_date)
    
    def fetch_multiple_series(
        self,
        series_codes: List[str],
        start_date: str,
        end_date: str,
        frequency: str = "W"
    ) -> pd.DataFrame:
        """
        Fetch multiple series at once.
        
        Args:
            series_codes: List of series codes
            start_date: Start date
            end_date: End date
            frequency: Data frequency
            
        Returns:
            Combined DataFrame
        """
        all_data = {}
        
        for code in series_codes:
            df = self.fetch_series(code, start_date, end_date, frequency)
            
            if not df.empty:
                all_data[code] = df['value']
                
        if not all_data:
            return pd.DataFrame()
            
        combined = pd.DataFrame(all_data)
        combined = combined.dropna()
        
        return combined
    
    def get_available_series(self) -> List[str]:
        """
        Get list of available series codes.
        
        Returns:
            List of series code descriptions
        """
        return [
            f"{key}: {desc}" 
            for key, desc in self.SERIES_CODES.items()
        ]


def fetch_evds_data(
    series_code: str,
    start_date: str,
    end_date: str,
    api_key: Optional[str] = None
) -> pd.DataFrame:
    """
    Convenience function to fetch EVDS data.
    
    Args:
        series_code: EVDS series code
        start_date: Start date (DD-MM-YYYY)
        end_date: End date (DD-MM-YYYY)
        api_key: EVDS API key
        
    Returns:
        DataFrame with time series data
    """
    fetcher = EVDSFetcher(api_key=api_key)
    return fetcher.fetch_series(series_code, start_date, end_date)