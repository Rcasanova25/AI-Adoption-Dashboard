"""Data loading and validation module"""

from .loaders import load_all_datasets, validate_all_loaded_data
from .models import safe_validate_data, ValidationResult
from .geographic import get_geographic_data, get_country_details, generate_geographic_insights
from .advanced_analytics import advanced_analytics, PredictionResult, TrendAnalysis, ClusteringResult
from .quality_assurance import quality_engine, QualityReport, QualityDimension
from .integration import integration_engine, DataPipeline, PipelineExecution

__all__ = [
    'load_all_datasets', 'validate_all_loaded_data', 'safe_validate_data', 'ValidationResult',
    'get_geographic_data', 'get_country_details', 'generate_geographic_insights',
    'advanced_analytics', 'PredictionResult', 'TrendAnalysis', 'ClusteringResult',
    'quality_engine', 'QualityReport', 'QualityDimension',
    'integration_engine', 'DataPipeline', 'PipelineExecution'
]