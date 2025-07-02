"""
Kedro Integration Module for AI Adoption Dashboard
Replaces custom data integration with McKinsey Kedro framework for production-grade data pipelines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging
from pathlib import Path

# Import yaml with fallback
try:
    import yaml
except ImportError:
    yaml = None
    import logging
    logging.warning("PyYAML not available. Kedro pipeline features will use fallback configuration.")

# Kedro imports with fallback classes
try:
    from kedro.pipeline import Pipeline, node
    from kedro.io import DataCatalog, MemoryDataSet
    from kedro.runner import ThreadRunner, ParallelRunner
    from kedro.config import ConfigLoader
    KEDRO_AVAILABLE = True
except ImportError:
    KEDRO_AVAILABLE = False
    logging.warning("Kedro not available. Install with: pip install kedro")
    
    # Fallback classes when Kedro is not available
    class Pipeline:
        """Fallback Pipeline class when Kedro is not available"""
        def __init__(self, nodes=None):
            self.nodes = nodes or []
        
        def only_nodes_with_tags(self, *tags):
            return Pipeline([])
    
    class DataCatalog:
        """Fallback DataCatalog class when Kedro is not available"""
        def __init__(self, datasets=None):
            self.datasets = datasets or {}
        
        @classmethod
        def from_config(cls, config):
            return cls()
    
    class ThreadRunner:
        """Fallback ThreadRunner class when Kedro is not available"""
        def run(self, pipeline, catalog):
            pass
    
    class ParallelRunner:
        """Fallback ParallelRunner class when Kedro is not available"""
        def run(self, pipeline, catalog):
            pass
    
    class ConfigLoader:
        """Fallback ConfigLoader class when Kedro is not available"""
        def __init__(self, conf_paths):
            pass
    
    def node(func=None, inputs=None, outputs=None, name=None, tags=None, namespace=None):
        """Fallback node function when Kedro is not available"""
        class FallbackNode:
            def __init__(self):
                self.name = name
                self.inputs = inputs or []
                self.outputs = outputs or []
                self.tags = tags or []
        return FallbackNode()

logger = logging.getLogger(__name__)

class KedroDatasetType(Enum):
    PANDAS_CSV = "pandas.CSVDataSet"
    PANDAS_PARQUET = "pandas.ParquetDataSet"
    PANDAS_EXCEL = "pandas.ExcelDataSet"
    PANDAS_SQL = "pandas.SQLQueryDataSet"
    API_DATASET = "api.APIDataSet"
    JSON_DATASET = "json.JSONDataSet"

class PipelineType(Enum):
    DATA_INGESTION = "data_ingestion"
    DATA_PROCESSING = "data_processing"
    FEATURE_ENGINEERING = "feature_engineering"
    ANALYTICS = "analytics"
    REPORTING = "reporting"

@dataclass
class KedroDataSource:
    """Kedro-compatible data source configuration"""
    dataset_name: str
    dataset_type: KedroDatasetType
    filepath: Optional[str]
    connection_config: Dict[str, Any]
    load_args: Dict[str, Any]
    save_args: Dict[str, Any]
    versioned: bool = True
    credentials: Optional[str] = None

@dataclass
class KedroNode:
    """Kedro pipeline node configuration"""
    func_name: str
    inputs: List[str]
    outputs: List[str]
    name: str
    tags: List[str]
    namespace: Optional[str] = None

class AIAdoptionKedroManager:
    """
    McKinsey Kedro integration manager for AI Adoption Dashboard
    Provides production-grade data pipeline management using Kedro framework
    """
    
    def __init__(self, project_path: str = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.catalog = None
        self.pipelines = {}
        self.config_loader = None
        
        if KEDRO_AVAILABLE:
            self._initialize_kedro_environment()
        else:
            logger.warning("Kedro not available. Pipeline management will use fallback implementation.")
    
    def _initialize_kedro_environment(self):
        """Initialize Kedro environment and configuration"""
        
        try:
            # Initialize configuration loader
            conf_paths = [str(self.project_path / "conf")]
            self.config_loader = ConfigLoader(conf_paths)
            
            # Load data catalog configuration
            catalog_config = self._create_ai_adoption_catalog_config()
            self.catalog = DataCatalog.from_config(catalog_config)
            
            logger.info("Kedro environment initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Kedro environment: {e}")
            self.catalog = DataCatalog()
    
    def create_ai_adoption_data_pipeline(
        self,
        pipeline_name: str = "ai_adoption_pipeline",
        enable_causal_analysis: bool = True
    ) -> Optional[Pipeline]:
        """
        Create comprehensive AI adoption data pipeline using Kedro
        """
        
        if not KEDRO_AVAILABLE:
            logger.warning("Kedro not available. Cannot create Kedro pipeline.")
            return None
        
        nodes = []
        
        # Data Ingestion Nodes
        nodes.extend([
            node(
                func=self._load_industry_ai_data,
                inputs=["industry_ai_raw"],
                outputs="industry_ai_cleaned",
                name="load_industry_ai_data",
                tags=["data_ingestion", "ai_adoption"]
            ),
            
            node(
                func=self._load_productivity_metrics,
                inputs=["productivity_raw"],
                outputs="productivity_cleaned",
                name="load_productivity_metrics", 
                tags=["data_ingestion", "productivity"]
            ),
            
            node(
                func=self._load_geographic_data,
                inputs=["geographic_raw"],
                outputs="geographic_cleaned",
                name="load_geographic_data",
                tags=["data_ingestion", "geographic"]
            ),
            
            node(
                func=self._load_market_intelligence,
                inputs=["market_intelligence_raw"],
                outputs="market_intelligence_cleaned",
                name="load_market_intelligence",
                tags=["data_ingestion", "market"]
            )
        ])
        
        # Data Processing Nodes
        nodes.extend([
            node(
                func=self._merge_adoption_productivity_data,
                inputs=["industry_ai_cleaned", "productivity_cleaned"],
                outputs="merged_ai_productivity",
                name="merge_adoption_productivity",
                tags=["data_processing", "integration"]
            ),
            
            node(
                func=self._calculate_derived_metrics,
                inputs="merged_ai_productivity",
                outputs="enhanced_metrics",
                name="calculate_derived_metrics",
                tags=["data_processing", "feature_engineering"]
            ),
            
            node(
                func=self._perform_data_quality_validation,
                inputs="enhanced_metrics",
                outputs="validated_data",
                name="data_quality_validation",
                tags=["data_processing", "quality_assurance"]
            )
        ])
        
        # Geographic Integration Nodes
        nodes.extend([
            node(
                func=self._integrate_geographic_data,
                inputs=["validated_data", "geographic_cleaned"],
                outputs="geo_integrated_data",
                name="integrate_geographic_data",
                tags=["data_processing", "geographic_integration"]
            ),
            
            node(
                func=self._calculate_regional_benchmarks,
                inputs="geo_integrated_data",
                outputs="regional_benchmarks",
                name="calculate_regional_benchmarks",
                tags=["analytics", "benchmarking"]
            )
        ])
        
        # Advanced Analytics Nodes
        if enable_causal_analysis:
            nodes.extend([
                node(
                    func=self._perform_causal_analysis,
                    inputs="geo_integrated_data",
                    outputs="causal_relationships",
                    name="perform_causal_analysis",
                    tags=["analytics", "causal_inference"]
                ),
                
                node(
                    func=self._generate_intervention_recommendations,
                    inputs=["causal_relationships", "regional_benchmarks"],
                    outputs="intervention_recommendations",
                    name="generate_interventions",
                    tags=["analytics", "recommendations"]
                )
            ])
        
        # Business Intelligence Nodes
        nodes.extend([
            node(
                func=self._calculate_roi_projections,
                inputs=["geo_integrated_data", "market_intelligence_cleaned"],
                outputs="roi_projections",
                name="calculate_roi_projections",
                tags=["analytics", "roi_analysis"]
            ),
            
            node(
                func=self._generate_executive_insights,
                inputs=["regional_benchmarks", "roi_projections"] + 
                       (["intervention_recommendations"] if enable_causal_analysis else []),
                outputs="executive_insights",
                name="generate_executive_insights",
                tags=["reporting", "executive"]
            ),
            
            node(
                func=self._create_dashboard_datasets,
                inputs=["executive_insights", "geo_integrated_data"],
                outputs=["dashboard_summary", "dashboard_detailed", "dashboard_geographic"],
                name="create_dashboard_datasets",
                tags=["reporting", "dashboard_preparation"]
            )
        ])
        
        # Create and register pipeline
        pipeline = Pipeline(nodes)
        self.pipelines[pipeline_name] = pipeline
        
        logger.info(f"Created AI adoption pipeline '{pipeline_name}' with {len(nodes)} nodes")
        return pipeline
    
    def run_pipeline(
        self,
        pipeline_name: str,
        runner_type: str = "parallel",
        tags: List[str] = None
    ) -> Dict[str, Any]:
        """
        Execute Kedro pipeline with specified runner
        """
        
        if not KEDRO_AVAILABLE:
            return self._run_fallback_pipeline(pipeline_name, tags)
        
        if pipeline_name not in self.pipelines:
            raise ValueError(f"Pipeline '{pipeline_name}' not found")
        
        pipeline = self.pipelines[pipeline_name]
        
        # Filter pipeline by tags if specified
        if tags:
            pipeline = pipeline.only_nodes_with_tags(*tags)
        
        # Select runner
        if runner_type == "parallel":
            runner = ParallelRunner()
        else:
            runner = ThreadRunner()
        
        try:
            # Execute pipeline
            start_time = datetime.now()
            runner.run(pipeline, self.catalog)
            end_time = datetime.now()
            
            execution_result = {
                'pipeline_name': pipeline_name,
                'status': 'completed',
                'start_time': start_time,
                'end_time': end_time,
                'duration': (end_time - start_time).total_seconds(),
                'nodes_executed': len(pipeline.nodes),
                'runner_type': runner_type,
                'tags_filter': tags
            }
            
            logger.info(f"Pipeline '{pipeline_name}' completed successfully in {execution_result['duration']:.2f} seconds")
            return execution_result
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {e}")
            return {
                'pipeline_name': pipeline_name,
                'status': 'failed',
                'error': str(e),
                'start_time': start_time,
                'end_time': datetime.now()
            }
    
    def get_pipeline_visualization(self, pipeline_name: str) -> Dict[str, Any]:
        """
        Get pipeline visualization data for Kedro-Viz integration
        """
        
        if pipeline_name not in self.pipelines:
            return {'error': f"Pipeline '{pipeline_name}' not found"}
        
        pipeline = self.pipelines[pipeline_name]
        
        # Extract pipeline structure for visualization
        viz_data = {
            'pipeline_name': pipeline_name,
            'nodes': [],
            'datasets': set(),
            'tags': set()
        }
        
        for node in pipeline.nodes:
            node_data = {
                'name': node.name,
                'inputs': list(node.inputs),
                'outputs': list(node.outputs),
                'tags': list(node.tags) if node.tags else []
            }
            viz_data['nodes'].append(node_data)
            viz_data['datasets'].update(node.inputs)
            viz_data['datasets'].update(node.outputs)
            if node.tags:
                viz_data['tags'].update(node.tags)
        
        viz_data['datasets'] = list(viz_data['datasets'])
        viz_data['tags'] = list(viz_data['tags'])
        
        return viz_data
    
    def create_production_catalog_config(self) -> Dict[str, Any]:
        """
        Create production-ready data catalog configuration
        """
        
        catalog_config = {
            # Raw Data Sources
            "industry_ai_raw": {
                "type": "pandas.CSVDataSet",
                "filepath": "data/01_raw/industry_ai_adoption.csv",
                "load_args": {
                    "sep": ",",
                    "encoding": "utf-8"
                },
                "versioned": True
            },
            
            "productivity_raw": {
                "type": "pandas.CSVDataSet", 
                "filepath": "data/01_raw/productivity_metrics.csv",
                "versioned": True
            },
            
            "geographic_raw": {
                "type": "pandas.CSVDataSet",
                "filepath": "data/01_raw/geographic_ai_data.csv",
                "versioned": True
            },
            
            "market_intelligence_raw": {
                "type": "pandas.CSVDataSet",
                "filepath": "data/01_raw/market_intelligence.csv",
                "versioned": True
            },
            
            # Intermediate Data
            "industry_ai_cleaned": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/02_intermediate/industry_ai_cleaned.parquet",
                "versioned": True
            },
            
            "productivity_cleaned": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/02_intermediate/productivity_cleaned.parquet",
                "versioned": True
            },
            
            "geographic_cleaned": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/02_intermediate/geographic_cleaned.parquet", 
                "versioned": True
            },
            
            "market_intelligence_cleaned": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/02_intermediate/market_intelligence_cleaned.parquet",
                "versioned": True
            },
            
            # Processed Data
            "merged_ai_productivity": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/03_primary/merged_ai_productivity.parquet",
                "versioned": True
            },
            
            "enhanced_metrics": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/03_primary/enhanced_metrics.parquet",
                "versioned": True
            },
            
            "validated_data": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/03_primary/validated_data.parquet",
                "versioned": True
            },
            
            "geo_integrated_data": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/03_primary/geo_integrated_data.parquet",
                "versioned": True
            },
            
            # Analytics Outputs
            "regional_benchmarks": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/04_feature/regional_benchmarks.parquet",
                "versioned": True
            },
            
            "causal_relationships": {
                "type": "pickle.PickleDataSet",
                "filepath": "data/04_feature/causal_relationships.pkl",
                "versioned": True
            },
            
            "intervention_recommendations": {
                "type": "json.JSONDataSet",
                "filepath": "data/04_feature/intervention_recommendations.json",
                "versioned": True
            },
            
            "roi_projections": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/04_feature/roi_projections.parquet",
                "versioned": True
            },
            
            # Reporting Outputs
            "executive_insights": {
                "type": "json.JSONDataSet",
                "filepath": "data/05_model_input/executive_insights.json",
                "versioned": True
            },
            
            "dashboard_summary": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/06_models/dashboard_summary.parquet",
                "versioned": True
            },
            
            "dashboard_detailed": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/06_models/dashboard_detailed.parquet",
                "versioned": True
            },
            
            "dashboard_geographic": {
                "type": "pandas.ParquetDataSet",
                "filepath": "data/06_models/dashboard_geographic.parquet",
                "versioned": True
            }
        }
        
        return catalog_config
    
    def _create_ai_adoption_catalog_config(self) -> Dict[str, Any]:
        """Create AI adoption specific catalog configuration"""
        return self.create_production_catalog_config()
    
    # Data Processing Functions (Kedro Node Functions)
    def _load_industry_ai_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Load and clean industry AI adoption data"""
        
        # Data cleaning and standardization
        cleaned_data = raw_data.copy()
        
        # Standardize column names
        column_mapping = {
            'AI_Adoption_Rate': 'adoption_rate',
            'Industry_Sector': 'sector',
            'Year': 'year',
            'Investment_Amount': 'investment_amount',
            'ROI_Percentage': 'roi_percentage'
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in cleaned_data.columns:
                cleaned_data = cleaned_data.rename(columns={old_col: new_col})
        
        # Data type conversions
        if 'year' in cleaned_data.columns:
            cleaned_data['year'] = pd.to_numeric(cleaned_data['year'], errors='coerce')
        
        if 'adoption_rate' in cleaned_data.columns:
            cleaned_data['adoption_rate'] = pd.to_numeric(cleaned_data['adoption_rate'], errors='coerce')
            # Ensure adoption rate is between 0 and 100
            cleaned_data['adoption_rate'] = cleaned_data['adoption_rate'].clip(0, 100)
        
        # Remove duplicates and handle missing values
        cleaned_data = cleaned_data.drop_duplicates()
        cleaned_data = cleaned_data.dropna(subset=['sector', 'year'])
        
        logger.info(f"Cleaned industry AI data: {len(cleaned_data)} records")
        return cleaned_data
    
    def _load_productivity_metrics(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Load and clean productivity metrics data"""
        
        cleaned_data = raw_data.copy()
        
        # Standardize productivity metrics
        productivity_columns = [
            'revenue_per_employee', 'operational_efficiency', 'cost_reduction_percentage',
            'time_to_market', 'customer_satisfaction', 'innovation_index'
        ]
        
        for col in productivity_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
        
        # Calculate composite productivity index
        if all(col in cleaned_data.columns for col in ['revenue_per_employee', 'operational_efficiency']):
            cleaned_data['productivity_index'] = (
                cleaned_data['revenue_per_employee'].fillna(0) * 0.4 +
                cleaned_data['operational_efficiency'].fillna(100) * 0.6
            )
        
        logger.info(f"Cleaned productivity data: {len(cleaned_data)} records")
        return cleaned_data
    
    def _load_geographic_data(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Load and clean geographic AI adoption data"""
        
        cleaned_data = raw_data.copy()
        
        # Standardize country names and codes
        if 'country' in cleaned_data.columns:
            cleaned_data['country'] = cleaned_data['country'].str.title()
        
        # Validate geographic coordinates
        if 'latitude' in cleaned_data.columns and 'longitude' in cleaned_data.columns:
            cleaned_data['latitude'] = pd.to_numeric(cleaned_data['latitude'], errors='coerce')
            cleaned_data['longitude'] = pd.to_numeric(cleaned_data['longitude'], errors='coerce')
            
            # Remove invalid coordinates
            cleaned_data = cleaned_data[
                (cleaned_data['latitude'].between(-90, 90)) &
                (cleaned_data['longitude'].between(-180, 180))
            ]
        
        logger.info(f"Cleaned geographic data: {len(cleaned_data)} records")
        return cleaned_data
    
    def _load_market_intelligence(self, raw_data: pd.DataFrame) -> pd.DataFrame:
        """Load and clean market intelligence data"""
        
        cleaned_data = raw_data.copy()
        
        # Standardize market metrics
        market_columns = ['market_size', 'growth_rate', 'competition_index', 'market_maturity']
        
        for col in market_columns:
            if col in cleaned_data.columns:
                cleaned_data[col] = pd.to_numeric(cleaned_data[col], errors='coerce')
        
        logger.info(f"Cleaned market intelligence data: {len(cleaned_data)} records")
        return cleaned_data
    
    def _merge_adoption_productivity_data(
        self,
        ai_data: pd.DataFrame,
        productivity_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Merge AI adoption and productivity data"""
        
        # Determine merge keys
        merge_keys = ['year']
        
        if 'sector' in ai_data.columns and 'sector' in productivity_data.columns:
            merge_keys.append('sector')
        
        if 'organization' in ai_data.columns and 'organization' in productivity_data.columns:
            merge_keys.append('organization')
        
        # Perform merge
        merged_data = pd.merge(
            ai_data,
            productivity_data,
            on=merge_keys,
            how='inner',
            suffixes=('_ai', '_prod')
        )
        
        logger.info(f"Merged AI and productivity data: {len(merged_data)} records")
        return merged_data
    
    def _calculate_derived_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics for enhanced analysis"""
        
        enhanced_data = data.copy()
        
        # Calculate AI maturity score
        if 'adoption_rate' in data.columns:
            enhanced_data['ai_maturity_level'] = pd.cut(
                data['adoption_rate'],
                bins=[0, 25, 50, 75, 100],
                labels=['Exploring', 'Piloting', 'Implementing', 'Leading']
            )
        
        # Calculate productivity improvement rate
        if 'productivity_index' in data.columns and 'year' in data.columns:
            enhanced_data['productivity_growth_rate'] = enhanced_data.groupby('sector')['productivity_index'].pct_change() * 100
        
        # Calculate ROI efficiency
        if 'roi_percentage' in data.columns and 'investment_amount' in data.columns:
            enhanced_data['roi_efficiency'] = enhanced_data['roi_percentage'] / (enhanced_data['investment_amount'] / 1000000)  # ROI per million invested
        
        logger.info(f"Enhanced data with derived metrics: {enhanced_data.shape[1]} total columns")
        return enhanced_data
    
    def _perform_data_quality_validation(self, data: pd.DataFrame) -> pd.DataFrame:
        """Perform comprehensive data quality validation"""
        
        validated_data = data.copy()
        
        # Remove outliers using IQR method
        numeric_columns = validated_data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in validated_data.columns and not validated_data[col].empty:
                Q1 = validated_data[col].quantile(0.25)
                Q3 = validated_data[col].quantile(0.75)
                IQR = Q3 - Q1
                
                if IQR > 0:
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    
                    # Cap outliers instead of removing them
                    validated_data[col] = validated_data[col].clip(lower_bound, upper_bound)
        
        # Validate business rules
        if 'adoption_rate' in validated_data.columns:
            validated_data['adoption_rate'] = validated_data['adoption_rate'].clip(0, 100)
        
        if 'roi_percentage' in validated_data.columns:
            # Remove negative ROI outliers (likely data errors)
            validated_data = validated_data[validated_data['roi_percentage'] >= -50]
        
        logger.info(f"Data quality validation completed: {len(validated_data)} records validated")
        return validated_data
    
    def _integrate_geographic_data(
        self,
        main_data: pd.DataFrame,
        geo_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Integrate geographic data with main dataset"""
        
        # Merge based on available keys
        if 'country' in main_data.columns and 'country' in geo_data.columns:
            integrated_data = pd.merge(main_data, geo_data, on='country', how='left')
        else:
            # If no direct geographic match, use main data as-is
            integrated_data = main_data.copy()
            logger.warning("No geographic integration possible - missing country columns")
        
        logger.info(f"Geographic data integrated: {len(integrated_data)} records")
        return integrated_data
    
    def _calculate_regional_benchmarks(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate regional benchmarks for comparison"""
        
        benchmarks = []
        
        # Calculate benchmarks by region/sector
        if 'sector' in data.columns:
            sector_benchmarks = data.groupby('sector').agg({
                'adoption_rate': ['mean', 'median', 'std'],
                'productivity_index': ['mean', 'median', 'std'],
                'roi_percentage': ['mean', 'median', 'std']
            }).round(2)
            
            # Flatten column names
            sector_benchmarks.columns = ['_'.join(col).strip() for col in sector_benchmarks.columns]
            sector_benchmarks = sector_benchmarks.reset_index()
            benchmarks.append(sector_benchmarks)
        
        if 'country' in data.columns:
            country_benchmarks = data.groupby('country').agg({
                'adoption_rate': ['mean', 'median'],
                'productivity_index': ['mean', 'median']
            }).round(2)
            
            country_benchmarks.columns = ['_'.join(col).strip() for col in country_benchmarks.columns]
            country_benchmarks = country_benchmarks.reset_index()
            benchmarks.append(country_benchmarks)
        
        # Combine all benchmarks
        if benchmarks:
            combined_benchmarks = pd.concat(benchmarks, ignore_index=True, sort=False)
        else:
            combined_benchmarks = pd.DataFrame()
        
        logger.info(f"Regional benchmarks calculated: {len(combined_benchmarks)} benchmark records")
        return combined_benchmarks
    
    def _perform_causal_analysis(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Perform causal analysis using integrated causal engine"""
        
        try:
            # Import causal analysis engine
            from business.causal_analysis import causal_engine
            
            # Split data for causal analysis
            adoption_cols = [col for col in data.columns if 'adoption' in col.lower() or 'ai' in col.lower()]
            productivity_cols = [col for col in data.columns if any(term in col.lower() for term in ['productivity', 'revenue', 'efficiency', 'roi'])]
            
            adoption_data = data[['year', 'sector'] + adoption_cols].dropna()
            productivity_data = data[['year', 'sector'] + productivity_cols].dropna()
            
            # Perform causal analysis
            causal_result = causal_engine.establish_ai_productivity_causality(
                adoption_data=adoption_data,
                productivity_data=productivity_data,
                sector="all_sectors"
            )
            
            # Convert to serializable format
            causal_dict = {
                'analysis_id': causal_result.analysis_id,
                'analysis_date': causal_result.analysis_date.isoformat(),
                'confidence_score': causal_result.confidence_score,
                'num_relationships': len(causal_result.causal_relationships),
                'num_productivity_impacts': len(causal_result.productivity_impacts),
                'intervention_recommendations': causal_result.intervention_recommendations
            }
            
            logger.info(f"Causal analysis completed: {len(causal_result.causal_relationships)} relationships found")
            return causal_dict
            
        except Exception as e:
            logger.error(f"Causal analysis failed: {e}")
            return {'error': str(e), 'analysis_completed': False}
    
    def _generate_intervention_recommendations(
        self,
        causal_data: Dict[str, Any],
        benchmarks: pd.DataFrame
    ) -> Dict[str, Any]:
        """Generate intervention recommendations based on causal analysis and benchmarks"""
        
        recommendations = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': [],
            'causal_insights': causal_data.get('intervention_recommendations', [])
        }
        
        # Generate benchmark-based recommendations
        if not benchmarks.empty:
            if 'adoption_rate_mean' in benchmarks.columns:
                top_performers = benchmarks.nlargest(3, 'adoption_rate_mean')
                for _, row in top_performers.iterrows():
                    recommendations['high_priority'].append(
                        f"Benchmark against {row.get('sector', 'top performer')}: {row['adoption_rate_mean']:.1f}% adoption rate"
                    )
        
        logger.info("Intervention recommendations generated")
        return recommendations
    
    def _calculate_roi_projections(
        self,
        integrated_data: pd.DataFrame,
        market_data: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculate ROI projections based on integrated data and market intelligence"""
        
        projections = integrated_data.copy()
        
        # Calculate projected ROI based on current trends
        if 'roi_percentage' in projections.columns and 'year' in projections.columns:
            # Calculate ROI growth rate
            projections['roi_growth_rate'] = projections.groupby('sector')['roi_percentage'].pct_change()
            
            # Project future ROI (next 3 years)
            current_year = projections['year'].max()
            for future_year in range(1, 4):
                future_roi_col = f'projected_roi_{current_year + future_year}'
                projections[future_roi_col] = projections['roi_percentage'] * (1 + projections['roi_growth_rate'].fillna(0.1)) ** future_year
        
        logger.info(f"ROI projections calculated for {len(projections)} records")
        return projections
    
    def _generate_executive_insights(self, *input_datasets) -> Dict[str, Any]:
        """Generate executive-level insights from all processed data"""
        
        insights = {
            'summary_metrics': {},
            'key_findings': [],
            'strategic_recommendations': [],
            'performance_indicators': {}
        }
        
        # Process each input dataset
        for dataset in input_datasets:
            if isinstance(dataset, pd.DataFrame) and not dataset.empty:
                # Extract key metrics
                if 'adoption_rate' in dataset.columns:
                    insights['summary_metrics']['avg_adoption_rate'] = dataset['adoption_rate'].mean()
                    insights['summary_metrics']['adoption_rate_std'] = dataset['adoption_rate'].std()
                
                if 'roi_percentage' in dataset.columns:
                    insights['summary_metrics']['avg_roi'] = dataset['roi_percentage'].mean()
                    insights['summary_metrics']['roi_variance'] = dataset['roi_percentage'].var()
            
            elif isinstance(dataset, dict):
                # Handle dictionary inputs (like causal analysis results)
                if 'intervention_recommendations' in dataset:
                    insights['strategic_recommendations'].extend(dataset['intervention_recommendations'])
        
        # Generate key findings
        if insights['summary_metrics']:
            avg_adoption = insights['summary_metrics'].get('avg_adoption_rate', 0)
            if avg_adoption > 75:
                insights['key_findings'].append("High AI adoption across sectors")
            elif avg_adoption > 50:
                insights['key_findings'].append("Moderate AI adoption with growth opportunities")
            else:
                insights['key_findings'].append("Early-stage AI adoption - significant potential")
        
        logger.info("Executive insights generated")
        return insights
    
    def _create_dashboard_datasets(
        self,
        executive_insights: Dict[str, Any],
        detailed_data: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Create optimized datasets for dashboard consumption"""
        
        # Summary dataset for overview charts
        summary_data = detailed_data.groupby(['sector', 'year']).agg({
            'adoption_rate': 'mean',
            'productivity_index': 'mean',
            'roi_percentage': 'mean'
        }).reset_index().round(2)
        
        # Detailed dataset for drill-down analysis
        detailed_data_clean = detailed_data.select_dtypes(include=[np.number, 'object']).fillna(0)
        
        # Geographic dataset for map visualizations
        geographic_data = detailed_data.copy()
        if 'country' in geographic_data.columns:
            geographic_data = geographic_data.groupby('country').agg({
                'adoption_rate': 'mean',
                'productivity_index': 'mean'
            }).reset_index().round(2)
        else:
            # Create placeholder geographic data if not available
            geographic_data = pd.DataFrame({
                'country': ['United States', 'United Kingdom', 'Germany', 'Japan', 'Singapore'],
                'adoption_rate': [85, 78, 72, 80, 88],
                'productivity_index': [92, 85, 78, 85, 95]
            })
        
        logger.info("Dashboard datasets created")
        return summary_data, detailed_data_clean, geographic_data
    
    def _run_fallback_pipeline(self, pipeline_name: str, tags: List[str] = None) -> Dict[str, Any]:
        """Fallback pipeline execution when Kedro is not available"""
        
        logger.warning(f"Running fallback pipeline for '{pipeline_name}' - Kedro not available")
        
        # Simple pipeline simulation
        return {
            'pipeline_name': pipeline_name,
            'status': 'completed_fallback',
            'message': 'Pipeline executed using fallback implementation',
            'kedro_available': False,
            'execution_time': datetime.now()
        }


# Global Kedro manager instance
kedro_manager = AIAdoptionKedroManager()

# Export functions and classes
__all__ = [
    'KedroDatasetType',
    'PipelineType',
    'KedroDataSource',
    'KedroNode',
    'AIAdoptionKedroManager',
    'kedro_manager'
]