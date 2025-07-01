"""
Data Quality Assurance Module for AI Adoption Dashboard
Provides comprehensive data quality monitoring, validation, and improvement capabilities
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import logging
import warnings

logger = logging.getLogger(__name__)

class QualityDimension(Enum):
    COMPLETENESS = "Completeness"
    ACCURACY = "Accuracy"
    CONSISTENCY = "Consistency"
    VALIDITY = "Validity"
    TIMELINESS = "Timeliness"
    UNIQUENESS = "Uniqueness"

class QualityLevel(Enum):
    EXCELLENT = "Excellent"
    GOOD = "Good"
    ACCEPTABLE = "Acceptable"
    POOR = "Poor"
    CRITICAL = "Critical"

@dataclass
class QualityRule:
    """Data quality rule definition"""
    rule_id: str
    name: str
    dimension: QualityDimension
    description: str
    validation_function: str
    threshold: float
    severity: str  # "Critical", "High", "Medium", "Low"
    columns: List[str]
    business_impact: str

@dataclass
class QualityIssue:
    """Data quality issue identified"""
    issue_id: str
    rule_id: str
    dimension: QualityDimension
    severity: str
    description: str
    affected_rows: int
    affected_columns: List[str]
    impact_score: float
    remediation_suggestion: str
    detection_date: datetime

@dataclass
class QualityReport:
    """Comprehensive data quality report"""
    dataset_name: str
    assessment_date: datetime
    overall_score: float
    dimension_scores: Dict[QualityDimension, float]
    quality_level: QualityLevel
    issues_identified: List[QualityIssue]
    improvement_recommendations: List[str]
    data_profile: Dict[str, Any]
    trend_analysis: Dict[str, float]

class DataQualityEngine:
    """Advanced data quality assessment and monitoring engine"""
    
    def __init__(self):
        self.quality_rules = self._initialize_quality_rules()
        self.dimension_weights = self._get_dimension_weights()
        self.quality_history = {}
        
    def assess_data_quality(
        self,
        data: pd.DataFrame,
        dataset_name: str,
        custom_rules: Optional[List[QualityRule]] = None,
        business_context: Optional[Dict[str, str]] = None
    ) -> QualityReport:
        """
        Perform comprehensive data quality assessment
        """
        
        if data.empty:
            return self._create_empty_data_report(dataset_name)
        
        # Apply quality rules
        all_rules = self.quality_rules.copy()
        if custom_rules:
            all_rules.extend(custom_rules)
        
        # Execute quality checks
        issues_identified = []
        dimension_scores = {}
        
        # Assess each quality dimension
        dimension_scores[QualityDimension.COMPLETENESS] = self._assess_completeness(data, issues_identified)
        dimension_scores[QualityDimension.ACCURACY] = self._assess_accuracy(data, issues_identified)
        dimension_scores[QualityDimension.CONSISTENCY] = self._assess_consistency(data, issues_identified)
        dimension_scores[QualityDimension.VALIDITY] = self._assess_validity(data, issues_identified)
        dimension_scores[QualityDimension.TIMELINESS] = self._assess_timeliness(data, issues_identified)
        dimension_scores[QualityDimension.UNIQUENESS] = self._assess_uniqueness(data, issues_identified)
        
        # Calculate overall quality score
        overall_score = self._calculate_overall_score(dimension_scores)
        
        # Determine quality level
        quality_level = self._determine_quality_level(overall_score)
        
        # Generate improvement recommendations
        recommendations = self._generate_improvement_recommendations(
            dimension_scores, issues_identified, business_context
        )
        
        # Create data profile
        data_profile = self._create_data_profile(data)
        
        # Analyze trends if historical data exists
        trend_analysis = self._analyze_quality_trends(dataset_name, dimension_scores)
        
        # Store quality history
        self._store_quality_history(dataset_name, dimension_scores, overall_score)
        
        return QualityReport(
            dataset_name=dataset_name,
            assessment_date=datetime.now(),
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            quality_level=quality_level,
            issues_identified=issues_identified,
            improvement_recommendations=recommendations,
            data_profile=data_profile,
            trend_analysis=trend_analysis
        )
    
    def monitor_data_quality_over_time(
        self,
        datasets: Dict[str, pd.DataFrame],
        monitoring_period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Monitor data quality trends over time
        """
        
        monitoring_results = {
            'monitoring_period': monitoring_period_days,
            'datasets_monitored': len(datasets),
            'quality_trends': {},
            'alerts': [],
            'overall_health': 'Good'
        }
        
        quality_deterioration_threshold = 0.1  # 10% drop in quality
        
        for dataset_name, data in datasets.items():
            # Assess current quality
            current_report = self.assess_data_quality(data, dataset_name)
            
            # Compare with historical data
            if dataset_name in self.quality_history:
                historical_scores = self.quality_history[dataset_name]
                
                if len(historical_scores) > 1:
                    # Calculate trend
                    recent_scores = [entry['overall_score'] for entry in historical_scores[-5:]]
                    trend = (recent_scores[-1] - recent_scores[0]) / len(recent_scores)
                    
                    monitoring_results['quality_trends'][dataset_name] = {
                        'current_score': current_report.overall_score,
                        'trend': trend,
                        'status': 'Improving' if trend > 0.01 else 'Stable' if trend > -0.01 else 'Declining'
                    }
                    
                    # Generate alerts for significant quality drops
                    if trend < -quality_deterioration_threshold:
                        monitoring_results['alerts'].append({
                            'dataset': dataset_name,
                            'alert_type': 'Quality Deterioration',
                            'severity': 'High',
                            'message': f'Quality score decreased by {abs(trend)*100:.1f}% over recent assessments',
                            'recommended_action': 'Investigate data sources and processing pipeline'
                        })
        
        # Determine overall health
        if monitoring_results['alerts']:
            high_severity_alerts = [a for a in monitoring_results['alerts'] if a['severity'] == 'High']
            if high_severity_alerts:
                monitoring_results['overall_health'] = 'Critical'
            else:
                monitoring_results['overall_health'] = 'Warning'
        
        return monitoring_results
    
    def create_data_quality_dashboard_metrics(
        self,
        datasets: Dict[str, pd.DataFrame]
    ) -> Dict[str, Any]:
        """
        Create metrics for data quality dashboard
        """
        
        dashboard_metrics = {
            'summary_metrics': {},
            'dimension_breakdown': {},
            'trend_indicators': {},
            'critical_issues': [],
            'recommendations': []
        }
        
        all_scores = []
        dimension_aggregates = {dim: [] for dim in QualityDimension}
        
        for dataset_name, data in datasets.items():
            report = self.assess_data_quality(data, dataset_name)
            
            all_scores.append(report.overall_score)
            
            # Aggregate dimension scores
            for dim, score in report.dimension_scores.items():
                dimension_aggregates[dim].append(score)
            
            # Collect critical issues
            critical_issues = [issue for issue in report.issues_identified if issue.severity == 'Critical']
            dashboard_metrics['critical_issues'].extend(critical_issues)
        
        # Calculate summary metrics
        if all_scores:
            dashboard_metrics['summary_metrics'] = {
                'overall_average_score': np.mean(all_scores),
                'datasets_above_threshold': sum(1 for score in all_scores if score >= 8.0),
                'datasets_below_threshold': sum(1 for score in all_scores if score < 6.0),
                'total_datasets': len(all_scores),
                'quality_variance': np.var(all_scores)
            }
            
            # Calculate dimension breakdown
            for dim, scores in dimension_aggregates.items():
                if scores:
                    dashboard_metrics['dimension_breakdown'][dim.value] = {
                        'average_score': np.mean(scores),
                        'min_score': np.min(scores),
                        'max_score': np.max(scores),
                        'std_deviation': np.std(scores)
                    }
        
        # Generate high-level recommendations
        dashboard_metrics['recommendations'] = self._generate_enterprise_recommendations(
            dashboard_metrics['summary_metrics'], dashboard_metrics['dimension_breakdown']
        )
        
        return dashboard_metrics
    
    def _assess_completeness(self, data: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """Assess data completeness"""
        
        total_cells = data.size
        if total_cells == 0:
            return 0.0
        
        missing_cells = data.isnull().sum().sum()
        completeness_score = ((total_cells - missing_cells) / total_cells) * 10
        
        # Identify columns with significant missing data
        for column in data.columns:
            missing_pct = data[column].isnull().mean()
            if missing_pct > 0.1:  # More than 10% missing
                severity = "Critical" if missing_pct > 0.5 else "High" if missing_pct > 0.25 else "Medium"
                
                issues.append(QualityIssue(
                    issue_id=f"COMP_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id="COMP_001",
                    dimension=QualityDimension.COMPLETENESS,
                    severity=severity,
                    description=f"Column '{column}' has {missing_pct*100:.1f}% missing values",
                    affected_rows=int(data[column].isnull().sum()),
                    affected_columns=[column],
                    impact_score=missing_pct * 10,
                    remediation_suggestion=f"Investigate data source for '{column}' and implement imputation strategy",
                    detection_date=datetime.now()
                ))
        
        return max(completeness_score, 0.0)
    
    def _assess_accuracy(self, data: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """Assess data accuracy"""
        
        accuracy_score = 8.5  # Default high accuracy score
        
        # Check for obviously incorrect values
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        for column in numeric_columns:
            if not data[column].empty:
                # Check for extreme outliers (more than 3 standard deviations)
                if data[column].std() > 0:
                    z_scores = np.abs((data[column] - data[column].mean()) / data[column].std())
                    outliers = (z_scores > 3).sum()
                    
                    if outliers > len(data) * 0.05:  # More than 5% outliers
                        issues.append(QualityIssue(
                            issue_id=f"ACC_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            rule_id="ACC_001",
                            dimension=QualityDimension.ACCURACY,
                            severity="Medium",
                            description=f"Column '{column}' has {outliers} potential outliers ({outliers/len(data)*100:.1f}%)",
                            affected_rows=outliers,
                            affected_columns=[column],
                            impact_score=min(outliers/len(data) * 10, 5),
                            remediation_suggestion=f"Review outliers in '{column}' for data entry errors",
                            detection_date=datetime.now()
                        ))
                        accuracy_score -= min(outliers/len(data) * 5, 2)
        
        # Check for negative values where they shouldn't exist (e.g., adoption rates)
        if 'adoption_rate' in data.columns:
            negative_adoption = (data['adoption_rate'] < 0).sum()
            if negative_adoption > 0:
                issues.append(QualityIssue(
                    issue_id=f"ACC_adoption_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id="ACC_002",
                    dimension=QualityDimension.ACCURACY,
                    severity="Critical",
                    description=f"Found {negative_adoption} negative adoption rate values",
                    affected_rows=negative_adoption,
                    affected_columns=['adoption_rate'],
                    impact_score=8.0,
                    remediation_suggestion="Correct negative adoption rate values",
                    detection_date=datetime.now()
                ))
                accuracy_score -= 3.0
        
        return max(accuracy_score, 0.0)
    
    def _assess_consistency(self, data: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """Assess data consistency"""
        
        consistency_score = 9.0  # Default high consistency score
        
        # Check for inconsistent data types within columns
        for column in data.columns:
            if data[column].dtype == 'object':
                # Check for mixed data types in string columns
                try:
                    # Try to convert to numeric - if some succeed and some fail, it's inconsistent
                    numeric_conversion = pd.to_numeric(data[column], errors='coerce')
                    mixed_types = numeric_conversion.isnull().sum() != len(data[column])
                    
                    if mixed_types and numeric_conversion.notna().sum() > 0:
                        issues.append(QualityIssue(
                            issue_id=f"CONS_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            rule_id="CONS_001",
                            dimension=QualityDimension.CONSISTENCY,
                            severity="Medium",
                            description=f"Column '{column}' contains mixed data types",
                            affected_rows=len(data),
                            affected_columns=[column],
                            impact_score=3.0,
                            remediation_suggestion=f"Standardize data types in column '{column}'",
                            detection_date=datetime.now()
                        ))
                        consistency_score -= 1.5
                except:
                    pass
        
        # Check for consistent formatting in categorical columns
        categorical_columns = data.select_dtypes(include=['object']).columns
        for column in categorical_columns:
            if column in data.columns and not data[column].empty:
                unique_values = data[column].dropna().unique()
                if len(unique_values) > 0:
                    # Check for potential formatting inconsistencies (case sensitivity)
                    lower_values = [str(val).lower() for val in unique_values]
                    if len(set(lower_values)) < len(unique_values):
                        issues.append(QualityIssue(
                            issue_id=f"CONS_case_{column}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                            rule_id="CONS_002",
                            dimension=QualityDimension.CONSISTENCY,
                            severity="Low",
                            description=f"Column '{column}' has case sensitivity inconsistencies",
                            affected_rows=len(data),
                            affected_columns=[column],
                            impact_score=1.0,
                            remediation_suggestion=f"Standardize case formatting in column '{column}'",
                            detection_date=datetime.now()
                        ))
                        consistency_score -= 0.5
        
        return max(consistency_score, 0.0)
    
    def _assess_validity(self, data: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """Assess data validity against business rules"""
        
        validity_score = 8.0  # Default validity score
        
        # Business rule validations for AI adoption data
        
        # 1. Adoption rates should be between 0 and 100
        if 'adoption_rate' in data.columns:
            invalid_adoption = ((data['adoption_rate'] < 0) | (data['adoption_rate'] > 100)).sum()
            if invalid_adoption > 0:
                issues.append(QualityIssue(
                    issue_id=f"VAL_adoption_range_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id="VAL_001",
                    dimension=QualityDimension.VALIDITY,
                    severity="High",
                    description=f"{invalid_adoption} adoption rate values outside valid range (0-100)",
                    affected_rows=invalid_adoption,
                    affected_columns=['adoption_rate'],
                    impact_score=min(invalid_adoption/len(data) * 10, 5),
                    remediation_suggestion="Correct adoption rate values to be within 0-100 range",
                    detection_date=datetime.now()
                ))
                validity_score -= min(invalid_adoption/len(data) * 5, 3)
        
        # 2. ROI values should be positive
        roi_columns = [col for col in data.columns if 'roi' in col.lower()]
        for col in roi_columns:
            if col in data.columns:
                negative_roi = (data[col] < 0).sum()
                if negative_roi > 0:
                    issues.append(QualityIssue(
                        issue_id=f"VAL_roi_{col}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        rule_id="VAL_002",
                        dimension=QualityDimension.VALIDITY,
                        severity="Medium",
                        description=f"Column '{col}' has {negative_roi} negative ROI values",
                        affected_rows=negative_roi,
                        affected_columns=[col],
                        impact_score=min(negative_roi/len(data) * 8, 4),
                        remediation_suggestion=f"Review negative ROI values in column '{col}'",
                        detection_date=datetime.now()
                    ))
                    validity_score -= min(negative_roi/len(data) * 3, 2)
        
        # 3. Year values should be reasonable
        if 'year' in data.columns:
            current_year = datetime.now().year
            invalid_years = ((data['year'] < 2000) | (data['year'] > current_year + 5)).sum()
            if invalid_years > 0:
                issues.append(QualityIssue(
                    issue_id=f"VAL_year_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id="VAL_003",
                    dimension=QualityDimension.VALIDITY,
                    severity="Medium",
                    description=f"{invalid_years} year values outside reasonable range",
                    affected_rows=invalid_years,
                    affected_columns=['year'],
                    impact_score=min(invalid_years/len(data) * 6, 3),
                    remediation_suggestion="Correct year values to be within reasonable range",
                    detection_date=datetime.now()
                ))
                validity_score -= min(invalid_years/len(data) * 2, 1)
        
        return max(validity_score, 0.0)
    
    def _assess_timeliness(self, data: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """Assess data timeliness"""
        
        timeliness_score = 7.5  # Default timeliness score
        
        # Check if data contains recent information
        if 'year' in data.columns and not data['year'].empty:
            max_year = data['year'].max()
            current_year = datetime.now().year
            
            if max_year < current_year - 2:  # Data is more than 2 years old
                issues.append(QualityIssue(
                    issue_id=f"TIME_outdated_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    rule_id="TIME_001",
                    dimension=QualityDimension.TIMELINESS,
                    severity="Medium",
                    description=f"Data appears outdated - latest year is {max_year}",
                    affected_rows=len(data),
                    affected_columns=['year'],
                    impact_score=4.0,
                    remediation_suggestion="Update dataset with more recent data",
                    detection_date=datetime.now()
                ))
                timeliness_score -= 2.0
            elif max_year == current_year:
                timeliness_score += 1.0  # Bonus for current data
        
        return max(timeliness_score, 0.0)
    
    def _assess_uniqueness(self, data: pd.DataFrame, issues: List[QualityIssue]) -> float:
        """Assess data uniqueness"""
        
        uniqueness_score = 9.0  # Default uniqueness score
        
        # Check for duplicate rows
        duplicate_rows = data.duplicated().sum()
        if duplicate_rows > 0:
            issues.append(QualityIssue(
                issue_id=f"UNIQ_duplicates_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id="UNIQ_001",
                dimension=QualityDimension.UNIQUENESS,
                severity="Medium",
                description=f"Found {duplicate_rows} duplicate rows",
                affected_rows=duplicate_rows,
                affected_columns=list(data.columns),
                impact_score=min(duplicate_rows/len(data) * 10, 5),
                remediation_suggestion="Remove or consolidate duplicate rows",
                detection_date=datetime.now()
            ))
            uniqueness_score -= min(duplicate_rows/len(data) * 5, 3)
        
        # Check for duplicate values in key columns
        key_columns = ['sector', 'industry', 'country']  # Columns that should have unique values
        for col in key_columns:
            if col in data.columns:
                total_values = len(data[col].dropna())
                unique_values = len(data[col].dropna().unique())
                
                if total_values > 0 and unique_values < total_values:
                    duplicate_count = total_values - unique_values
                    issues.append(QualityIssue(
                        issue_id=f"UNIQ_{col}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        rule_id="UNIQ_002",
                        dimension=QualityDimension.UNIQUENESS,
                        severity="Low",
                        description=f"Column '{col}' has {duplicate_count} duplicate values",
                        affected_rows=duplicate_count,
                        affected_columns=[col],
                        impact_score=min(duplicate_count/total_values * 5, 2),
                        remediation_suggestion=f"Review duplicate values in column '{col}'",
                        detection_date=datetime.now()
                    ))
                    uniqueness_score -= min(duplicate_count/total_values * 2, 1)
        
        return max(uniqueness_score, 0.0)
    
    def _calculate_overall_score(self, dimension_scores: Dict[QualityDimension, float]) -> float:
        """Calculate weighted overall quality score"""
        
        total_weighted_score = 0
        total_weight = 0
        
        for dimension, score in dimension_scores.items():
            weight = self.dimension_weights.get(dimension, 1.0)
            total_weighted_score += score * weight
            total_weight += weight
        
        return total_weighted_score / total_weight if total_weight > 0 else 0
    
    def _determine_quality_level(self, overall_score: float) -> QualityLevel:
        """Determine quality level based on overall score"""
        
        if overall_score >= 9.0:
            return QualityLevel.EXCELLENT
        elif overall_score >= 8.0:
            return QualityLevel.GOOD
        elif overall_score >= 6.5:
            return QualityLevel.ACCEPTABLE
        elif overall_score >= 4.0:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL
    
    def _generate_improvement_recommendations(
        self,
        dimension_scores: Dict[QualityDimension, float],
        issues: List[QualityIssue],
        business_context: Optional[Dict[str, str]]
    ) -> List[str]:
        """Generate data quality improvement recommendations"""
        
        recommendations = []
        
        # Dimension-specific recommendations
        for dimension, score in dimension_scores.items():
            if score < 7.0:
                if dimension == QualityDimension.COMPLETENESS:
                    recommendations.append("Implement data collection improvements to reduce missing values")
                elif dimension == QualityDimension.ACCURACY:
                    recommendations.append("Establish data validation rules at the source")
                elif dimension == QualityDimension.CONSISTENCY:
                    recommendations.append("Standardize data formats and naming conventions")
                elif dimension == QualityDimension.VALIDITY:
                    recommendations.append("Implement business rule validation in data pipelines")
                elif dimension == QualityDimension.TIMELINESS:
                    recommendations.append("Establish more frequent data refresh cycles")
                elif dimension == QualityDimension.UNIQUENESS:
                    recommendations.append("Implement duplicate detection and resolution processes")
        
        # Issue-specific recommendations
        critical_issues = [issue for issue in issues if issue.severity == "Critical"]
        if critical_issues:
            recommendations.append("Address critical data quality issues immediately")
        
        high_issues = [issue for issue in issues if issue.severity == "High"]
        if len(high_issues) > 3:
            recommendations.append("Develop systematic approach to resolve high-priority data issues")
        
        # General recommendations
        if len(issues) > 10:
            recommendations.append("Consider implementing automated data quality monitoring")
        
        recommendations.append("Establish data quality metrics and monitoring dashboards")
        recommendations.append("Create data stewardship roles and responsibilities")
        
        return recommendations[:8]  # Limit to top 8 recommendations
    
    def _create_data_profile(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Create comprehensive data profile"""
        
        profile = {
            'row_count': len(data),
            'column_count': len(data.columns),
            'numeric_columns': len(data.select_dtypes(include=[np.number]).columns),
            'categorical_columns': len(data.select_dtypes(include=['object']).columns),
            'missing_cells_total': data.isnull().sum().sum(),
            'missing_percentage': (data.isnull().sum().sum() / data.size) * 100,
            'duplicate_rows': data.duplicated().sum(),
            'memory_usage_mb': data.memory_usage(deep=True).sum() / 1024 / 1024
        }
        
        # Column-specific statistics
        profile['column_profiles'] = {}
        for column in data.columns:
            col_profile = {
                'data_type': str(data[column].dtype),
                'non_null_count': data[column].count(),
                'null_percentage': (data[column].isnull().sum() / len(data)) * 100,
                'unique_values': data[column].nunique()
            }
            
            if data[column].dtype in ['int64', 'float64']:
                col_profile.update({
                    'mean': data[column].mean(),
                    'std': data[column].std(),
                    'min': data[column].min(),
                    'max': data[column].max(),
                    'median': data[column].median()
                })
            
            profile['column_profiles'][column] = col_profile
        
        return profile
    
    def _analyze_quality_trends(
        self,
        dataset_name: str,
        current_scores: Dict[QualityDimension, float]
    ) -> Dict[str, float]:
        """Analyze quality trends over time"""
        
        trends = {}
        
        if dataset_name in self.quality_history:
            historical_data = self.quality_history[dataset_name]
            
            if len(historical_data) >= 2:
                # Calculate trends for each dimension
                for dimension in QualityDimension:
                    dimension_history = [entry['dimension_scores'].get(dimension, 0) 
                                       for entry in historical_data]
                    
                    if len(dimension_history) >= 2:
                        # Simple linear trend calculation
                        trend = (dimension_history[-1] - dimension_history[0]) / len(dimension_history)
                        trends[dimension.value] = trend
        
        return trends
    
    def _store_quality_history(
        self,
        dataset_name: str,
        dimension_scores: Dict[QualityDimension, float],
        overall_score: float
    ) -> None:
        """Store quality assessment history"""
        
        if dataset_name not in self.quality_history:
            self.quality_history[dataset_name] = []
        
        # Store current assessment
        self.quality_history[dataset_name].append({
            'timestamp': datetime.now(),
            'overall_score': overall_score,
            'dimension_scores': dimension_scores.copy()
        })
        
        # Keep only last 20 assessments to manage memory
        if len(self.quality_history[dataset_name]) > 20:
            self.quality_history[dataset_name] = self.quality_history[dataset_name][-20:]
    
    def _generate_enterprise_recommendations(
        self,
        summary_metrics: Dict[str, Any],
        dimension_breakdown: Dict[str, Dict[str, float]]
    ) -> List[str]:
        """Generate enterprise-level data quality recommendations"""
        
        recommendations = []
        
        if summary_metrics.get('overall_average_score', 0) < 7.0:
            recommendations.append("Implement organization-wide data quality improvement initiative")
        
        if summary_metrics.get('datasets_below_threshold', 0) > 0:
            recommendations.append("Prioritize remediation of datasets below quality threshold")
        
        if summary_metrics.get('quality_variance', 0) > 2.0:
            recommendations.append("Standardize data quality processes across all datasets")
        
        # Dimension-specific enterprise recommendations
        for dim_name, dim_stats in dimension_breakdown.items():
            if dim_stats.get('average_score', 0) < 6.5:
                recommendations.append(f"Focus improvement efforts on {dim_name} across all datasets")
        
        recommendations.append("Establish data quality governance council")
        recommendations.append("Implement automated data quality monitoring")
        
        return recommendations[:6]  # Limit to top 6 recommendations
    
    def _create_empty_data_report(self, dataset_name: str) -> QualityReport:
        """Create quality report for empty dataset"""
        
        return QualityReport(
            dataset_name=dataset_name,
            assessment_date=datetime.now(),
            overall_score=0.0,
            dimension_scores={dim: 0.0 for dim in QualityDimension},
            quality_level=QualityLevel.CRITICAL,
            issues_identified=[QualityIssue(
                issue_id=f"EMPTY_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                rule_id="GEN_001",
                dimension=QualityDimension.COMPLETENESS,
                severity="Critical",
                description="Dataset is empty",
                affected_rows=0,
                affected_columns=[],
                impact_score=10.0,
                remediation_suggestion="Load data into dataset",
                detection_date=datetime.now()
            )],
            improvement_recommendations=["Load data into the dataset"],
            data_profile={'row_count': 0, 'column_count': 0},
            trend_analysis={}
        )
    
    def _initialize_quality_rules(self) -> List[QualityRule]:
        """Initialize standard data quality rules"""
        
        return [
            QualityRule(
                rule_id="COMP_001",
                name="Missing Value Check",
                dimension=QualityDimension.COMPLETENESS,
                description="Check for missing values in critical columns",
                validation_function="check_missing_values",
                threshold=0.1,
                severity="High",
                columns=["all"],
                business_impact="Incomplete data affects analysis accuracy"
            ),
            QualityRule(
                rule_id="ACC_001",
                name="Outlier Detection",
                dimension=QualityDimension.ACCURACY,
                description="Detect statistical outliers in numeric columns",
                validation_function="check_outliers",
                threshold=3.0,
                severity="Medium",
                columns=["numeric"],
                business_impact="Outliers may indicate data errors"
            ),
            QualityRule(
                rule_id="VAL_001",
                name="Range Validation",
                dimension=QualityDimension.VALIDITY,
                description="Validate values are within expected ranges",
                validation_function="check_ranges",
                threshold=0.0,
                severity="High",
                columns=["adoption_rate", "roi"],
                business_impact="Invalid ranges compromise data reliability"
            )
        ]
    
    def _get_dimension_weights(self) -> Dict[QualityDimension, float]:
        """Get weights for different quality dimensions"""
        
        return {
            QualityDimension.COMPLETENESS: 1.2,
            QualityDimension.ACCURACY: 1.3,
            QualityDimension.CONSISTENCY: 1.0,
            QualityDimension.VALIDITY: 1.1,
            QualityDimension.TIMELINESS: 0.9,
            QualityDimension.UNIQUENESS: 0.8
        }

# Global data quality engine instance
quality_engine = DataQualityEngine()

# Export functions
__all__ = [
    'QualityDimension',
    'QualityLevel',
    'QualityRule',
    'QualityIssue',
    'QualityReport',
    'DataQualityEngine',
    'quality_engine'
]