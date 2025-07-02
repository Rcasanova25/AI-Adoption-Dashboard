"""
OECD Real-time Data Integration Module
======================================

This module provides a comprehensive client for fetching real-time economic indicators
from the OECD SDMX API to enhance causal analysis in the AI Adoption Dashboard.

Features:
- Multiple OECD indicator support
- Caching with TTL
- Error handling and retries
- Data validation and cleaning
- Time series alignment
- Production-ready logging
"""

import os
import json
import time
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from functools import lru_cache
from urllib.parse import urlencode
import requests
import pandas as pd
import numpy as np
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OECDDataCache:
    """Simple file-based cache with TTL support"""
    
    def __init__(self, cache_dir: str = "./cache/oecd", default_ttl: int = 3600):
        self.cache_dir = cache_dir
        self.default_ttl = default_ttl
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        """Generate cache file path from key"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{key_hash}.json")
    
    def get(self, key: str) -> Optional[Any]:
        """Retrieve cached data if valid"""
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cached_time > timedelta(seconds=cache_data['ttl']):
                os.remove(cache_path)
                return None
            
            return cache_data['data']
        except Exception as e:
            logger.warning(f"Cache read error: {e}")
            return None
    
    def set(self, key: str, data: Any, ttl: Optional[int] = None) -> None:
        """Store data in cache"""
        cache_path = self._get_cache_path(key)
        ttl = ttl or self.default_ttl
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'ttl': ttl,
            'data': data
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f)
        except Exception as e:
            logger.warning(f"Cache write error: {e}")


class OECDIndicator:
    """Configuration for OECD indicators"""
    
    def __init__(self, name: str, dataset: str, series_key: str, 
                 description: str, unit: str = None):
        self.name = name
        self.dataset = dataset
        self.series_key = series_key
        self.description = description
        self.unit = unit


class OECDRealTimeClient:
    """
    OECD SDMX API Client for real-time economic data
    
    Provides access to multiple economic indicators to enhance
    causal analysis capabilities of the AI Adoption Dashboard.
    """
    
    BASE_URL = "https://sdmx.oecd.org/public/rest/data"
    
    # Define available indicators
    INDICATORS = {
        'cli': OECDIndicator(
            name='Composite Leading Indicators',
            dataset='OECD.SDD.STES,DSD_STES@DF_CLI',
            series_key='.M.LI...AA...H',
            description='Leading economic indicators for forecasting turning points',
            unit='Index'
        ),
        'gdp_growth': OECDIndicator(
            name='GDP Growth Rate',
            dataset='OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA_EXPENDITURE_GROWTH',
            series_key='.Q.N.B1GQ.DOBSA.G1',
            description='Quarterly GDP growth rates',
            unit='Percentage'
        ),
        'productivity': OECDIndicator(
            name='Labour Productivity',
            dataset='OECD.SDD.NAD,DSD_NAMAIN7@DF_PROD_EMP',
            series_key='.A.PDTY.VPVOB',
            description='GDP per hour worked',
            unit='Index'
        ),
        'employment': OECDIndicator(
            name='Employment Rate',
            dataset='OECD.SDD.NAD,DSD_NAMAIN1@DF_QNA_EXPENDITURE',
            series_key='.Q.EMP.DOBSA.PC_WAPOP',
            description='Employment to working age population ratio',
            unit='Percentage'
        ),
        'business_confidence': OECDIndicator(
            name='Business Confidence Index',
            dataset='OECD.SDD.STES,DSD_STES@DF_BSCI',
            series_key='.M.BS.BLSA',
            description='Business sentiment and expectations',
            unit='Index'
        ),
        'innovation': OECDIndicator(
            name='R&D Expenditure',
            dataset='OECD.STI.STP,DSD_MSTI@DF_MSTI',
            series_key='.GERD.PC_GDP',
            description='Gross domestic expenditure on R&D as % of GDP',
            unit='Percentage'
        )
    }
    
    def __init__(self, cache_ttl: int = 3600, timeout: int = 30, max_retries: int = 3):
        """
        Initialize OECD client
        
        Args:
            cache_ttl: Cache time-to-live in seconds (default: 1 hour)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.cache = OECDDataCache(default_ttl=cache_ttl)
        self.timeout = timeout
        self.session = self._create_session(max_retries)
        logger.info("OECD Real-time Client initialized")
    
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create requests session with retry logic"""
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def _build_url(self, indicator: OECDIndicator, countries: List[str] = None,
                   start_period: str = None, end_period: str = None) -> str:
        """Build OECD API URL"""
        # Base URL with dataset and series
        url = f"{self.BASE_URL}/{indicator.dataset}/{indicator.series_key}"
        
        # Add country filter if specified
        if countries:
            country_filter = '+'.join(countries)
            url = url.replace('.', f'{country_filter}.', 1)
        
        # Query parameters
        params = {
            'dimensionAtObservation': 'AllDimensions',
            'format': 'csvfilewithlabels'
        }
        
        if start_period:
            params['startPeriod'] = start_period
        if end_period:
            params['endPeriod'] = end_period
        
        return f"{url}?{urlencode(params)}"
    
    def _parse_csv_response(self, response_text: str) -> pd.DataFrame:
        """Parse CSV response from OECD API"""
        try:
            # Read CSV data
            from io import StringIO
            df = pd.read_csv(StringIO(response_text))
            
            # Standardize column names
            df.columns = [col.strip().upper() for col in df.columns]
            
            # Ensure we have required columns
            required_cols = ['REF_AREA', 'TIME_PERIOD', 'OBS_VALUE']
            missing_cols = [col for col in required_cols if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            # Convert time period to datetime
            if 'TIME_PERIOD' in df.columns:
                df['TIME_PERIOD'] = pd.to_datetime(df['TIME_PERIOD'])
            
            # Convert observation value to numeric
            if 'OBS_VALUE' in df.columns:
                df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'], errors='coerce')
            
            # Remove rows with missing values
            df = df.dropna(subset=['OBS_VALUE'])
            
            return df
            
        except Exception as e:
            logger.error(f"Error parsing CSV response: {e}")
            raise
    
    def fetch_indicator(self, indicator_key: str, countries: List[str] = None,
                       start_period: str = None, end_period: str = None,
                       use_cache: bool = True) -> pd.DataFrame:
        """
        Fetch data for a specific indicator
        
        Args:
            indicator_key: Key from INDICATORS dict
            countries: List of ISO country codes (default: all OECD)
            start_period: Start date (YYYY-MM format)
            end_period: End date (YYYY-MM format)
            use_cache: Whether to use cached data
            
        Returns:
            DataFrame with indicator data
        """
        if indicator_key not in self.INDICATORS:
            raise ValueError(f"Unknown indicator: {indicator_key}")
        
        indicator = self.INDICATORS[indicator_key]
        
        # Generate cache key
        cache_key = f"{indicator_key}_{countries}_{start_period}_{end_period}"
        
        # Check cache first
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data is not None:
                logger.info(f"Using cached data for {indicator.name}")
                return pd.DataFrame(cached_data)
        
        # Build URL
        url = self._build_url(indicator, countries, start_period, end_period)
        logger.info(f"Fetching {indicator.name} from OECD API")
        
        try:
            # Make request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Parse response
            df = self._parse_csv_response(response.text)
            
            # Add metadata
            df['INDICATOR'] = indicator_key
            df['INDICATOR_NAME'] = indicator.name
            df['UNIT'] = indicator.unit
            
            # Cache the result
            if use_cache:
                self.cache.set(cache_key, df.to_dict('records'))
            
            logger.info(f"Successfully fetched {len(df)} records for {indicator.name}")
            return df
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for {indicator.name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching {indicator.name}: {e}")
            raise
    
    def fetch_multiple_indicators(self, indicator_keys: List[str] = None,
                                countries: List[str] = None,
                                start_period: str = None,
                                end_period: str = None) -> Dict[str, pd.DataFrame]:
        """
        Fetch multiple indicators in parallel
        
        Args:
            indicator_keys: List of indicator keys (default: all)
            countries: List of ISO country codes
            start_period: Start date
            end_period: End date
            
        Returns:
            Dictionary mapping indicator keys to DataFrames
        """
        if indicator_keys is None:
            indicator_keys = list(self.INDICATORS.keys())
        
        results = {}
        errors = {}
        
        for key in indicator_keys:
            try:
                df = self.fetch_indicator(key, countries, start_period, end_period)
                results[key] = df
            except Exception as e:
                logger.error(f"Failed to fetch {key}: {e}")
                errors[key] = str(e)
        
        if errors:
            logger.warning(f"Failed to fetch {len(errors)} indicators: {list(errors.keys())}")
        
        return results
    
    def get_latest_values(self, indicator_key: str, countries: List[str] = None) -> pd.DataFrame:
        """Get the most recent values for an indicator"""
        # Fetch last 3 months of data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        df = self.fetch_indicator(
            indicator_key,
            countries,
            start_date.strftime('%Y-%m'),
            end_date.strftime('%Y-%m')
        )
        
        # Get latest value for each country
        if not df.empty:
            latest = df.sort_values('TIME_PERIOD').groupby('REF_AREA').last()
            return latest.reset_index()
        
        return df
    
    def align_time_series(self, data: Dict[str, pd.DataFrame], 
                         frequency: str = 'M') -> pd.DataFrame:
        """
        Align multiple time series to common dates
        
        Args:
            data: Dictionary of indicator DataFrames
            frequency: Target frequency (M=monthly, Q=quarterly)
            
        Returns:
            Aligned DataFrame with all indicators
        """
        aligned_dfs = []
        
        for indicator_key, df in data.items():
            if df.empty:
                continue
            
            # Pivot to wide format
            pivot = df.pivot_table(
                index='TIME_PERIOD',
                columns='REF_AREA',
                values='OBS_VALUE',
                aggfunc='mean'
            )
            
            # Add indicator suffix to column names
            pivot.columns = [f"{col}_{indicator_key}" for col in pivot.columns]
            
            aligned_dfs.append(pivot)
        
        if not aligned_dfs:
            return pd.DataFrame()
        
        # Merge all indicators
        result = pd.concat(aligned_dfs, axis=1)
        
        # Resample to target frequency
        if frequency:
            result = result.resample(frequency).mean()
        
        # Forward fill missing values (up to 3 periods)
        result = result.fillna(method='ffill', limit=3)
        
        return result
    
    def calculate_correlations(self, aligned_data: pd.DataFrame,
                             target_column: str = None) -> pd.DataFrame:
        """
        Calculate correlations between indicators
        
        Args:
            aligned_data: Aligned time series data
            target_column: Column to correlate against (optional)
            
        Returns:
            Correlation matrix or series
        """
        if aligned_data.empty:
            return pd.DataFrame()
        
        if target_column and target_column in aligned_data.columns:
            # Correlate all columns with target
            correlations = aligned_data.corr()[target_column].sort_values(ascending=False)
            return correlations
        else:
            # Full correlation matrix
            return aligned_data.corr()
    
    def get_indicator_summary(self) -> pd.DataFrame:
        """Get summary of available indicators"""
        summary_data = []
        
        for key, indicator in self.INDICATORS.items():
            summary_data.append({
                'key': key,
                'name': indicator.name,
                'description': indicator.description,
                'dataset': indicator.dataset,
                'unit': indicator.unit
            })
        
        return pd.DataFrame(summary_data)


class OECDIntegration:
    """
    High-level integration class for AI Adoption Dashboard
    
    Provides simplified interface for fetching and analyzing OECD data
    to enhance causal analysis capabilities.
    """
    
    def __init__(self, cache_ttl: int = 3600):
        self.client = OECDRealTimeClient(cache_ttl=cache_ttl)
        self.last_update = None
        logger.info("OECD Integration initialized")
    
    def fetch_causal_indicators(self, countries: List[str] = None,
                              months_back: int = 24) -> Dict[str, pd.DataFrame]:
        """
        Fetch all indicators relevant for causal analysis
        
        Args:
            countries: List of countries (default: G7)
            months_back: Number of months of historical data
            
        Returns:
            Dictionary of indicator DataFrames
        """
        if countries is None:
            # Default to G7 countries
            countries = ['USA', 'JPN', 'DEU', 'GBR', 'FRA', 'ITA', 'CAN']
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months_back * 30)
        
        # Fetch all indicators
        indicators = ['cli', 'gdp_growth', 'productivity', 'business_confidence']
        
        data = self.client.fetch_multiple_indicators(
            indicators,
            countries,
            start_date.strftime('%Y-%m'),
            end_date.strftime('%Y-%m')
        )
        
        self.last_update = datetime.now()
        return data
    
    def get_aligned_dataset(self, countries: List[str] = None,
                          months_back: int = 24) -> pd.DataFrame:
        """
        Get all indicators aligned to common time periods
        
        Returns:
            DataFrame with all indicators aligned by date and country
        """
        # Fetch data
        data = self.fetch_causal_indicators(countries, months_back)
        
        # Align time series
        aligned = self.client.align_time_series(data, frequency='M')
        
        return aligned
    
    def analyze_leading_indicators(self, target_data: pd.Series,
                                 countries: List[str] = None) -> Dict[str, Any]:
        """
        Analyze relationship between OECD indicators and target variable
        
        Args:
            target_data: Time series to analyze (e.g., AI adoption metrics)
            countries: Countries to include
            
        Returns:
            Analysis results including correlations and lag analysis
        """
        # Get aligned OECD data
        oecd_data = self.get_aligned_dataset(countries)
        
        # Ensure target data is aligned
        target_aligned = target_data.reindex(oecd_data.index)
        
        # Calculate correlations
        correlations = {}
        for col in oecd_data.columns:
            corr = oecd_data[col].corr(target_aligned)
            if not np.isnan(corr):
                correlations[col] = corr
        
        # Lag analysis - check if OECD indicators lead the target
        lag_correlations = {}
        for lag in range(1, 7):  # Check up to 6 months lag
            lag_corr = {}
            for col in oecd_data.columns:
                lagged_series = oecd_data[col].shift(lag)
                corr = lagged_series.corr(target_aligned)
                if not np.isnan(corr):
                    lag_corr[col] = corr
            lag_correlations[f'lag_{lag}'] = lag_corr
        
        # Find best predictors
        best_predictors = sorted(correlations.items(), 
                               key=lambda x: abs(x[1]), 
                               reverse=True)[:5]
        
        return {
            'correlations': correlations,
            'lag_correlations': lag_correlations,
            'best_predictors': best_predictors,
            'n_observations': len(target_aligned),
            'date_range': (oecd_data.index.min(), oecd_data.index.max())
        }
    
    def update_data(self, force: bool = False) -> bool:
        """
        Update cached data if needed
        
        Args:
            force: Force update regardless of cache
            
        Returns:
            True if data was updated
        """
        if force:
            # Clear cache
            import shutil
            cache_dir = "./cache/oecd"
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir)
        
        # Fetch fresh data
        try:
            self.fetch_causal_indicators()
            logger.info("OECD data updated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to update OECD data: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Initialize integration
    oecd = OECDIntegration()
    
    # Get indicator summary
    print("Available OECD Indicators:")
    print(oecd.client.get_indicator_summary())
    
    # Fetch latest CLI data for G7
    print("\nFetching latest Composite Leading Indicators...")
    cli_data = oecd.client.get_latest_values('cli', ['USA', 'JPN', 'DEU'])
    print(cli_data)
    
    # Get aligned dataset
    print("\nGetting aligned dataset for causal analysis...")
    aligned = oecd.get_aligned_dataset(countries=['USA', 'GBR'], months_back=12)
    print(f"Aligned data shape: {aligned.shape}")
    print(f"Date range: {aligned.index.min()} to {aligned.index.max()}")
    
    # Example: Analyze relationship with mock AI adoption data
    if not aligned.empty:
        # Create mock AI adoption time series
        mock_adoption = pd.Series(
            np.random.randn(len(aligned)) + np.arange(len(aligned)) * 0.1,
            index=aligned.index,
            name='ai_adoption_score'
        )
        
        print("\nAnalyzing leading indicators...")
        analysis = oecd.analyze_leading_indicators(mock_adoption, ['USA'])
        print(f"Top predictors: {analysis['best_predictors'][:3]}")