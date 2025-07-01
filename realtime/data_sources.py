"""
Specific data source integrations for AI metrics, financial data, policy data, and research metrics
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import re

from .models import DataSourceConfig, DataSourceType, AuthenticationType, DataValidationRule
from .core import RealtimeDataManager

logger = logging.getLogger(__name__)

class AIMetricsDataSource:
    """Data source for AI industry metrics and trends"""
    
    @staticmethod
    def create_ai_research_config() -> DataSourceConfig:
        """Create configuration for AI research metrics"""
        return DataSourceConfig(
            source_id="ai_research_metrics",
            name="AI Research Metrics",
            description="Academic AI research publication and citation metrics",
            source_type=DataSourceType.REST_API,
            base_url="https://api.semanticscholar.org",
            endpoint="/graph/v1/paper/search",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "custom_headers": {
                    "User-Agent": "AI-Dashboard/1.0 (research metrics collector)"
                }
            },
            data_mapping={
                "total_papers": "total",
                "papers": "data",
                "ai_papers_count": "data.length",
                "recent_papers": "data"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="total",
                    rule_type="required",
                    error_message="Total count is required"
                ),
                DataValidationRule(
                    field_name="total",
                    rule_type="type",
                    rule_config={"type": "int"},
                    error_message="Total must be an integer"
                )
            ],
            update_interval=timedelta(hours=6),
            cache_duration=timedelta(hours=12)
        )
    
    @staticmethod
    def create_ai_funding_config() -> DataSourceConfig:
        """Create configuration for AI funding data"""
        return DataSourceConfig(
            source_id="ai_funding_data",
            name="AI Funding Metrics",
            description="Venture capital and investment data for AI companies",
            source_type=DataSourceType.REST_API,
            base_url="https://api.crunchbase.com",
            endpoint="/v4/searches/organizations",
            method="POST",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "api_key": "${CRUNCHBASE_API_KEY}"
            },
            data_mapping={
                "total_funding": "funding_total.value_usd",
                "funding_rounds": "funding_total.count",
                "recent_rounds": "funding_rounds"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="funding_total",
                    rule_type="required",
                    error_message="Funding total is required"
                )
            ],
            update_interval=timedelta(hours=12),
            cache_duration=timedelta(days=1)
        )
    
    @staticmethod
    def create_ai_patents_config() -> DataSourceConfig:
        """Create configuration for AI patent data"""
        return DataSourceConfig(
            source_id="ai_patents_data",
            name="AI Patents Metrics",
            description="AI-related patent filings and grants",
            source_type=DataSourceType.REST_API,
            base_url="https://api.patentsview.org",
            endpoint="/patents/query",
            method="GET",
            data_mapping={
                "total_patents": "total_patent_count",
                "patent_list": "patents",
                "recent_patents": "patents"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="total_patent_count",
                    rule_type="type",
                    rule_config={"type": "int"}
                )
            ],
            update_interval=timedelta(days=1),
            cache_duration=timedelta(days=7)
        )

class FinancialDataSource:
    """Data source for financial market data and ROI calculations"""
    
    @staticmethod
    def create_market_data_config() -> DataSourceConfig:
        """Create configuration for market data"""
        return DataSourceConfig(
            source_id="financial_market_data",
            name="Financial Market Data",
            description="Stock market and financial indicators for AI companies",
            source_type=DataSourceType.REST_API,
            base_url="https://api.polygon.io",
            endpoint="/v2/aggs/grouped/locale/us/market/stocks",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "api_key": "${POLYGON_API_KEY}"
            },
            data_mapping={
                "market_cap": "results.marketcap",
                "volume": "results.volume",
                "price": "results.close",
                "change_percent": "results.change_percent"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="results",
                    rule_type="required"
                )
            ],
            update_interval=timedelta(hours=1),
            cache_duration=timedelta(hours=4)
        )
    
    @staticmethod
    def create_economic_indicators_config() -> DataSourceConfig:
        """Create configuration for economic indicators"""
        return DataSourceConfig(
            source_id="economic_indicators",
            name="Economic Indicators",
            description="Economic indicators relevant to AI adoption",
            source_type=DataSourceType.REST_API,
            base_url="https://api.stlouisfed.org",
            endpoint="/fred/series/observations",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "api_key": "${FRED_API_KEY}"
            },
            data_mapping={
                "gdp_growth": "observations.value",
                "unemployment_rate": "observations.value",
                "tech_spending": "observations.value"
            },
            update_interval=timedelta(days=1),
            cache_duration=timedelta(days=7)
        )

class PolicyDataSource:
    """Data source for government policy and funding data"""
    
    @staticmethod
    def create_government_funding_config() -> DataSourceConfig:
        """Create configuration for government AI funding"""
        return DataSourceConfig(
            source_id="government_ai_funding",
            name="Government AI Funding",
            description="Government AI research and development funding",
            source_type=DataSourceType.REST_API,
            base_url="https://api.usaspending.gov",
            endpoint="/api/v2/search/spending_by_award",
            method="POST",
            data_mapping={
                "total_funding": "results.total_funding",
                "award_count": "results.award_count",
                "agencies": "results.agencies"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="results",
                    rule_type="required"
                )
            ],
            update_interval=timedelta(days=7),
            cache_duration=timedelta(days=30)
        )
    
    @staticmethod
    def create_policy_tracker_config() -> DataSourceConfig:
        """Create configuration for AI policy tracking"""
        return DataSourceConfig(
            source_id="ai_policy_tracker",
            name="AI Policy Tracker",
            description="Tracking of AI-related policies and regulations",
            source_type=DataSourceType.REST_API,
            base_url="https://api.congress.gov",
            endpoint="/v3/bill",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "api_key": "${CONGRESS_API_KEY}"
            },
            data_mapping={
                "bills_count": "count",
                "bills": "bills",
                "recent_bills": "bills"
            },
            update_interval=timedelta(days=1),
            cache_duration=timedelta(days=7)
        )

class ResearchDataSource:
    """Data source for research publication metrics"""
    
    @staticmethod
    def create_arxiv_config() -> DataSourceConfig:
        """Create configuration for arXiv research papers"""
        return DataSourceConfig(
            source_id="arxiv_ai_papers",
            name="arXiv AI Papers",
            description="AI research papers from arXiv",
            source_type=DataSourceType.REST_API,
            base_url="http://export.arxiv.org",
            endpoint="/api/query",
            method="GET",
            data_mapping={
                "total_results": "feed.opensearch:totalResults",
                "entries": "feed.entry",
                "papers": "feed.entry"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="feed",
                    rule_type="required"
                )
            ],
            update_interval=timedelta(hours=6),
            cache_duration=timedelta(hours=24)
        )
    
    @staticmethod
    def create_google_scholar_config() -> DataSourceConfig:
        """Create configuration for Google Scholar metrics"""
        return DataSourceConfig(
            source_id="google_scholar_metrics",
            name="Google Scholar AI Metrics",
            description="Citation and publication metrics from Google Scholar",
            source_type=DataSourceType.REST_API,
            base_url="https://serpapi.com",
            endpoint="/search",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "api_key": "${SERPAPI_KEY}"
            },
            data_mapping={
                "search_results": "organic_results",
                "total_results": "search_information.total_results",
                "papers": "organic_results"
            },
            update_interval=timedelta(hours=12),
            cache_duration=timedelta(days=1)
        )

class GeographicDataSource:
    """Data source for geographic and demographic data"""
    
    @staticmethod
    def create_census_data_config() -> DataSourceConfig:
        """Create configuration for census demographic data"""
        return DataSourceConfig(
            source_id="census_demographics",
            name="Census Demographics",
            description="Demographic data relevant to AI adoption",
            source_type=DataSourceType.REST_API,
            base_url="https://api.census.gov",
            endpoint="/data/2021/acs/acs1",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.API_KEY,
                "api_key": "${CENSUS_API_KEY}"
            },
            data_mapping={
                "population": "population",
                "education_level": "education",
                "tech_workers": "tech_employment"
            },
            update_interval=timedelta(days=30),
            cache_duration=timedelta(days=90)
        )
    
    @staticmethod
    def create_world_bank_config() -> DataSourceConfig:
        """Create configuration for World Bank data"""
        return DataSourceConfig(
            source_id="world_bank_indicators",
            name="World Bank Indicators",
            description="Global economic and development indicators",
            source_type=DataSourceType.REST_API,
            base_url="https://api.worldbank.org",
            endpoint="/v2/country/all/indicator",
            method="GET",
            data_mapping={
                "countries": "country",
                "indicators": "indicator",
                "values": "value"
            },
            update_interval=timedelta(days=7),
            cache_duration=timedelta(days=30)
        )

class TechnologyDataSource:
    """Data source for technology adoption statistics"""
    
    @staticmethod
    def create_github_trends_config() -> DataSourceConfig:
        """Create configuration for GitHub AI project trends"""
        return DataSourceConfig(
            source_id="github_ai_trends",
            name="GitHub AI Trends",
            description="AI project trends and repository statistics from GitHub",
            source_type=DataSourceType.REST_API,
            base_url="https://api.github.com",
            endpoint="/search/repositories",
            method="GET",
            credentials={
                "auth_type": AuthenticationType.BEARER_TOKEN,
                "bearer_token": "${GITHUB_TOKEN}"
            },
            data_mapping={
                "total_repos": "total_count",
                "repositories": "items",
                "trending_repos": "items"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="total_count",
                    rule_type="type",
                    rule_config={"type": "int"}
                )
            ],
            update_interval=timedelta(hours=6),
            cache_duration=timedelta(hours=12)
        )
    
    @staticmethod
    def create_stack_overflow_config() -> DataSourceConfig:
        """Create configuration for Stack Overflow AI trends"""
        return DataSourceConfig(
            source_id="stackoverflow_ai_trends",
            name="Stack Overflow AI Trends",
            description="AI-related questions and activity trends on Stack Overflow",
            source_type=DataSourceType.REST_API,
            base_url="https://api.stackexchange.com",
            endpoint="/2.3/questions",
            method="GET",
            data_mapping={
                "total_questions": "total",
                "questions": "items",
                "trending_tags": "items.tags"
            },
            validation_rules=[
                DataValidationRule(
                    field_name="items",
                    rule_type="required"
                )
            ],
            update_interval=timedelta(hours=12),
            cache_duration=timedelta(days=1)
        )

class DataSourceIntegrator:
    """Integrates all data sources with the real-time data manager"""
    
    def __init__(self, data_manager: RealtimeDataManager):
        self.data_manager = data_manager
        self.source_configs = {}
        self._initialize_sources()
    
    def _initialize_sources(self):
        """Initialize all data source configurations"""
        # AI Metrics
        self.source_configs.update({
            "ai_research_metrics": AIMetricsDataSource.create_ai_research_config(),
            "ai_funding_data": AIMetricsDataSource.create_ai_funding_config(),
            "ai_patents_data": AIMetricsDataSource.create_ai_patents_config(),
        })
        
        # Financial Data
        self.source_configs.update({
            "financial_market_data": FinancialDataSource.create_market_data_config(),
            "economic_indicators": FinancialDataSource.create_economic_indicators_config(),
        })
        
        # Policy Data
        self.source_configs.update({
            "government_ai_funding": PolicyDataSource.create_government_funding_config(),
            "ai_policy_tracker": PolicyDataSource.create_policy_tracker_config(),
        })
        
        # Research Data
        self.source_configs.update({
            "arxiv_ai_papers": ResearchDataSource.create_arxiv_config(),
            "google_scholar_metrics": ResearchDataSource.create_google_scholar_config(),
        })
        
        # Geographic Data
        self.source_configs.update({
            "census_demographics": GeographicDataSource.create_census_data_config(),
            "world_bank_indicators": GeographicDataSource.create_world_bank_config(),
        })
        
        # Technology Data
        self.source_configs.update({
            "github_ai_trends": TechnologyDataSource.create_github_trends_config(),
            "stackoverflow_ai_trends": TechnologyDataSource.create_stack_overflow_config(),
        })
    
    async def setup_all_sources(self, enabled_sources: Optional[List[str]] = None):
        """Setup all data sources in the data manager"""
        if enabled_sources is None:
            enabled_sources = list(self.source_configs.keys())
        
        for source_id in enabled_sources:
            if source_id in self.source_configs:
                config = self.source_configs[source_id]
                try:
                    await self.data_manager.add_data_source(config, auto_start=True)
                    logger.info(f"Successfully setup data source: {source_id}")
                except Exception as e:
                    logger.error(f"Failed to setup data source {source_id}: {e}")
    
    async def setup_demo_sources(self):
        """Setup a subset of data sources for demo purposes"""
        demo_sources = [
            "ai_research_metrics",
            "github_ai_trends",
            "arxiv_ai_papers"
        ]
        await self.setup_all_sources(demo_sources)
    
    def get_source_config(self, source_id: str) -> Optional[DataSourceConfig]:
        """Get configuration for a specific source"""
        return self.source_configs.get(source_id)
    
    def list_available_sources(self) -> Dict[str, Dict[str, str]]:
        """List all available data sources with descriptions"""
        return {
            source_id: {
                "name": config.name,
                "description": config.description,
                "type": config.source_type.value,
                "update_interval": str(config.update_interval)
            }
            for source_id, config in self.source_configs.items()
        }
    
    async def validate_source_credentials(self, source_id: str) -> bool:
        """Validate that a data source has proper credentials configured"""
        config = self.source_configs.get(source_id)
        if not config:
            return False
        
        creds = config.credentials
        
        if creds.auth_type == AuthenticationType.API_KEY:
            return bool(creds.api_key and creds.api_key != "${API_KEY}")
        elif creds.auth_type == AuthenticationType.BEARER_TOKEN:
            return bool(creds.bearer_token and creds.bearer_token != "${TOKEN}")
        elif creds.auth_type == AuthenticationType.BASIC_AUTH:
            return bool(creds.username and creds.password)
        else:
            return True  # No auth required
    
    async def test_source_connection(self, source_id: str) -> Dict[str, Any]:
        """Test connection to a data source"""
        try:
            stream = await self.data_manager.get_stream(source_id)
            if not stream:
                return {"success": False, "error": "Source not found or not started"}
            
            # Get the API client and test connection
            client = stream._client
            if not client:
                return {"success": False, "error": "No API client available"}
            
            health_check_result = await client.health_check()
            
            return {
                "success": health_check_result,
                "source_id": source_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "source_id": source_id,
                "timestamp": datetime.utcnow().isoformat()
            }

# Helper functions for creating custom data sources
def create_custom_rest_api_source(
    source_id: str,
    name: str,
    base_url: str,
    endpoint: str = "/",
    auth_type: AuthenticationType = AuthenticationType.NONE,
    **kwargs
) -> DataSourceConfig:
    """Create a custom REST API data source configuration"""
    return DataSourceConfig(
        source_id=source_id,
        name=name,
        description=f"Custom API integration for {name}",
        source_type=DataSourceType.REST_API,
        base_url=base_url,
        endpoint=endpoint,
        credentials={"auth_type": auth_type},
        **kwargs
    )

# Global integrator instance
_global_integrator: Optional[DataSourceIntegrator] = None

async def get_global_integrator() -> DataSourceIntegrator:
    """Get the global data source integrator instance"""
    global _global_integrator
    if _global_integrator is None:
        from .core import get_global_manager
        data_manager = await get_global_manager()
        _global_integrator = DataSourceIntegrator(data_manager)
    return _global_integrator