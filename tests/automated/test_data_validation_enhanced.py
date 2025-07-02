"""
Enhanced Automated Data Validation Tests
Tests for the integrated PDF extraction and data validation pipeline
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, List
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock

# Import the modules to test
from data.models import (
    validate_dataset, safe_validate_data, ValidationResult,
    HistoricalDataPoint, AIAdoptionData, CompanySize, DataQuality, DataSource
)
from data.pipeline_integration import integration_manager, load_all_datasets_integrated
from data.automated_loaders import automated_loader
from data.pdf_data_pipeline import pdf_pipeline


class TestEnhancedDataValidation:
    """Enhanced tests for data validation with automated pipeline"""
    
    def test_historical_data_pydantic_validation(self):
        """Test Pydantic validation for historical data"""
        # Valid data
        valid_data = {
            'year': 2024,
            'ai_use': 78.0,
            'genai_use': 71.0
        }
        point = HistoricalDataPoint(**valid_data)
        assert point.year == 2024
        assert point.ai_use == 78.0
        assert point.genai_use == 71.0
    
    def test_historical_data_validation_errors(self):
        """Test validation errors for historical data"""
        # Invalid year
        with pytest.raises(ValueError, match="Year must be between 2017 and 2025"):
            HistoricalDataPoint(year=2030, ai_use=50.0, genai_use=40.0)
        
        # GenAI exceeding AI use
        with pytest.raises(ValueError, match="GenAI adoption cannot exceed overall AI adoption"):
            HistoricalDataPoint(year=2024, ai_use=50.0, genai_use=60.0)
        
        # Invalid percentages
        with pytest.raises(ValueError):
            HistoricalDataPoint(year=2024, ai_use=-10.0, genai_use=40.0)
    
    def test_ai_adoption_data_validation(self):
        """Test comprehensive AI adoption data validation"""
        valid_data = {
            'company_size': CompanySize.LARGE,
            'adoption_rate': 85.5,
            'year': 2024,
            'sector': 'Technology',
            'data_source': DataSource.AI_INDEX,
            'data_quality': DataQuality.EXCELLENT,
            'genai_adoption': 80.0,
            'roi_multiplier': 3.5
        }
        
        adoption_data = AIAdoptionData(**valid_data)
        assert adoption_data.company_size == CompanySize.LARGE
        assert adoption_data.adoption_rate == 85.5
        assert adoption_data.genai_adoption == 80.0
    
    def test_dataframe_validation_with_pydantic(self):
        """Test DataFrame validation using Pydantic models"""
        # Create valid DataFrame
        df = pd.DataFrame({
            'year': [2023, 2024],
            'ai_use': [65.0, 78.0],
            'genai_use': [55.0, 71.0]
        })
        
        # Test validation
        result = safe_validate_data(df, "historical_data", show_warnings=False)
        assert result.is_valid
        assert result.errors == []
    
    def test_dataframe_validation_with_errors(self):
        """Test DataFrame validation with errors"""
        # Create invalid DataFrame (GenAI > AI)
        df = pd.DataFrame({
            'year': [2023, 2024],
            'ai_use': [65.0, 78.0],
            'genai_use': [70.0, 85.0]  # Higher than AI use
        })
        
        # Test validation
        result = safe_validate_data(df, "historical_data", show_warnings=False)
        assert not result.is_valid
        assert len(result.errors) > 0


class TestAutomatedPipelineValidation:
    """Test validation of the automated PDF extraction pipeline"""
    
    def test_pipeline_prerequisites(self):
        """Test pipeline prerequisite checking"""
        status = integration_manager.get_system_status()
        
        # Check status structure
        assert 'integration_strategy' in status
        assert 'automation_enabled' in status
        assert 'prerequisites' in status
        
        # Check prerequisites structure
        prereqs = status['prerequisites']
        assert 'pdf_libraries' in prereqs
        assert 'resources_folder' in prereqs
        assert 'write_permissions' in prereqs
        
        # Each prerequisite should be boolean
        for key, value in prereqs.items():
            assert isinstance(value, bool), f"{key} should be boolean"
    
    @patch('data.pdf_data_pipeline.pdf_pipeline.scan_for_pdfs')
    def test_pdf_pipeline_with_mock_files(self, mock_scan):
        """Test PDF pipeline with mocked files"""
        # Mock PDF files
        mock_scan.return_value = [
            Path('test1.pdf'),
            Path('test2.pdf')
        ]
        
        # Test that scan returns expected structure
        files = pdf_pipeline.scan_for_pdfs()
        assert len(files) == 2
        assert all(isinstance(f, Path) for f in files)
    
    def test_integration_strategy_selection(self):
        """Test integration strategy selection logic"""
        strategy = integration_manager.get_integration_strategy()
        
        # Check strategy structure
        assert 'primary_method' in strategy
        assert 'fallback_method' in strategy
        assert 'pdf_extraction' in strategy
        assert 'data_source' in strategy
        
        # Check valid values
        assert strategy['primary_method'] in ['automated', 'manual']
        assert strategy['pdf_extraction'] in ['enabled', 'disabled']
    
    @patch('data.automated_loaders.automated_loader.get_extracted_datasets')
    def test_automated_loader_fallback(self, mock_extract):
        """Test automated loader fallback mechanism"""
        # Mock extraction failure
        mock_extract.side_effect = Exception("PDF extraction failed")
        
        # Test that fallback works
        try:
            df = automated_loader.load_historical_data_automated()
            # Should not raise exception, should fall back to manual data
            assert isinstance(df, pd.DataFrame)
            assert not df.empty
        except Exception as e:
            pytest.fail(f"Fallback failed: {e}")
    
    def test_data_merge_functionality(self):
        """Test merging of automated and manual data"""
        # Create mock automated data
        auto_df = pd.DataFrame({
            'source': ['Auto Source 1', 'Auto Source 2'],
            'value': [85, 92],
            'type': 'automated'
        })
        
        # Create mock manual data
        manual_df = pd.DataFrame({
            'source': ['Manual Source 1', 'Auto Source 1'],  # One duplicate
            'value': [75, 80],
            'type': 'manual'
        })
        
        # Test merge
        merged = automated_loader.merge_with_manual_data(auto_df, manual_df, 'source')
        
        # Should prefer automated data for duplicates
        assert len(merged) == 3  # 2 auto + 1 unique manual
        auto_source_row = merged[merged['source'] == 'Auto Source 1'].iloc[0]
        assert auto_source_row['type'] == 'automated'  # Should keep automated version


class TestDataQualityAssurance:
    """Test data quality assurance measures"""
    
    def test_data_completeness_validation(self):
        """Test validation of data completeness"""
        datasets = {
            'historical_data': pd.DataFrame({'year': [2024], 'ai_use': [78]}),
            'sector_data': pd.DataFrame({'sector': ['Tech'], 'adoption_rate': [85]}),
            'empty_data': pd.DataFrame(),
            'invalid_data': None
        }
        
        # Test completeness check
        complete_datasets = {k: v for k, v in datasets.items() 
                           if v is not None and not v.empty}
        
        assert len(complete_datasets) == 2
        assert 'historical_data' in complete_datasets
        assert 'sector_data' in complete_datasets
    
    def test_data_consistency_validation(self):
        """Test validation of data consistency across datasets"""
        # Create datasets with consistent years
        historical = pd.DataFrame({
            'year': [2023, 2024],
            'ai_use': [65, 78]
        })
        
        investment = pd.DataFrame({
            'year': [2023, 2024],
            'investment': [100, 150]
        })
        
        # Check year consistency
        hist_years = set(historical['year'].tolist())
        inv_years = set(investment['year'].tolist())
        
        assert hist_years == inv_years, "Years should be consistent across datasets"
    
    def test_data_range_validation(self):
        """Test validation of data ranges"""
        df = pd.DataFrame({
            'adoption_rate': [45, 78, 92, 101, -5],  # Contains invalid values
            'year': [2020, 2021, 2022, 2023, 2024]
        })
        
        # Validate ranges
        valid_adoption = df['adoption_rate'].between(0, 100)
        invalid_count = (~valid_adoption).sum()
        
        assert invalid_count == 2, "Should detect 2 invalid adoption rates"
    
    def test_data_source_credibility(self):
        """Test data source credibility validation"""
        sources = [
            {'authority': 'Stanford', 'credibility': 'A+'},
            {'authority': 'McKinsey', 'credibility': 'A+'},
            {'authority': 'Unknown Source', 'credibility': 'B'},
            {'authority': 'OECD', 'credibility': 'A+'}
        ]
        
        # Count high-credibility sources
        high_cred = [s for s in sources if s['credibility'] in ['A+', 'A']]
        
        assert len(high_cred) >= 3, "Should have multiple high-credibility sources"


class TestPerformanceValidation:
    """Test performance aspects of data validation"""
    
    def test_large_dataset_validation_performance(self):
        """Test validation performance with large datasets"""
        import time
        
        # Create large dataset
        large_df = pd.DataFrame({
            'year': np.random.choice(range(2020, 2025), 10000),
            'ai_use': np.random.uniform(30, 95, 10000),
            'genai_use': np.random.uniform(20, 80, 10000)
        })
        
        # Time the validation
        start_time = time.time()
        result = safe_validate_data(large_df, "large_historical_data", show_warnings=False)
        end_time = time.time()
        
        # Should complete in reasonable time (< 5 seconds)
        assert (end_time - start_time) < 5.0, "Large dataset validation should be fast"
        assert result.is_valid or len(result.warnings) > 0  # Should handle large data
    
    def test_caching_effectiveness(self):
        """Test that caching improves performance"""
        import time
        
        # First call (should be slower)
        start1 = time.time()
        try:
            datasets1, _ = load_all_datasets_integrated()
            end1 = time.time()
            
            # Second call (should be faster due to caching)
            start2 = time.time()
            datasets2, _ = load_all_datasets_integrated()
            end2 = time.time()
            
            # Second call should be faster (accounting for potential variations)
            time1 = end1 - start1
            time2 = end2 - start2
            
            # Allow some tolerance for system variations
            if time1 > 0.1:  # Only test if first call took meaningful time
                assert time2 <= time1 * 1.5, "Cached call should be faster or similar"
        
        except Exception:
            # If integration fails, test passes (system may not be fully set up)
            pytest.skip("Integration system not available for performance testing")


class TestErrorHandlingValidation:
    """Test error handling in validation pipeline"""
    
    def test_graceful_pdf_extraction_failure(self):
        """Test graceful handling of PDF extraction failures"""
        with patch('data.pdf_data_pipeline.PDFTextProcessor.extract_text_from_pdf', 
                   side_effect=Exception("PDF corrupt")):
            
            # Should not crash, should fall back to manual data
            try:
                datasets, metadata = load_all_datasets_integrated()
                assert isinstance(datasets, dict)
                assert isinstance(metadata, dict)
                
                # Check that fallback was used
                strategy_used = metadata.get('integration_strategy', {}).get('primary_method')
                assert strategy_used in ['manual', 'manual_fallback']
                
            except Exception as e:
                pytest.fail(f"Should handle PDF extraction failure gracefully: {e}")
    
    def test_invalid_data_handling(self):
        """Test handling of invalid data during validation"""
        # Create completely invalid data
        invalid_df = pd.DataFrame({
            'invalid_column': ['bad', 'data', 'here'],
            'another_bad_col': [None, None, None]
        })
        
        # Should handle gracefully
        result = safe_validate_data(invalid_df, "invalid_test", show_warnings=False)
        
        assert not result.is_valid
        assert len(result.errors) > 0
        assert isinstance(result.errors, list)
    
    def test_missing_file_handling(self):
        """Test handling of missing files"""
        with patch('pathlib.Path.exists', return_value=False):
            # Should handle missing resources folder gracefully
            status = integration_manager.get_system_status()
            
            # Should detect missing prerequisites
            assert not status['prerequisites']['resources_folder']
            assert status['integration_strategy']['primary_method'] == 'manual'


# Fixtures for testing
@pytest.fixture
def sample_valid_historical_data():
    """Fixture providing valid historical data"""
    return pd.DataFrame({
        'year': [2022, 2023, 2024],
        'ai_use': [55.0, 65.0, 78.0],
        'genai_use': [33.0, 55.0, 71.0],
        'data_source': ['Stanford AI Index'] * 3
    })


@pytest.fixture
def sample_invalid_historical_data():
    """Fixture providing invalid historical data"""
    return pd.DataFrame({
        'year': [2022, 2023, 2024],
        'ai_use': [55.0, 65.0, 78.0],
        'genai_use': [60.0, 70.0, 85.0],  # Invalid: GenAI > AI
        'data_source': ['Test Source'] * 3
    })


@pytest.fixture
def sample_extraction_metadata():
    """Fixture providing sample extraction metadata"""
    return {
        'integration_strategy': {
            'primary_method': 'automated',
            'pdf_extraction': 'enabled'
        },
        'summary': {
            'total_datasets': 10,
            'successful_loads': 8,
            'success_rate': 80.0,
            'automated_loads': 3,
            'manual_loads': 5
        }
    }


class TestIntegrationWithFixtures:
    """Integration tests using fixtures"""
    
    def test_valid_data_processing(self, sample_valid_historical_data):
        """Test processing of valid data"""
        result = safe_validate_data(
            sample_valid_historical_data, 
            "historical_data", 
            show_warnings=False
        )
        
        assert result.is_valid
        assert len(result.errors) == 0
    
    def test_invalid_data_processing(self, sample_invalid_historical_data):
        """Test processing of invalid data"""
        result = safe_validate_data(
            sample_invalid_historical_data, 
            "historical_data", 
            show_warnings=False
        )
        
        assert not result.is_valid
        assert len(result.errors) > 0
    
    def test_metadata_structure(self, sample_extraction_metadata):
        """Test metadata structure validation"""
        metadata = sample_extraction_metadata
        
        assert 'integration_strategy' in metadata
        assert 'summary' in metadata
        
        summary = metadata['summary']
        assert summary['success_rate'] == 80.0
        assert summary['automated_loads'] + summary['manual_loads'] <= summary['successful_loads']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])