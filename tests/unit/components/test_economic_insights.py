"""Unit tests for Economic Insights component."""

from unittest.mock import Mock, call, patch

import numpy as np
import pandas as pd
import pytest

from components.economic_insights import EconomicInsights
from tests.utils.test_helpers import MockSessionState, StreamlitTestHelper


class TestEconomicInsights:
    """Test suite for Economic Insights functionality."""

    @pytest.fixture
    def insights(self):
        """Create EconomicInsights instance."""
        return EconomicInsights()

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return {
            "current_value": 1000000,
            "growth_rate": 0.15,
            "time_horizon": 5,
            "adoption_rate": 87.3,
            "industry_average": 72.5,
        }

    def test_display_executive_summary(self):
        """Test executive summary display."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Display summary
            EconomicInsights.display_executive_summary(
                title="Q4 2024 AI Performance",
                key_points=[
                    "87% adoption rate achieved",
                    "185% ROI projected",
                    "18-month payback period",
                ],
                recommendations=["Increase AI investment by 25%", "Focus on high-ROI use cases"],
                urgency="high",
            )

            # Verify display elements
            assert mocks["markdown"].called
            markdown_content = StreamlitTestHelper.get_markdown_content(mocks["markdown"])

            # Check title displayed
            assert any("Q4 2024 AI Performance" in content for content in markdown_content)

            # Check urgency indicator
            assert any("high" in content.lower() for content in markdown_content)

    def test_calculate_cost_of_inaction(self):
        """Test cost of inaction calculation."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Calculate cost
            result = EconomicInsights.calculate_cost_of_inaction(
                current_position=75, industry_average=85, market_size=10000000, years=3
            )

            # Verify calculation
            assert isinstance(result, dict)
            assert "total_cost" in result
            assert "yearly_cost" in result
            assert "opportunity_loss" in result
            assert "competitive_disadvantage" in result

            # Verify display
            assert mocks["metric"].called

            # Check metrics displayed
            metric_calls = mocks["metric"].call_args_list
            assert len(metric_calls) >= 3

    def test_create_competitive_matrix(self):
        """Test competitive position matrix creation."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create test data
            companies_data = pd.DataFrame(
                {
                    "company": ["Your Company", "Leader A", "Leader B", "Peer 1"],
                    "ai_maturity": [7.5, 9.0, 8.5, 7.0],
                    "market_share": [15, 25, 20, 12],
                    "growth_rate": [18, 22, 20, 15],
                }
            )

            # Create matrix
            EconomicInsights.create_competitive_matrix(companies_data, your_company="Your Company")

            # Verify chart created
            assert mocks["plotly_chart"].called

            # Get figure from call
            fig = mocks["plotly_chart"].call_args[0][0]
            assert fig is not None

    def test_generate_what_if_scenarios(self):
        """Test what-if scenario generation."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Setup mock session state
            mocks["selectbox"].return_value = "adoption_rate"
            mocks["slider"].return_value = 50

            # Generate scenarios
            scenarios = EconomicInsights.generate_what_if_scenarios(
                base_metrics={"revenue": 1000000, "costs": 600000, "adoption_rate": 30}
            )

            # Verify UI elements created
            assert mocks["selectbox"].called
            assert mocks["slider"].called

            # Verify scenarios generated
            assert mocks["plotly_chart"].called

    def test_create_action_plan(self):
        """Test action plan creation."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create action plan
            EconomicInsights.create_action_plan(
                assessment_results={
                    "maturity_score": 6.5,
                    "gaps": ["Data Quality", "Talent", "Governance"],
                    "opportunities": ["Process Automation", "Customer Analytics"],
                },
                timeline_months=12,
            )

            # Verify components displayed
            assert mocks["markdown"].called
            assert mocks["columns"].called

            # Check timeline displayed
            markdown_content = StreamlitTestHelper.get_markdown_content(mocks["markdown"])
            assert any("timeline" in content.lower() for content in markdown_content)

    def test_roi_projection_chart(self):
        """Test ROI projection visualization."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create projection
            EconomicInsights._create_roi_projection_chart(
                investment=1000000,
                expected_return=1850000,
                timeline_months=18,
                confidence_interval=(1500000, 2200000),
            )

            # Verify chart created
            assert mocks["plotly_chart"].called

            # Verify chart has confidence interval
            fig = mocks["plotly_chart"].call_args[0][0]
            assert len(fig.data) >= 2  # Main line + confidence band

    def test_benchmark_comparison(self):
        """Test benchmark comparison functionality."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create benchmark
            EconomicInsights._display_benchmark_comparison(
                your_metrics={"adoption": 75, "roi": 165, "productivity": 22},
                industry_benchmarks={"adoption": 85, "roi": 150, "productivity": 25},
                leader_benchmarks={"adoption": 92, "roi": 210, "productivity": 35},
            )

            # Verify comparison displayed
            assert mocks["columns"].called
            assert mocks["metric"].called

            # Check multiple metrics displayed
            metric_calls = mocks["metric"].call_args_list
            assert len(metric_calls) >= 3

    def test_calculate_economic_impact(self):
        """Test economic impact calculation."""
        impact = EconomicInsights._calculate_economic_impact(
            current_productivity=100,
            ai_productivity_gain=0.25,
            workforce_size=1000,
            average_output_per_worker=100000,
        )

        # Verify calculation
        assert isinstance(impact, dict)
        assert "total_impact" in impact
        assert "per_worker_gain" in impact
        assert "roi_percentage" in impact

        # Verify values
        assert impact["total_impact"] == 25000000  # 25% of 100M
        assert impact["per_worker_gain"] == 25000

    def test_urgency_indicator(self):
        """Test urgency indicator display."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Test different urgency levels
            urgency_levels = ["low", "medium", "high", "critical"]

            for urgency in urgency_levels:
                EconomicInsights._display_urgency_indicator(urgency=urgency, reason="Test reason")

            # Verify all levels displayed
            assert mocks["markdown"].call_count >= 4

            # Check color coding
            markdown_content = StreamlitTestHelper.get_markdown_content(mocks["markdown"])
            assert any("color" in content for content in markdown_content)

    def test_opportunity_cost_timeline(self):
        """Test opportunity cost timeline visualization."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create timeline
            EconomicInsights._create_opportunity_cost_timeline(
                monthly_opportunity_loss=50000, months=24
            )

            # Verify chart created
            assert mocks["plotly_chart"].called

            # Verify cumulative calculation
            fig = mocks["plotly_chart"].call_args[0][0]
            assert fig.data[0].y[-1] == 1200000  # 50k * 24 months

    def test_investment_optimizer(self):
        """Test investment optimization calculator."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Setup inputs
            mocks["slider"].side_effect = [1000000, 6, 0.8]  # budget, timeline, risk

            # Run optimizer
            EconomicInsights.investment_optimizer(
                available_projects=[
                    {"name": "Project A", "cost": 200000, "roi": 2.5},
                    {"name": "Project B", "cost": 300000, "roi": 2.0},
                    {"name": "Project C", "cost": 500000, "roi": 3.0},
                ]
            )

            # Verify optimization results displayed
            assert mocks["dataframe"].called
            assert mocks["metric"].called

    def test_peer_comparison_radar(self):
        """Test peer comparison radar chart."""
        with StreamlitTestHelper.mock_streamlit() as mocks:
            # Create comparison
            EconomicInsights._create_peer_comparison_radar(
                your_scores={
                    "Technology": 7.5,
                    "Talent": 6.8,
                    "Process": 7.2,
                    "Data": 6.5,
                    "Governance": 5.9,
                },
                peer_average={
                    "Technology": 6.8,
                    "Talent": 6.2,
                    "Process": 6.5,
                    "Data": 6.0,
                    "Governance": 6.1,
                },
                leader_average={
                    "Technology": 8.5,
                    "Talent": 8.2,
                    "Process": 8.8,
                    "Data": 8.3,
                    "Governance": 8.0,
                },
            )

            # Verify radar chart created
            assert mocks["plotly_chart"].called

            # Check multiple traces
            fig = mocks["plotly_chart"].call_args[0][0]
            assert len(fig.data) >= 3  # Your company, peers, leaders
