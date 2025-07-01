"""
Data Integration Engine for AI Adoption Dashboard
Provides comprehensive data integration, transformation, and pipeline management capabilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import logging
import json
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

logger = logging.getLogger(__name__)

class DataSourceType(Enum):
    DATABASE = "Database"
    API = "API"
    FILE = "File"
    STREAM = "Stream"
    CLOUD_STORAGE = "Cloud Storage"

class TransformationType(Enum):
    CLEAN = "Clean"
    AGGREGATE = "Aggregate"
    JOIN = "Join"
    FILTER = "Filter"
    ENRICH = "Enrich"
    VALIDATE = "Validate"

class PipelineStatus(Enum):
    PENDING = "Pending"
    RUNNING = "Running"
    COMPLETED = "Completed"
    FAILED = "Failed"
    PAUSED = "Paused"

@dataclass
class DataSource:
    """Data source configuration"""
    source_id: str
    name: str
    source_type: DataSourceType
    connection_config: Dict[str, Any]
    schema_definition: Dict[str, str]
    refresh_frequency: str
    last_updated: Optional[datetime]
    data_quality_threshold: float
    business_owner: str

@dataclass
class TransformationStep:
    """Data transformation step definition"""
    step_id: str
    name: str
    transformation_type: TransformationType
    parameters: Dict[str, Any]
    input_dependencies: List[str]
    output_schema: Dict[str, str]
    validation_rules: List[str]
    error_handling: str

@dataclass
class DataPipeline:
    """Complete data pipeline definition"""
    pipeline_id: str
    name: str
    description: str
    data_sources: List[DataSource]
    transformation_steps: List[TransformationStep]
    output_destinations: List[str]
    schedule: str
    status: PipelineStatus
    created_date: datetime
    last_run: Optional[datetime]
    success_rate: float

@dataclass
class PipelineExecution:
    """Pipeline execution results"""
    execution_id: str
    pipeline_id: str
    start_time: datetime
    end_time: Optional[datetime]
    status: PipelineStatus
    records_processed: int
    errors_encountered: List[str]
    performance_metrics: Dict[str, float]
    data_quality_scores: Dict[str, float]

class DataIntegrationEngine:
    """Advanced data integration and pipeline management engine"""
    
    def __init__(self):
        self.registered_sources = {}
        self.active_pipelines = {}
        self.execution_history = []
        self.transformation_library = self._initialize_transformation_library()
        
    def register_data_source(
        self,
        source_config: DataSource
    ) -> bool:
        """
        Register a new data source with the integration engine
        """
        
        try:
            # Validate source configuration
            validation_result = self._validate_source_config(source_config)
            if not validation_result['is_valid']:
                logger.error(f"Invalid source configuration: {validation_result['errors']}")
                return False
            
            # Test connection
            connection_test = self._test_source_connection(source_config)
            if not connection_test['success']:
                logger.error(f"Connection test failed: {connection_test['error']}")
                return False
            
            # Register the source
            self.registered_sources[source_config.source_id] = source_config
            logger.info(f"Successfully registered data source: {source_config.name}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error registering data source: {e}")
            return False
    
    def create_data_pipeline(
        self,
        pipeline_config: DataPipeline
    ) -> str:
        """
        Create a new data integration pipeline
        """
        
        try:
            # Validate pipeline configuration
            validation_result = self._validate_pipeline_config(pipeline_config)
            if not validation_result['is_valid']:
                raise ValueError(f"Invalid pipeline configuration: {validation_result['errors']}")
            
            # Optimize pipeline execution order
            optimized_steps = self._optimize_pipeline_execution(pipeline_config.transformation_steps)
            pipeline_config.transformation_steps = optimized_steps
            
            # Register the pipeline
            self.active_pipelines[pipeline_config.pipeline_id] = pipeline_config
            
            logger.info(f"Successfully created pipeline: {pipeline_config.name}")
            return pipeline_config.pipeline_id
            
        except Exception as e:
            logger.error(f"Error creating pipeline: {e}")
            raise
    
    def execute_pipeline(
        self,
        pipeline_id: str,
        execution_mode: str = "full",
        custom_parameters: Optional[Dict[str, Any]] = None
    ) -> PipelineExecution:
        """
        Execute a data integration pipeline
        """
        
        if pipeline_id not in self.active_pipelines:
            raise ValueError(f"Pipeline {pipeline_id} not found")
        
        pipeline = self.active_pipelines[pipeline_id]
        execution_id = f"{pipeline_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        execution = PipelineExecution(
            execution_id=execution_id,
            pipeline_id=pipeline_id,
            start_time=datetime.now(),
            end_time=None,
            status=PipelineStatus.RUNNING,
            records_processed=0,
            errors_encountered=[],
            performance_metrics={},
            data_quality_scores={}
        )
        
        try:
            # Update pipeline status
            pipeline.status = PipelineStatus.RUNNING
            pipeline.last_run = datetime.now()
            
            # Execute pipeline steps
            execution_results = self._execute_pipeline_steps(
                pipeline, execution_mode, custom_parameters
            )
            
            # Update execution results
            execution.records_processed = execution_results['total_records']
            execution.errors_encountered = execution_results['errors']
            execution.performance_metrics = execution_results['performance']
            execution.data_quality_scores = execution_results['quality_scores']
            execution.status = PipelineStatus.COMPLETED
            execution.end_time = datetime.now()
            
            # Update pipeline success rate
            self._update_pipeline_success_rate(pipeline_id, True)
            
            logger.info(f"Pipeline {pipeline_id} executed successfully")
            
        except Exception as e:
            execution.status = PipelineStatus.FAILED
            execution.end_time = datetime.now()
            execution.errors_encountered.append(str(e))
            
            # Update pipeline success rate
            self._update_pipeline_success_rate(pipeline_id, False)
            
            logger.error(f"Pipeline {pipeline_id} execution failed: {e}")
        
        finally:
            pipeline.status = execution.status
            self.execution_history.append(execution)
        
        return execution
    
    def create_ai_adoption_integration_pipeline(
        self,
        source_mappings: Dict[str, str],
        target_schema: Dict[str, str],
        quality_requirements: Dict[str, float]
    ) -> str:
        """
        Create specialized pipeline for AI adoption data integration
        """
        
        pipeline_id = f"ai_adoption_pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Define AI adoption specific transformations
        transformation_steps = [
            TransformationStep(
                step_id="step_001",
                name="Data Source Integration",
                transformation_type=TransformationType.JOIN,
                parameters={
                    "join_type": "left",
                    "join_keys": ["sector", "year"],
                    "source_mappings": source_mappings
                },
                input_dependencies=[],
                output_schema=target_schema,
                validation_rules=["no_null_key_columns", "valid_date_ranges"],
                error_handling="skip_invalid_records"
            ),
            
            TransformationStep(
                step_id="step_002",
                name="AI Metrics Standardization",
                transformation_type=TransformationType.CLEAN,
                parameters={
                    "standardize_adoption_rates": True,
                    "normalize_roi_values": True,
                    "convert_percentage_formats": True,
                    "handle_missing_values": "interpolate"
                },
                input_dependencies=["step_001"],
                output_schema=target_schema,
                validation_rules=["adoption_rate_0_100", "positive_roi_values"],
                error_handling="log_and_continue"
            ),
            
            TransformationStep(
                step_id="step_003",
                name="Data Quality Enhancement",
                transformation_type=TransformationType.VALIDATE,
                parameters={
                    "quality_thresholds": quality_requirements,
                    "outlier_detection": True,
                    "consistency_checks": True,
                    "completeness_validation": True
                },
                input_dependencies=["step_002"],
                output_schema=target_schema,
                validation_rules=["data_quality_score_threshold"],
                error_handling="quarantine_poor_quality"
            ),
            
            TransformationStep(
                step_id="step_004",
                name="Business Intelligence Enrichment",
                transformation_type=TransformationType.ENRICH,
                parameters={
                    "calculate_growth_rates": True,
                    "derive_maturity_levels": True,
                    "compute_benchmarks": True,
                    "generate_insights": True
                },
                input_dependencies=["step_003"],
                output_schema=target_schema,
                validation_rules=["derived_metrics_valid"],
                error_handling="use_fallback_calculations"
            )
        ]
        
        # Create data sources for AI adoption data
        data_sources = [
            DataSource(
                source_id="historical_ai_data",
                name="Historical AI Adoption Data",
                source_type=DataSourceType.FILE,
                connection_config={"path": "data/historical", "format": "csv"},
                schema_definition={"year": "int", "ai_use": "float", "sector": "string"},
                refresh_frequency="weekly",
                last_updated=None,
                data_quality_threshold=8.0,
                business_owner="Data Analytics Team"
            ),
            
            DataSource(
                source_id="sector_benchmarks",
                name="Industry Sector Benchmarks",
                source_type=DataSourceType.FILE,
                connection_config={"path": "data/benchmarks", "format": "csv"},
                schema_definition={"sector": "string", "adoption_rate": "float", "avg_roi": "float"},
                refresh_frequency="monthly",
                last_updated=None,
                data_quality_threshold=9.0,
                business_owner="Business Intelligence Team"
            )
        ]
        
        # Create the pipeline
        pipeline = DataPipeline(
            pipeline_id=pipeline_id,
            name="AI Adoption Data Integration Pipeline",
            description="Comprehensive pipeline for integrating and processing AI adoption data",
            data_sources=data_sources,
            transformation_steps=transformation_steps,
            output_destinations=["ai_adoption_warehouse", "analytics_dashboard"],
            schedule="daily",
            status=PipelineStatus.PENDING,
            created_date=datetime.now(),
            last_run=None,
            success_rate=0.0
        )
        
        return self.create_data_pipeline(pipeline)
    
    def monitor_pipeline_health(
        self,
        pipeline_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Monitor pipeline health and performance
        """
        
        health_report = {
            'overall_health': 'Good',
            'active_pipelines': len(self.active_pipelines),
            'total_executions': len(self.execution_history),
            'pipeline_details': {},
            'alerts': [],
            'recommendations': []
        }
        
        # Monitor specific pipeline or all pipelines
        pipelines_to_monitor = []
        if pipeline_id:
            if pipeline_id in self.active_pipelines:
                pipelines_to_monitor = [self.active_pipelines[pipeline_id]]
        else:
            pipelines_to_monitor = list(self.active_pipelines.values())
        
        critical_issues = 0
        warning_issues = 0
        
        for pipeline in pipelines_to_monitor:
            pipeline_health = self._assess_pipeline_health(pipeline)
            health_report['pipeline_details'][pipeline.pipeline_id] = pipeline_health
            
            # Count issues
            critical_issues += len(pipeline_health.get('critical_issues', []))
            warning_issues += len(pipeline_health.get('warnings', []))
            
            # Collect alerts
            health_report['alerts'].extend(pipeline_health.get('alerts', []))
        
        # Determine overall health
        if critical_issues > 0:
            health_report['overall_health'] = 'Critical'
        elif warning_issues > 2:
            health_report['overall_health'] = 'Warning'
        
        # Generate recommendations
        health_report['recommendations'] = self._generate_pipeline_recommendations(
            health_report['pipeline_details']
        )
        
        return health_report
    
    def create_real_time_data_stream(
        self,
        stream_config: Dict[str, Any]
    ) -> str:
        """
        Create real-time data streaming pipeline
        """
        
        stream_id = f"stream_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Real-time streaming is simulated in this implementation
        # In production, this would integrate with streaming platforms like Kafka, Kinesis, etc.
        
        streaming_pipeline = {
            'stream_id': stream_id,
            'config': stream_config,
            'status': 'active',
            'created_at': datetime.now(),
            'metrics': {
                'messages_processed': 0,
                'processing_latency': 0,
                'error_rate': 0
            }
        }
        
        logger.info(f"Created real-time data stream: {stream_id}")
        return stream_id
    
    def get_integration_metrics(self) -> Dict[str, Any]:
        """
        Get comprehensive integration metrics and KPIs
        """
        
        metrics = {
            'pipeline_metrics': {
                'total_pipelines': len(self.active_pipelines),
                'active_pipelines': sum(1 for p in self.active_pipelines.values() 
                                      if p.status == PipelineStatus.RUNNING),
                'avg_success_rate': np.mean([p.success_rate for p in self.active_pipelines.values()]) 
                                   if self.active_pipelines else 0
            },
            'execution_metrics': {
                'total_executions': len(self.execution_history),
                'successful_executions': sum(1 for e in self.execution_history 
                                            if e.status == PipelineStatus.COMPLETED),
                'failed_executions': sum(1 for e in self.execution_history 
                                       if e.status == PipelineStatus.FAILED),
                'avg_execution_time': self._calculate_avg_execution_time()
            },
            'data_volume_metrics': {
                'total_records_processed': sum(e.records_processed for e in self.execution_history),
                'daily_processing_volume': self._calculate_daily_processing_volume(),
                'peak_processing_time': self._identify_peak_processing_time()
            },
            'quality_metrics': {
                'avg_data_quality_score': self._calculate_avg_quality_score(),
                'quality_improvement_trend': self._calculate_quality_trend(),
                'data_sources_above_threshold': self._count_sources_above_threshold()
            }
        }
        
        return metrics
    
    def _execute_pipeline_steps(
        self,
        pipeline: DataPipeline,
        execution_mode: str,
        custom_parameters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute all steps in a pipeline"""
        
        results = {
            'total_records': 0,
            'errors': [],
            'performance': {},
            'quality_scores': {}
        }
        
        step_data = {}  # Store intermediate data between steps
        
        try:
            # Load data from sources
            source_data = self._load_source_data(pipeline.data_sources, execution_mode)
            step_data['source_data'] = source_data
            
            # Execute transformation steps in order
            for step in pipeline.transformation_steps:
                step_start_time = datetime.now()
                
                try:
                    # Execute transformation
                    step_result = self._execute_transformation_step(
                        step, step_data, custom_parameters
                    )
                    
                    # Store result for next step
                    step_data[step.step_id] = step_result['data']
                    
                    # Track performance
                    step_duration = (datetime.now() - step_start_time).total_seconds()
                    results['performance'][step.step_id] = step_duration
                    
                    # Update record count
                    if isinstance(step_result['data'], pd.DataFrame):
                        results['total_records'] = len(step_result['data'])
                    
                    # Store quality scores
                    if 'quality_score' in step_result:
                        results['quality_scores'][step.step_id] = step_result['quality_score']
                    
                except Exception as e:
                    error_msg = f"Step {step.step_id} failed: {str(e)}"
                    results['errors'].append(error_msg)
                    
                    if step.error_handling == "fail_pipeline":
                        raise Exception(error_msg)
                    elif step.error_handling == "skip_step":
                        continue
                    # For "log_and_continue", we just continue with next step
            
        except Exception as e:
            results['errors'].append(f"Pipeline execution failed: {str(e)}")
            raise
        
        return results
    
    def _execute_transformation_step(
        self,
        step: TransformationStep,
        step_data: Dict[str, Any],
        custom_parameters: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute a single transformation step"""
        
        # Get input data
        if step.input_dependencies:
            input_data = step_data[step.input_dependencies[0]]
        else:
            input_data = step_data.get('source_data', pd.DataFrame())
        
        # Merge custom parameters
        parameters = step.parameters.copy()
        if custom_parameters:
            parameters.update(custom_parameters)
        
        # Execute transformation based on type
        if step.transformation_type == TransformationType.CLEAN:
            result_data = self._clean_data(input_data, parameters)
        elif step.transformation_type == TransformationType.AGGREGATE:
            result_data = self._aggregate_data(input_data, parameters)
        elif step.transformation_type == TransformationType.JOIN:
            result_data = self._join_data(input_data, step_data, parameters)
        elif step.transformation_type == TransformationType.FILTER:
            result_data = self._filter_data(input_data, parameters)
        elif step.transformation_type == TransformationType.ENRICH:
            result_data = self._enrich_data(input_data, parameters)
        elif step.transformation_type == TransformationType.VALIDATE:
            result_data = self._validate_data(input_data, parameters)
        else:
            result_data = input_data.copy()
        
        # Apply validation rules
        validation_result = self._apply_validation_rules(result_data, step.validation_rules)
        
        return {
            'data': result_data,
            'validation_passed': validation_result['passed'],
            'validation_errors': validation_result['errors'],
            'quality_score': validation_result.get('quality_score', 8.0)
        }
    
    def _clean_data(self, data: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Clean data based on parameters"""
        
        cleaned_data = data.copy()
        
        if parameters.get('standardize_adoption_rates', False):
            # Ensure adoption rates are in 0-100 range
            adoption_cols = [col for col in cleaned_data.columns if 'adoption' in col.lower()]
            for col in adoption_cols:
                if col in cleaned_data.columns:
                    # Convert to percentage if values are in 0-1 range
                    if cleaned_data[col].max() <= 1.0:
                        cleaned_data[col] = cleaned_data[col] * 100
                    # Cap at 100%
                    cleaned_data[col] = cleaned_data[col].clip(0, 100)
        
        if parameters.get('normalize_roi_values', False):
            # Normalize ROI values
            roi_cols = [col for col in cleaned_data.columns if 'roi' in col.lower()]
            for col in roi_cols:
                if col in cleaned_data.columns:
                    # Ensure positive values
                    cleaned_data[col] = cleaned_data[col].abs()
        
        if parameters.get('handle_missing_values') == 'interpolate':
            # Interpolate missing values for numeric columns
            numeric_cols = cleaned_data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                cleaned_data[col] = cleaned_data[col].interpolate(method='linear')
        
        return cleaned_data
    
    def _aggregate_data(self, data: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Aggregate data based on parameters"""
        
        if data.empty:
            return data
        
        group_by = parameters.get('group_by', [])
        aggregations = parameters.get('aggregations', {})
        
        if group_by and aggregations:
            return data.groupby(group_by).agg(aggregations).reset_index()
        
        return data
    
    def _join_data(
        self,
        data: pd.DataFrame,
        step_data: Dict[str, Any],
        parameters: Dict[str, Any]
    ) -> pd.DataFrame:
        """Join data based on parameters"""
        
        join_type = parameters.get('join_type', 'left')
        join_keys = parameters.get('join_keys', [])
        
        # For simplified implementation, return original data
        # In practice, this would perform complex joins
        return data
    
    def _filter_data(self, data: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Filter data based on parameters"""
        
        conditions = parameters.get('conditions', [])
        
        filtered_data = data.copy()
        for condition in conditions:
            if 'column' in condition and 'operator' in condition and 'value' in condition:
                col = condition['column']
                op = condition['operator']
                val = condition['value']
                
                if col in filtered_data.columns:
                    if op == 'gt':
                        filtered_data = filtered_data[filtered_data[col] > val]
                    elif op == 'lt':
                        filtered_data = filtered_data[filtered_data[col] < val]
                    elif op == 'eq':
                        filtered_data = filtered_data[filtered_data[col] == val]
        
        return filtered_data
    
    def _enrich_data(self, data: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Enrich data with derived metrics"""
        
        enriched_data = data.copy()
        
        if parameters.get('calculate_growth_rates', False) and 'year' in enriched_data.columns:
            # Calculate year-over-year growth rates
            adoption_cols = [col for col in enriched_data.columns if 'adoption' in col.lower()]
            for col in adoption_cols:
                growth_col = f"{col}_growth_rate"
                enriched_data[growth_col] = enriched_data.groupby('sector')[col].pct_change() * 100
        
        if parameters.get('derive_maturity_levels', False):
            # Derive AI maturity levels
            if 'adoption_rate' in enriched_data.columns:
                def get_maturity_level(adoption_rate):
                    if adoption_rate >= 80:
                        return "Leading"
                    elif adoption_rate >= 50:
                        return "Scaling"
                    elif adoption_rate >= 25:
                        return "Implementing"
                    elif adoption_rate >= 10:
                        return "Piloting"
                    else:
                        return "Exploring"
                
                enriched_data['maturity_level'] = enriched_data['adoption_rate'].apply(get_maturity_level)
        
        return enriched_data
    
    def _validate_data(self, data: pd.DataFrame, parameters: Dict[str, Any]) -> pd.DataFrame:
        """Validate data quality"""
        
        quality_thresholds = parameters.get('quality_thresholds', {})
        
        # Perform basic quality validations
        if parameters.get('outlier_detection', False):
            # Remove outliers (simplified)
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if len(data[col].dropna()) > 3:
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    lower_bound = Q1 - 1.5 * IQR
                    upper_bound = Q3 + 1.5 * IQR
                    data = data[(data[col] >= lower_bound) & (data[col] <= upper_bound)]
        
        return data
    
    def _apply_validation_rules(
        self,
        data: pd.DataFrame,
        validation_rules: List[str]
    ) -> Dict[str, Any]:
        """Apply validation rules to data"""
        
        validation_result = {
            'passed': True,
            'errors': [],
            'quality_score': 8.0
        }
        
        for rule in validation_rules:
            if rule == "no_null_key_columns":
                key_columns = ['sector', 'year']
                for col in key_columns:
                    if col in data.columns and data[col].isnull().any():
                        validation_result['errors'].append(f"Null values found in key column: {col}")
                        validation_result['passed'] = False
            
            elif rule == "adoption_rate_0_100":
                adoption_cols = [col for col in data.columns if 'adoption' in col.lower()]
                for col in adoption_cols:
                    if col in data.columns:
                        invalid_values = ((data[col] < 0) | (data[col] > 100)).sum()
                        if invalid_values > 0:
                            validation_result['errors'].append(f"Invalid adoption rates in {col}: {invalid_values} values")
        
        # Adjust quality score based on errors
        if validation_result['errors']:
            validation_result['quality_score'] -= len(validation_result['errors']) * 0.5
        
        return validation_result
    
    def _load_source_data(
        self,
        sources: List[DataSource],
        execution_mode: str
    ) -> pd.DataFrame:
        """Load data from configured sources"""
        
        # Simplified implementation - return sample data
        # In practice, this would load from actual data sources
        
        sample_data = pd.DataFrame({
            'year': [2023, 2024, 2025],
            'sector': ['Technology', 'Healthcare', 'Finance'],
            'adoption_rate': [92, 78, 85],
            'avg_roi': [4.2, 3.2, 3.8]
        })
        
        return sample_data
    
    def _optimize_pipeline_execution(
        self,
        steps: List[TransformationStep]
    ) -> List[TransformationStep]:
        """Optimize pipeline execution order"""
        
        # Simple dependency-based ordering
        # In practice, this would use topological sorting
        
        return sorted(steps, key=lambda s: len(s.input_dependencies))
    
    def _validate_source_config(self, source: DataSource) -> Dict[str, Any]:
        """Validate data source configuration"""
        
        errors = []
        
        if not source.source_id:
            errors.append("Source ID is required")
        
        if not source.name:
            errors.append("Source name is required")
        
        if source.data_quality_threshold < 0 or source.data_quality_threshold > 10:
            errors.append("Data quality threshold must be between 0 and 10")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _validate_pipeline_config(self, pipeline: DataPipeline) -> Dict[str, Any]:
        """Validate pipeline configuration"""
        
        errors = []
        
        if not pipeline.pipeline_id:
            errors.append("Pipeline ID is required")
        
        if not pipeline.transformation_steps:
            errors.append("At least one transformation step is required")
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors
        }
    
    def _test_source_connection(self, source: DataSource) -> Dict[str, Any]:
        """Test connection to data source"""
        
        # Simplified implementation
        return {'success': True, 'error': None}
    
    def _assess_pipeline_health(self, pipeline: DataPipeline) -> Dict[str, Any]:
        """Assess health of a specific pipeline"""
        
        health_assessment = {
            'pipeline_id': pipeline.pipeline_id,
            'status': pipeline.status.value,
            'success_rate': pipeline.success_rate,
            'last_run': pipeline.last_run,
            'critical_issues': [],
            'warnings': [],
            'alerts': []
        }
        
        # Check for critical issues
        if pipeline.success_rate < 0.8:
            health_assessment['critical_issues'].append("Low success rate")
            health_assessment['alerts'].append({
                'severity': 'Critical',
                'message': f"Pipeline {pipeline.name} has success rate below 80%"
            })
        
        # Check for warnings
        if pipeline.last_run and (datetime.now() - pipeline.last_run).days > 1:
            health_assessment['warnings'].append("Pipeline hasn't run recently")
        
        return health_assessment
    
    def _update_pipeline_success_rate(self, pipeline_id: str, success: bool) -> None:
        """Update pipeline success rate"""
        
        if pipeline_id in self.active_pipelines:
            pipeline = self.active_pipelines[pipeline_id]
            
            # Simple moving average for success rate
            # In practice, this would be more sophisticated
            current_rate = pipeline.success_rate
            new_rate = (current_rate * 0.9) + (1.0 if success else 0.0) * 0.1
            pipeline.success_rate = new_rate
    
    def _generate_pipeline_recommendations(
        self,
        pipeline_details: Dict[str, Any]
    ) -> List[str]:
        """Generate pipeline improvement recommendations"""
        
        recommendations = []
        
        low_performance_pipelines = [
            pid for pid, details in pipeline_details.items()
            if details.get('success_rate', 1.0) < 0.8
        ]
        
        if low_performance_pipelines:
            recommendations.append("Review and optimize low-performing pipelines")
        
        recommendations.append("Implement automated pipeline monitoring")
        recommendations.append("Set up proactive alerting for pipeline failures")
        
        return recommendations
    
    def _calculate_avg_execution_time(self) -> float:
        """Calculate average pipeline execution time"""
        
        execution_times = []
        for execution in self.execution_history:
            if execution.start_time and execution.end_time:
                duration = (execution.end_time - execution.start_time).total_seconds()
                execution_times.append(duration)
        
        return np.mean(execution_times) if execution_times else 0.0
    
    def _calculate_daily_processing_volume(self) -> int:
        """Calculate daily data processing volume"""
        
        today = datetime.now().date()
        today_executions = [
            e for e in self.execution_history
            if e.start_time.date() == today
        ]
        
        return sum(e.records_processed for e in today_executions)
    
    def _identify_peak_processing_time(self) -> str:
        """Identify peak processing time"""
        
        hour_counts = {}
        for execution in self.execution_history:
            hour = execution.start_time.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        if hour_counts:
            peak_hour = max(hour_counts, key=hour_counts.get)
            return f"{peak_hour:02d}:00"
        
        return "N/A"
    
    def _calculate_avg_quality_score(self) -> float:
        """Calculate average data quality score"""
        
        quality_scores = []
        for execution in self.execution_history:
            if execution.data_quality_scores:
                quality_scores.extend(execution.data_quality_scores.values())
        
        return np.mean(quality_scores) if quality_scores else 8.0
    
    def _calculate_quality_trend(self) -> float:
        """Calculate data quality improvement trend"""
        
        # Simplified trend calculation
        recent_executions = self.execution_history[-10:] if len(self.execution_history) >= 10 else self.execution_history
        
        if len(recent_executions) < 2:
            return 0.0
        
        recent_scores = []
        for execution in recent_executions:
            if execution.data_quality_scores:
                avg_score = np.mean(list(execution.data_quality_scores.values()))
                recent_scores.append(avg_score)
        
        if len(recent_scores) >= 2:
            return (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
        
        return 0.0
    
    def _count_sources_above_threshold(self) -> int:
        """Count data sources above quality threshold"""
        
        return sum(
            1 for source in self.registered_sources.values()
            if source.data_quality_threshold >= 8.0
        )
    
    def _initialize_transformation_library(self) -> Dict[str, Callable]:
        """Initialize library of transformation functions"""
        
        return {
            'clean_adoption_rates': self._clean_data,
            'aggregate_by_sector': self._aggregate_data,
            'join_benchmark_data': self._join_data,
            'filter_recent_years': self._filter_data,
            'enrich_with_insights': self._enrich_data,
            'validate_data_quality': self._validate_data
        }

# Global data integration engine instance
integration_engine = DataIntegrationEngine()

# Export functions
__all__ = [
    'DataSourceType',
    'TransformationType', 
    'PipelineStatus',
    'DataSource',
    'TransformationStep',
    'DataPipeline',
    'PipelineExecution',
    'DataIntegrationEngine',
    'integration_engine'
]