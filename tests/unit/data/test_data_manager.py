"""Unit tests for DataManager class."""

import pytest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
from datetime import datetime

from data.data_manager import DataManager
from data.models import DataSource
from tests.fixtures.mock_data import (
    generate_adoption_data,
    generate_industry_data,
    generate_geographic_data
)


class TestDataManager:
    """Test suite for DataManager functionality."""
    
    @pytest.fixture
    def data_manager(self):
        """Create a DataManager instance for testing."""
        return DataManager()
    
    @pytest.fixture
    def mock_loaders(self):
        """Create mock loaders for testing."""
        mock_ai_index = Mock()
        mock_ai_index.load.return_value = {
            'adoption_rates': generate_adoption_data(),
            'industry_analysis': generate_industry_data()
        }
        
        mock_mckinsey = Mock()
        mock_mckinsey.load.return_value = {
            'competitive_position': pd.DataFrame({
                'company': ['A', 'B', 'C'],
                'score': [8.5, 7.2, 6.8]
            })
        }
        
        return {
            'AIIndexLoader': mock_ai_index,
            'McKinseyLoader': mock_mckinsey
        }
    
    def test_initialization(self, data_manager):
        """Test DataManager initialization."""
        assert isinstance(data_manager.loaders, dict)
        assert isinstance(data_manager.cache, dict)
        assert data_manager.cache_duration == 3600
    
    @patch('data.data_manager.AIIndexLoader')
    @patch('data.data_manager.McKinseyLoader')
    def test_initialize_loaders(self, mock_mckinsey_class, mock_ai_index_class, data_manager):
        """Test loader initialization."""
        # Setup mocks
        mock_ai_index_class.return_value = Mock()
        mock_mckinsey_class.return_value = Mock()
        
        # Initialize loaders
        data_manager._initialize_loaders()
        
        # Verify loaders created
        assert 'ai_index' in data_manager.loaders
        assert 'mckinsey' in data_manager.loaders
        mock_ai_index_class.assert_called_once()
        mock_mckinsey_class.assert_called_once()
    
    def test_get_data_with_cache_hit(self, data_manager):
        """Test getting data when cache is valid."""
        # Setup cache
        test_data = {'test': 'data'}
        data_manager.cache['ai_index'] = {
            'data': test_data,
            'timestamp': datetime.now()
        }
        
        # Get data
        result = data_manager.get_data('ai_index')
        
        # Verify cache hit
        assert result == test_data
    
    def test_get_data_with_cache_miss(self, data_manager, mock_loaders):
        """Test getting data when cache is expired or missing."""
        # Setup mock loader
        data_manager.loaders['ai_index'] = mock_loaders['AIIndexLoader']
        
        # Get data (cache miss)
        result = data_manager.get_data('ai_index')
        
        # Verify loader called
        mock_loaders['AIIndexLoader'].load.assert_called_once()
        assert result == mock_loaders['AIIndexLoader'].load.return_value
    
    def test_get_data_invalid_source(self, data_manager):
        """Test getting data from invalid source."""
        result = data_manager.get_data('invalid_source')
        assert result == {}
    
    def test_cache_expiration(self, data_manager, mock_loaders):
        """Test cache expiration logic."""
        # Setup expired cache
        from datetime import timedelta
        expired_time = datetime.now() - timedelta(seconds=3700)  # Expired
        
        data_manager.cache['ai_index'] = {
            'data': {'old': 'data'},
            'timestamp': expired_time
        }
        data_manager.loaders['ai_index'] = mock_loaders['AIIndexLoader']
        
        # Get data
        result = data_manager.get_data('ai_index')
        
        # Verify loader called due to expiration
        mock_loaders['AIIndexLoader'].load.assert_called_once()
        assert result == mock_loaders['AIIndexLoader'].load.return_value
    
    def test_get_all_data(self, data_manager, mock_loaders):
        """Test getting all data from all sources."""
        # Setup loaders
        data_manager.loaders = {
            'ai_index': mock_loaders['AIIndexLoader'],
            'mckinsey': mock_loaders['McKinseyLoader']
        }
        
        # Get all data
        result = data_manager.get_all_data()
        
        # Verify all loaders called
        assert 'ai_index' in result
        assert 'mckinsey' in result
        mock_loaders['AIIndexLoader'].load.assert_called_once()
        mock_loaders['McKinseyLoader'].load.assert_called_once()
    
    def test_refresh_cache(self, data_manager, mock_loaders):
        """Test cache refresh functionality."""
        # Setup cache and loader
        data_manager.cache['ai_index'] = {
            'data': {'old': 'data'},
            'timestamp': datetime.now()
        }
        data_manager.loaders['ai_index'] = mock_loaders['AIIndexLoader']
        
        # Refresh specific source
        data_manager.refresh_cache('ai_index')
        
        # Verify loader called
        mock_loaders['AIIndexLoader'].load.assert_called_once()
        
        # Verify cache updated
        assert data_manager.cache['ai_index']['data'] == \
               mock_loaders['AIIndexLoader'].load.return_value
    
    def test_clear_cache(self, data_manager):
        """Test clearing cache."""
        # Setup cache
        data_manager.cache = {
            'ai_index': {'data': 'test1'},
            'mckinsey': {'data': 'test2'}
        }
        
        # Clear cache
        data_manager.clear_cache()
        
        # Verify cache empty
        assert len(data_manager.cache) == 0
    
    def test_get_combined_dataset(self, data_manager, mock_loaders):
        """Test getting combined dataset from multiple sources."""
        # Setup loaders
        data_manager.loaders = {
            'ai_index': mock_loaders['AIIndexLoader'],
            'mckinsey': mock_loaders['McKinseyLoader']
        }
        
        # Get combined adoption data
        result = data_manager.get_combined_dataset('adoption_rates')
        
        # Verify data combined
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
    
    def test_error_handling_in_loader(self, data_manager):
        """Test error handling when loader fails."""
        # Create failing loader
        failing_loader = Mock()
        failing_loader.load.side_effect = Exception("Load failed")
        
        data_manager.loaders['failing'] = failing_loader
        
        # Get data should return empty dict
        result = data_manager.get_data('failing')
        assert result == {}
    
    def test_concurrent_access(self, data_manager, mock_loaders):
        """Test thread-safe concurrent access to cache."""
        import threading
        
        data_manager.loaders['ai_index'] = mock_loaders['AIIndexLoader']
        
        def access_data():
            data_manager.get_data('ai_index')
        
        # Create multiple threads
        threads = [threading.Thread(target=access_data) for _ in range(5)]
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Verify loader called only once (cache worked)
        assert mock_loaders['AIIndexLoader'].load.call_count == 1
    
    def test_get_data_sources(self, data_manager):
        """Test getting list of available data sources."""
        data_manager.loaders = {
            'ai_index': Mock(),
            'mckinsey': Mock(),
            'goldman': Mock()
        }
        
        sources = data_manager.get_data_sources()
        
        assert len(sources) == 3
        assert 'ai_index' in sources
        assert 'mckinsey' in sources
        assert 'goldman' in sources
    
    def test_validate_data_integrity(self, data_manager, mock_loaders):
        """Test data validation after loading."""
        # Setup loader with test data
        test_df = generate_adoption_data()
        mock_loaders['AIIndexLoader'].load.return_value = {
            'adoption_rates': test_df
        }
        data_manager.loaders['ai_index'] = mock_loaders['AIIndexLoader']
        
        # Get data
        result = data_manager.get_data('ai_index')
        
        # Verify data integrity
        assert 'adoption_rates' in result
        df = result['adoption_rates']
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert 'date' in df.columns
        assert 'adoption_rate' in df.columns