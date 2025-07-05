"""Unit tests for AI Index Loader."""

from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pandas as pd
import pytest

from data.loaders.ai_index import AIIndexLoader
from tests.fixtures.mock_data import generate_adoption_data, generate_mock_pdf_data


class TestAIIndexLoader:
    """Test suite for AI Index data loader."""

    @pytest.fixture
    def data_source(self):
        """Create test data source."""
        return DataSource(
            name="AI Index Report 2025",
            type="pdf",
            path="/test/ai_index_2025.pdf",
            year=2025,
            credibility_score=0.95,
        )

    @pytest.fixture
    def loader(self, data_source):
        """Create loader instance."""
        return AIIndexLoader(data_source)

    @pytest.fixture
    def mock_pdf_data(self):
        """Get mock PDF data."""
        return generate_mock_pdf_data("ai_index")

    def test_initialization(self, loader, data_source):
        """Test loader initialization."""
        assert loader.source == data_source
        assert isinstance(loader._cache, dict)
        assert len(loader._cache) == 0

    @patch("data.loaders.ai_index.PDFExtractor")
    def test_load_success(self, mock_extractor_class, loader, mock_pdf_data):
        """Test successful data loading."""
        # Setup mock
        mock_extractor = Mock()
        mock_extractor.extract_text.return_value = """
        AI Adoption Rates 2025
        Overall: 87.3%
        Enterprise: 92.1%
        SME: 78.5%
        Growth YoY: 15.2%
        """
        mock_extractor.extract_tables.return_value = [mock_pdf_data["metrics"]]
        mock_extractor_class.return_value = mock_extractor

        # Load data
        result = loader.load()

        # Verify structure
        assert isinstance(result, dict)
        assert "adoption_rates" in result
        assert "industry_analysis" in result
        assert "geographic_distribution" in result

        # Verify data
        adoption_df = result["adoption_rates"]
        assert isinstance(adoption_df, pd.DataFrame)
        assert not adoption_df.empty

    def test_parse_adoption_rates(self, loader):
        """Test adoption rate parsing logic."""
        test_text = """
        Global AI Adoption Statistics:
        - Overall adoption: 87.3%
        - Enterprise adoption: 92.1%
        - SME adoption: 78.5%
        - Year-over-year growth: 15.2%
        
        By Function:
        - Marketing: 89.5%
        - Sales: 85.2%
        - Operations: 78.9%
        """

        # Parse rates
        result = loader._parse_adoption_rates(test_text, [])

        # Verify DataFrame
        assert isinstance(result, pd.DataFrame)
        assert "metric" in result.columns
        assert "value" in result.columns
        assert len(result) > 0

        # Verify specific values
        overall_row = result[result["metric"] == "Overall Adoption"]
        assert not overall_row.empty
        assert overall_row["value"].iloc[0] == 87.3

    def test_parse_industry_data(self, loader):
        """Test industry data parsing."""
        test_tables = [
            pd.DataFrame(
                {
                    "Industry": ["Technology", "Finance", "Healthcare"],
                    "Adoption Rate": [92.1, 88.5, 75.3],
                    "Growth": [18.5, 15.2, 22.1],
                }
            )
        ]

        # Parse industry data
        result = loader._parse_industry_analysis("", test_tables)

        # Verify DataFrame
        assert isinstance(result, pd.DataFrame)
        assert "industry" in result.columns
        assert "adoption_rate" in result.columns
        assert len(result) == 3

        # Verify sorting (should be by adoption rate)
        assert result.iloc[0]["industry"] == "Technology"

    def test_parse_geographic_data(self, loader):
        """Test geographic data parsing."""
        test_tables = [
            pd.DataFrame(
                {
                    "Region": ["North America", "Europe", "Asia Pacific"],
                    "Country": ["USA", "Germany", "China"],
                    "Adoption": [87.5, 78.9, 89.2],
                }
            )
        ]

        # Parse geographic data
        result = loader._parse_geographic_distribution("", test_tables)

        # Verify DataFrame
        assert isinstance(result, pd.DataFrame)
        assert "region" in result.columns
        assert "country" in result.columns
        assert "adoption_rate" in result.columns

    def test_parse_investment_trends(self, loader):
        """Test investment trend parsing."""
        test_text = """
        AI Investment Trends:
        - Total investment: $189.6 billion
        - YoY growth: 32%
        - Average per company: $2.5 million
        """

        test_tables = [
            pd.DataFrame(
                {
                    "Year": [2021, 2022, 2023, 2024, 2025],
                    "Investment_Billions": [45.2, 68.5, 98.7, 142.3, 189.6],
                }
            )
        ]

        # Parse investment data
        result = loader._parse_investment_trends(test_text, test_tables)

        # Verify DataFrame
        assert isinstance(result, pd.DataFrame)
        assert "year" in result.columns
        assert "investment_billions" in result.columns
        assert len(result) == 5

    def test_cache_functionality(self, loader):
        """Test caching mechanism."""
        # First load
        test_data = pd.DataFrame({"test": [1, 2, 3]})
        loader._cache["test_key"] = test_data

        # Verify cache hit
        assert "test_key" in loader._cache
        cached = loader._cache["test_key"]
        pd.testing.assert_frame_equal(cached, test_data)

    @patch("data.loaders.ai_index.PDFExtractor")
    def test_error_handling(self, mock_extractor_class, loader):
        """Test error handling during load."""
        # Setup failing extractor
        mock_extractor = Mock()
        mock_extractor.extract_text.side_effect = Exception("PDF read error")
        mock_extractor_class.return_value = mock_extractor

        # Load should not raise but return empty data
        result = loader.load()

        # Verify empty result
        assert isinstance(result, dict)
        assert len(result) > 0  # Should have keys
        for key, value in result.items():
            assert isinstance(value, pd.DataFrame)
            assert value.empty

    def test_data_validation(self, loader):
        """Test data validation after parsing."""
        # Create data with invalid values
        test_df = pd.DataFrame(
            {
                "metric": ["Adoption", "Growth", "Invalid"],
                "value": [87.3, 15.2, -10.5],  # Negative value
            }
        )

        # Loader should handle validation
        validated = loader._validate_dataframe(test_df, "value", min_val=0, max_val=100)

        # Negative values should be filtered or corrected
        assert all(validated["value"] >= 0)

    def test_empty_pdf_handling(self, loader):
        """Test handling of empty PDF data."""
        # Parse empty data
        result = loader._parse_adoption_rates("", [])

        # Should return empty but valid DataFrame
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert "metric" in result.columns
        assert "value" in result.columns

    def test_malformed_data_handling(self, loader):
        """Test handling of malformed data."""
        # Malformed table
        bad_table = pd.DataFrame({"Wrong Column": ["A", "B"], "Another Wrong": [1, 2]})

        # Should handle gracefully
        result = loader._parse_industry_analysis("", [bad_table])

        assert isinstance(result, pd.DataFrame)
        # Should have expected columns even if empty
        assert "industry" in result.columns

    def test_extract_key_metrics(self, loader):
        """Test extraction of key metrics."""
        test_text = """
        Key Findings:
        - 87% of enterprises use AI
        - 25% average productivity gain
        - $13 trillion economic impact by 2030
        - 3x ROI within 18 months
        """

        # Extract metrics
        metrics = loader._extract_key_metrics(test_text)

        assert isinstance(metrics, dict)
        assert "adoption_rate" in metrics
        assert "productivity_gain" in metrics
        assert metrics["adoption_rate"] == 87.0

    def test_integration_with_models(self, loader):
        """Test integration with Pydantic models."""
        # Create test data
        test_data = {
            "overall_adoption_rate": 87.3,
            "enterprise_adoption_rate": 92.1,
            "sme_adoption_rate": 78.5,
            "growth_rate_yoy": 15.2,
            "adoption_by_function": {"Marketing": 89.5, "Sales": 85.2},
            "timestamp": datetime.now(),
        }

        # Should create valid model
        metrics = AdoptionMetrics(**test_data)

        assert metrics.overall_adoption_rate == 87.3
        assert metrics.growth_rate_yoy == 15.2
        assert "Marketing" in metrics.adoption_by_function
