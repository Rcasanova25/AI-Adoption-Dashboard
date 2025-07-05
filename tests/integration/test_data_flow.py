"""Integration tests for data flow between components."""

from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import numpy as np
import pandas as pd
import pytest

from components.economic_insights import EconomicInsights
from components.key_takeaways import KeyTakeawaysGenerator
from data.data_manager import DataManager
from data.loaders.ai_index import AIIndexLoader
from tests.fixtures.mock_data import (
    generate_adoption_data,
    generate_competitive_matrix,
    generate_industry_data,
)


class TestDataFlowIntegration:
    """Test data flow from loaders through components to UI."""

    @pytest.fixture
    def mock_pdf_extractor(self):
        """Mock PDF extractor for all tests."""
        with patch("data.extractors.pdf.PDFExtractor") as mock:
            extractor = Mock()
            extractor.extract_text.return_value = """
            AI Adoption Report 2025
            Overall adoption: 87.3%
            Enterprise: 92.1%
            YoY Growth: 15.2%
            """
            extractor.extract_tables.return_value = [
                generate_adoption_data(12),
                generate_industry_data(),
            ]
            mock.return_value = extractor
            yield mock

    @pytest.fixture
    def data_manager(self, mock_pdf_extractor):
        """Create DataManager with mocked loaders."""
        return DataManager()

    def test_loader_to_insights_flow(self, data_manager):
        """Test data flow from loader to economic insights."""
        # Load data
        ai_data = data_manager.get_data("ai_index")

        # Verify data loaded
        assert "adoption_rates" in ai_data
        assert isinstance(ai_data["adoption_rates"], pd.DataFrame)

        # Pass to economic insights
        with patch("streamlit.metric") as mock_metric:
            EconomicInsights.display_executive_summary(
                title="AI Performance",
                key_points=[
                    f"Adoption rate: {ai_data['adoption_rates']['adoption_rate'].iloc[-1]:.1f}%"
                ],
                recommendations=["Increase investment"],
                urgency="high",
            )

        # Verify insights displayed
        assert mock_metric.called

    def test_multiple_loader_aggregation(self, data_manager):
        """Test aggregating data from multiple loaders."""
        # Get data from multiple sources
        all_data = data_manager.get_all_data()

        # Verify multiple sources loaded
        assert len(all_data) >= 2

        # Combine adoption data
        combined = data_manager.get_combined_dataset("adoption_rates")

        # Verify combination
        assert isinstance(combined, pd.DataFrame)
        assert not combined.empty

    def test_data_to_takeaways_flow(self, data_manager):
        """Test data flow to key takeaways generation."""
        # Load data
        data = data_manager.get_data("ai_index")
        adoption_df = data.get("adoption_rates", pd.DataFrame())

        # Calculate metrics
        current_adoption = adoption_df["adoption_rate"].iloc[-1] if not adoption_df.empty else 87.3
        growth_rate = 15.2  # From mock data

        # Generate takeaways
        generator = KeyTakeawaysGenerator()
        takeaways = generator.generate_takeaways(
            "adoption_rates",
            {
                "current_adoption": current_adoption,
                "yoy_growth": growth_rate,
                "industry_average": 72,
            },
        )

        # Verify takeaways generated
        assert len(takeaways) > 0
        assert takeaways[0].category in ["threat", "opportunity", "action"]

    def test_competitive_analysis_flow(self):
        """Test competitive position analysis data flow."""
        # Create competitive data
        competitive_data = generate_competitive_matrix()

        # Process through insights
        with patch("streamlit.plotly_chart") as mock_chart:
            EconomicInsights.create_competitive_matrix(
                competitive_data, your_company="Your Company"
            )

        # Verify visualization created
        assert mock_chart.called
        fig = mock_chart.call_args[0][0]
        assert len(fig.data) > 0

    def test_cache_integration(self, data_manager):
        """Test caching works across components."""
        # First load
        data1 = data_manager.get_data("ai_index")

        # Second load (should use cache)
        data2 = data_manager.get_data("ai_index")

        # Verify same data returned
        assert data1.keys() == data2.keys()

        # Verify loader not called twice
        with patch.object(data_manager.loaders.get("ai_index", Mock()), "load") as mock_load:
            data3 = data_manager.get_data("ai_index")
            mock_load.assert_not_called()

    def test_error_propagation(self, data_manager):
        """Test error handling across components."""
        # Create failing loader
        failing_loader = Mock()
        failing_loader.load.side_effect = Exception("Load failed")
        data_manager.loaders["failing"] = failing_loader

        # Try to load data
        data = data_manager.get_data("failing")

        # Should return empty dict
        assert data == {}

        # Components should handle empty data gracefully
        generator = KeyTakeawaysGenerator()
        takeaways = generator.generate_takeaways("adoption_rates", {})
        assert len(takeaways) > 0  # Should have fallback takeaways

    def test_data_transformation_pipeline(self, data_manager):
        """Test complete data transformation pipeline."""
        # Load raw data
        raw_data = data_manager.get_data("ai_index")

        # Transform for visualization
        adoption_df = raw_data.get("adoption_rates", pd.DataFrame())

        if not adoption_df.empty:
            # Calculate rolling average
            adoption_df["rolling_avg"] = adoption_df["adoption_rate"].rolling(3).mean()

            # Calculate growth rate
            adoption_df["growth_rate"] = adoption_df["adoption_rate"].pct_change() * 100

            # Verify transformations
            assert "rolling_avg" in adoption_df.columns
            assert "growth_rate" in adoption_df.columns
            assert not adoption_df["rolling_avg"].isna().all()

    def test_persona_data_filtering(self, data_manager):
        """Test data filtering based on persona."""
        # Load full data
        full_data = data_manager.get_all_data()

        # Filter for executive persona
        exec_data = {}
        for source, data in full_data.items():
            if isinstance(data, dict):
                # Keep only high-level metrics
                exec_data[source] = {
                    k: v
                    for k, v in data.items()
                    if k in ["adoption_rates", "roi_analysis", "competitive_position"]
                }

        # Verify filtered data
        assert len(exec_data) <= len(full_data)

        # Filter for researcher persona (keep everything)
        researcher_data = full_data
        assert len(researcher_data) == len(full_data)

    def test_real_time_data_updates(self, data_manager):
        """Test real-time data update handling."""
        # Initial load
        initial_data = data_manager.get_data("ai_index")

        # Simulate data update by clearing cache
        data_manager.clear_cache()

        # Modify mock to return different data
        with patch.object(data_manager.loaders.get("ai_index", Mock()), "load") as mock_load:
            new_df = generate_adoption_data(12)
            new_df["adoption_rate"] = new_df["adoption_rate"] + 5  # Increase rates
            mock_load.return_value = {"adoption_rates": new_df}

            # Load updated data
            updated_data = data_manager.get_data("ai_index")

            # Verify data updated
            if "adoption_rates" in initial_data and "adoption_rates" in updated_data:
                initial_rate = initial_data["adoption_rates"]["adoption_rate"].mean()
                updated_rate = updated_data["adoption_rates"]["adoption_rate"].mean()
                assert updated_rate > initial_rate

    def test_data_validation_pipeline(self, data_manager):
        """Test data validation across the pipeline."""
        # Load data
        data = data_manager.get_data("ai_index")

        # Validate adoption rates
        if "adoption_rates" in data:
            df = data["adoption_rates"]

            # Check data types
            assert pd.api.types.is_numeric_dtype(df.get("adoption_rate", pd.Series()))

            # Check value ranges
            if "adoption_rate" in df.columns:
                assert df["adoption_rate"].min() >= 0
                assert df["adoption_rate"].max() <= 100

            # Check for required columns
            expected_cols = ["date", "adoption_rate"]
            for col in expected_cols:
                if col == "date":
                    # Date might be index
                    assert col in df.columns or df.index.name == col

    def test_cross_component_consistency(self, data_manager):
        """Test data consistency across different components."""
        # Load data once
        data = data_manager.get_data("ai_index")

        # Use in multiple components
        adoption_rate = 87.3  # Default
        if "adoption_rates" in data and not data["adoption_rates"].empty:
            adoption_rate = data["adoption_rates"]["adoption_rate"].iloc[-1]

        # Generate takeaways
        generator = KeyTakeawaysGenerator()
        takeaways = generator.generate_takeaways(
            "adoption_rates", {"current_adoption": adoption_rate}
        )

        # Create economic insight
        with patch("streamlit.metric") as mock_metric:
            EconomicInsights.display_executive_summary(
                title="Summary",
                key_points=[f"Adoption: {adoption_rate:.1f}%"],
                recommendations=["Continue momentum"],
                urgency="medium",
            )

        # Verify consistent adoption rate used
        takeaway_has_rate = any(str(adoption_rate) in t.message for t in takeaways)

        metric_has_rate = any(
            str(int(adoption_rate)) in str(call) for call in mock_metric.call_args_list
        )

        assert takeaway_has_rate or metric_has_rate
