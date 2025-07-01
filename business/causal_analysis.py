"""
Causal Analysis Engine for AI Adoption Dashboard
Integrates McKinsey CausalNex for establishing causal relationships between AI adoption and productivity
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

# CausalNex imports for causal reasoning
try:
    from causalnex.structure import StructureModel
    from causalnex.structure.notears import from_pandas
    from causalnex.network import BayesianNetwork
    from causalnex.inference import InferenceEngine
    from causalnx.discretiser import Discretiser
    CAUSALNEX_AVAILABLE = True
except ImportError:
    CAUSALNEX_AVAILABLE = False
    logging.warning("CausalNex not available. Install with: pip install causalnex")

logger = logging.getLogger(__name__)

class CausalRelationType(Enum):
    DIRECT = "Direct"
    INDIRECT = "Indirect"
    BIDIRECTIONAL = "Bidirectional"
    CONDITIONAL = "Conditional"

class ProductivityMetric(Enum):
    REVENUE_PER_EMPLOYEE = "Revenue per Employee"
    OPERATIONAL_EFFICIENCY = "Operational Efficiency"
    COST_REDUCTION = "Cost Reduction"
    TIME_TO_MARKET = "Time to Market"
    CUSTOMER_SATISFACTION = "Customer Satisfaction"
    INNOVATION_INDEX = "Innovation Index"

@dataclass
class CausalRelationship:
    """Represents a causal relationship between variables"""
    cause: str
    effect: str
    relationship_type: CausalRelationType
    strength: float  # 0-1, strength of causal relationship
    confidence: float  # 0-1, statistical confidence
    impact_direction: str  # "positive", "negative", "neutral"
    evidence_sources: List[str]
    discovery_method: str

@dataclass
class ProductivityImpact:
    """Quantifies productivity impact from AI adoption"""
    metric: ProductivityMetric
    baseline_value: float
    post_ai_value: float
    improvement_percentage: float
    causal_confidence: float
    contributing_factors: List[str]
    measurement_period: str
    sector: str

@dataclass
class CausalAnalysisResult:
    """Results from causal analysis"""
    analysis_id: str
    analysis_date: datetime
    data_sources: List[str]
    causal_relationships: List[CausalRelationship]
    productivity_impacts: List[ProductivityImpact]
    intervention_recommendations: List[str]
    confidence_score: float
    model_quality_metrics: Dict[str, float]

class CausalAnalysisEngine:
    """
    Advanced causal analysis engine using McKinsey CausalNex
    Establishes causal relationships between AI adoption and productivity outcomes
    """
    
    def __init__(self):
        self.causal_models = {}
        self.trained_networks = {}
        self.historical_analyses = []
        self.intervention_cache = {}
        
        if not CAUSALNEX_AVAILABLE:
            logger.warning("CausalNex not available. Causal analysis will use statistical approximations.")
    
    def establish_ai_productivity_causality(
        self,
        adoption_data: pd.DataFrame,
        productivity_data: pd.DataFrame,
        sector: str = "all_sectors",
        time_window: str = "2020-2024"
    ) -> CausalAnalysisResult:
        """
        Establish causal relationships between AI adoption and productivity gains
        """
        
        analysis_id = f"causal_analysis_{sector}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Merge and prepare data for causal analysis
            merged_data = self._prepare_causal_dataset(adoption_data, productivity_data, sector)
            
            if CAUSALNEX_AVAILABLE:
                # Use CausalNex for rigorous causal discovery
                causal_relationships = self._discover_causal_structure_causalnx(merged_data, analysis_id)
                productivity_impacts = self._quantify_productivity_impacts_causalnx(merged_data, causal_relationships)
                intervention_recommendations = self._generate_intervention_recommendations_causalnx(
                    merged_data, causal_relationships
                )
                confidence_score = self._calculate_model_confidence_causalnx(merged_data)
                
            else:
                # Fallback to statistical correlation analysis
                causal_relationships = self._discover_causal_structure_statistical(merged_data)
                productivity_impacts = self._quantify_productivity_impacts_statistical(merged_data)
                intervention_recommendations = self._generate_basic_intervention_recommendations(merged_data)
                confidence_score = 0.7  # Lower confidence for statistical methods
            
            # Create comprehensive analysis result
            result = CausalAnalysisResult(
                analysis_id=analysis_id,
                analysis_date=datetime.now(),
                data_sources=[f"AI Adoption Data ({sector})", f"Productivity Data ({sector})"],
                causal_relationships=causal_relationships,
                productivity_impacts=productivity_impacts,
                intervention_recommendations=intervention_recommendations,
                confidence_score=confidence_score,
                model_quality_metrics=self._calculate_quality_metrics(merged_data)
            )
            
            # Store analysis for future reference
            self.historical_analyses.append(result)
            
            logger.info(f"Completed causal analysis for {sector}: {len(causal_relationships)} relationships identified")
            return result
            
        except Exception as e:
            logger.error(f"Error in causal analysis: {e}")
            return self._create_fallback_analysis_result(analysis_id, sector)
    
    def predict_intervention_impact(
        self,
        intervention: Dict[str, float],
        target_metrics: List[ProductivityMetric],
        sector: str = "technology"
    ) -> Dict[str, Any]:
        """
        Predict the impact of specific AI adoption interventions
        """
        
        prediction_id = f"intervention_prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            if CAUSALNEX_AVAILABLE and sector in self.trained_networks:
                # Use trained Bayesian network for intervention prediction
                network = self.trained_networks[sector]
                inference_engine = InferenceEngine(network)
                
                # Set intervention values
                predictions = {}
                for variable, value in intervention.items():
                    # Query network for impact on target metrics
                    for metric in target_metrics:
                        metric_var = f"{metric.value.lower().replace(' ', '_')}"
                        if metric_var in network.nodes:
                            # Perform intervention and predict outcome
                            result = inference_engine.query(
                                variables=[metric_var],
                                evidence={variable: value}
                            )
                            predictions[metric.value] = self._interpret_prediction_result(result)
                
                confidence = 0.85  # High confidence with CausalNex
                
            else:
                # Fallback statistical prediction
                predictions = self._predict_intervention_statistical(intervention, target_metrics, sector)
                confidence = 0.65  # Lower confidence for statistical methods
            
            return {
                'prediction_id': prediction_id,
                'intervention': intervention,
                'predicted_impacts': predictions,
                'confidence_level': confidence,
                'prediction_date': datetime.now(),
                'methodology': 'CausalNex Bayesian Network' if CAUSALNEX_AVAILABLE else 'Statistical Correlation'
            }
            
        except Exception as e:
            logger.error(f"Error predicting intervention impact: {e}")
            return self._create_fallback_prediction(prediction_id, intervention, target_metrics)
    
    def generate_causal_insights_for_executives(
        self,
        analysis_result: CausalAnalysisResult,
        focus_areas: List[str] = None
    ) -> Dict[str, Any]:
        """
        Generate executive-level insights from causal analysis
        """
        
        if focus_areas is None:
            focus_areas = ["roi_optimization", "risk_mitigation", "competitive_advantage"]
        
        insights = {
            'executive_summary': self._create_executive_summary(analysis_result),
            'key_causal_drivers': self._identify_key_drivers(analysis_result),
            'intervention_priorities': self._rank_intervention_priorities(analysis_result),
            'productivity_opportunities': self._identify_productivity_opportunities(analysis_result),
            'risk_assessment': self._assess_causal_risks(analysis_result),
            'competitive_implications': self._analyze_competitive_implications(analysis_result),
            'recommended_actions': self._generate_executive_actions(analysis_result, focus_areas)
        }
        
        return insights
    
    def create_what_if_scenarios(
        self,
        base_scenario: Dict[str, float],
        variable_ranges: Dict[str, Tuple[float, float]],
        num_scenarios: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Create what-if scenarios for AI adoption decisions
        """
        
        scenarios = []
        
        for i in range(num_scenarios):
            scenario = base_scenario.copy()
            scenario_id = f"scenario_{i+1:03d}"
            
            # Vary each variable within specified ranges
            for variable, (min_val, max_val) in variable_ranges.items():
                if variable in scenario:
                    # Use normal distribution around base value
                    base_val = base_scenario[variable]
                    std_dev = (max_val - min_val) / 6  # 99.7% within range
                    new_val = np.clip(np.random.normal(base_val, std_dev), min_val, max_val)
                    scenario[variable] = new_val
            
            # Predict outcomes for this scenario
            if CAUSALNEX_AVAILABLE:
                predicted_outcomes = self._predict_scenario_outcomes_causalnx(scenario)
            else:
                predicted_outcomes = self._predict_scenario_outcomes_statistical(scenario)
            
            scenarios.append({
                'scenario_id': scenario_id,
                'input_variables': scenario,
                'predicted_outcomes': predicted_outcomes,
                'scenario_score': self._calculate_scenario_score(predicted_outcomes),
                'risk_level': self._assess_scenario_risk(scenario, predicted_outcomes)
            })
        
        # Sort scenarios by score
        scenarios.sort(key=lambda x: x['scenario_score'], reverse=True)
        
        return scenarios
    
    def _prepare_causal_dataset(
        self,
        adoption_data: pd.DataFrame,
        productivity_data: pd.DataFrame,
        sector: str
    ) -> pd.DataFrame:
        """Prepare merged dataset for causal analysis"""
        
        # Filter by sector if specified
        if sector != "all_sectors" and 'sector' in adoption_data.columns:
            adoption_data = adoption_data[adoption_data['sector'] == sector]
        if sector != "all_sectors" and 'sector' in productivity_data.columns:
            productivity_data = productivity_data[productivity_data['sector'] == sector]
        
        # Merge datasets on common keys
        merge_keys = ['year', 'sector'] if 'sector' in adoption_data.columns and 'sector' in productivity_data.columns else ['year']
        if 'organization' in adoption_data.columns and 'organization' in productivity_data.columns:
            merge_keys.append('organization')
        
        merged = pd.merge(adoption_data, productivity_data, on=merge_keys, how='inner', suffixes=('_adoption', '_productivity'))
        
        # Create derived variables for causal analysis
        if 'adoption_rate' in merged.columns and 'revenue_per_employee' in merged.columns:
            merged['ai_maturity_score'] = merged['adoption_rate'] * 0.4 + \
                                        merged.get('investment_amount', 0) * 0.3 + \
                                        merged.get('implementation_timeline', 12) * -0.3
            
            merged['productivity_index'] = (
                merged['revenue_per_employee'] * 0.3 +
                merged.get('operational_efficiency', 100) * 0.3 +
                merged.get('cost_reduction_percentage', 0) * 0.4
            )
        
        # Handle missing values
        numeric_columns = merged.select_dtypes(include=[np.number]).columns
        merged[numeric_columns] = merged[numeric_columns].fillna(merged[numeric_columns].median())
        
        return merged
    
    def _discover_causal_structure_causalnx(
        self,
        data: pd.DataFrame,
        analysis_id: str
    ) -> List[CausalRelationship]:
        """Use CausalNex to discover causal structure"""
        
        # Select relevant variables for causal discovery
        causal_vars = self._select_causal_variables(data)
        causal_data = data[causal_vars].copy()
        
        # Learn structure using NOTEARS algorithm
        structure_model = from_pandas(causal_data, alpha=0.1)
        
        # Create Bayesian Network
        bayesian_network = BayesianNetwork(structure_model)
        
        # Discretize continuous variables for Bayesian Network
        discretiser = Discretiser(method="fixed", numeric_split_points=[0.25, 0.5, 0.75])
        causal_data_discrete = discretiser.transform(causal_data)
        
        # Fit network parameters
        bayesian_network = bayesian_network.fit_node_states_and_cpds(causal_data_discrete)
        
        # Store trained network for future use
        sector = data.get('sector', ['general']).iloc[0] if 'sector' in data.columns else 'general'
        self.trained_networks[sector] = bayesian_network
        
        # Extract causal relationships
        relationships = []
        for parent, child in structure_model.edges:
            strength = abs(structure_model[parent][child]['weight']) if 'weight' in structure_model[parent][child] else 0.5
            
            relationships.append(CausalRelationship(
                cause=parent,
                effect=child,
                relationship_type=CausalRelationType.DIRECT,
                strength=min(strength, 1.0),
                confidence=0.8,  # High confidence with CausalNx
                impact_direction="positive" if strength > 0 else "negative",
                evidence_sources=[f"CausalNX Structure Learning - {analysis_id}"],
                discovery_method="NOTEARS Algorithm"
            ))
        
        return relationships
    
    def _discover_causal_structure_statistical(self, data: pd.DataFrame) -> List[CausalRelationship]:
        """Fallback statistical approach for causal discovery"""
        
        relationships = []
        
        # Define known AI adoption → productivity relationships based on literature
        ai_variables = [col for col in data.columns if any(term in col.lower() for term in ['adoption', 'ai', 'automation', 'digital'])]
        productivity_variables = [col for col in data.columns if any(term in col.lower() for term in ['revenue', 'efficiency', 'productivity', 'roi'])]
        
        for ai_var in ai_variables:
            for prod_var in productivity_variables:
                if ai_var in data.columns and prod_var in data.columns:
                    # Calculate correlation as proxy for causal strength
                    correlation = data[ai_var].corr(data[prod_var])
                    
                    if abs(correlation) > 0.3:  # Moderate correlation threshold
                        relationships.append(CausalRelationship(
                            cause=ai_var,
                            effect=prod_var,
                            relationship_type=CausalRelationType.DIRECT,
                            strength=abs(correlation),
                            confidence=0.6,  # Lower confidence for correlation
                            impact_direction="positive" if correlation > 0 else "negative",
                            evidence_sources=["Statistical Correlation Analysis"],
                            discovery_method="Pearson Correlation"
                        ))
        
        return relationships
    
    def _quantify_productivity_impacts_causalnx(
        self,
        data: pd.DataFrame,
        relationships: List[CausalRelationship]
    ) -> List[ProductivityImpact]:
        """Quantify productivity impacts using causal relationships"""
        
        impacts = []
        
        # Map productivity metrics to data columns
        metric_mapping = {
            ProductivityMetric.REVENUE_PER_EMPLOYEE: ['revenue_per_employee', 'revenue_employee'],
            ProductivityMetric.OPERATIONAL_EFFICIENCY: ['operational_efficiency', 'efficiency_score'],
            ProductivityMetric.COST_REDUCTION: ['cost_reduction', 'cost_savings'],
            ProductivityMetric.TIME_TO_MARKET: ['time_to_market', 'development_speed'],
            ProductivityMetric.CUSTOMER_SATISFACTION: ['customer_satisfaction', 'satisfaction_score'],
            ProductivityMetric.INNOVATION_INDEX: ['innovation_index', 'innovation_score']
        }
        
        for metric, possible_columns in metric_mapping.items():
            # Find matching column in data
            data_column = None
            for col in possible_columns:
                if col in data.columns:
                    data_column = col
                    break
            
            if data_column and not data[data_column].empty:
                # Calculate productivity impact
                baseline = data[data_column].quantile(0.25)  # 25th percentile as baseline
                post_ai = data[data_column].quantile(0.75)   # 75th percentile as AI-enhanced
                
                if baseline > 0:
                    improvement = ((post_ai - baseline) / baseline) * 100
                    
                    # Find contributing causal factors
                    contributing_factors = [
                        rel.cause for rel in relationships 
                        if rel.effect == data_column and rel.strength > 0.5
                    ]
                    
                    impacts.append(ProductivityImpact(
                        metric=metric,
                        baseline_value=baseline,
                        post_ai_value=post_ai,
                        improvement_percentage=improvement,
                        causal_confidence=0.8,
                        contributing_factors=contributing_factors or ["AI Adoption"],
                        measurement_period="Historical Analysis",
                        sector=data.get('sector', pd.Series(['General'])).iloc[0] if 'sector' in data.columns else 'General'
                    ))
        
        return impacts
    
    def _quantify_productivity_impacts_statistical(self, data: pd.DataFrame) -> List[ProductivityImpact]:
        """Fallback statistical approach for productivity impact quantification"""
        
        impacts = []
        
        # Simple statistical analysis of productivity improvements
        if 'adoption_rate' in data.columns and 'revenue_per_employee' in data.columns:
            # Split data into high vs low AI adoption
            high_adoption = data[data['adoption_rate'] > data['adoption_rate'].median()]
            low_adoption = data[data['adoption_rate'] <= data['adoption_rate'].median()]
            
            if not high_adoption.empty and not low_adoption.empty:
                baseline_revenue = low_adoption['revenue_per_employee'].mean()
                enhanced_revenue = high_adoption['revenue_per_employee'].mean()
                
                if baseline_revenue > 0:
                    improvement = ((enhanced_revenue - baseline_revenue) / baseline_revenue) * 100
                    
                    impacts.append(ProductivityImpact(
                        metric=ProductivityMetric.REVENUE_PER_EMPLOYEE,
                        baseline_value=baseline_revenue,
                        post_ai_value=enhanced_revenue,
                        improvement_percentage=improvement,
                        causal_confidence=0.6,
                        contributing_factors=["AI Adoption Rate"],
                        measurement_period="Comparative Analysis",
                        sector="Statistical Analysis"
                    ))
        
        return impacts
    
    def _generate_intervention_recommendations_causalnx(
        self,
        data: pd.DataFrame,
        relationships: List[CausalRelationship]
    ) -> List[str]:
        """Generate intervention recommendations based on causal analysis"""
        
        recommendations = []
        
        # Find highest-impact causal drivers
        high_impact_causes = [
            rel.cause for rel in relationships 
            if rel.strength > 0.7 and rel.impact_direction == "positive"
        ]
        
        for cause in high_impact_causes[:5]:  # Top 5 recommendations
            if 'adoption' in cause.lower():
                recommendations.append(f"Increase {cause} - High causal impact identified (strength: {max(rel.strength for rel in relationships if rel.cause == cause):.2f})")
            elif 'investment' in cause.lower():
                recommendations.append(f"Optimize {cause} allocation - Strong productivity correlation identified")
            elif 'training' in cause.lower():
                recommendations.append(f"Enhance {cause} programs - Direct causal link to performance improvements")
        
        # Add general recommendations
        recommendations.extend([
            "Implement systematic AI adoption measurement and tracking",
            "Establish causal monitoring dashboards for intervention effectiveness",
            "Create feedback loops between productivity metrics and AI initiatives"
        ])
        
        return recommendations[:8]  # Limit to top 8 recommendations
    
    def _generate_basic_intervention_recommendations(self, data: pd.DataFrame) -> List[str]:
        """Generate basic intervention recommendations without causal analysis"""
        
        return [
            "Increase AI adoption rates systematically across organization",
            "Focus on high-ROI AI implementation areas",
            "Establish productivity measurement frameworks",
            "Create AI training and capability development programs",
            "Implement data-driven decision making processes",
            "Monitor and measure AI intervention effectiveness"
        ]
    
    def _calculate_model_confidence_causalnx(self, data: pd.DataFrame) -> float:
        """Calculate confidence score for CausalNx model"""
        
        # Factors affecting confidence
        sample_size_score = min(len(data) / 1000, 1.0)  # Prefer larger samples
        data_quality_score = 1.0 - (data.isnull().sum().sum() / data.size)  # Penalize missing data
        variable_coverage_score = min(len(data.columns) / 20, 1.0)  # Prefer more variables
        
        # Weighted confidence score
        confidence = (
            sample_size_score * 0.4 +
            data_quality_score * 0.4 +
            variable_coverage_score * 0.2
        )
        
        return max(min(confidence, 1.0), 0.5)  # Clamp between 0.5 and 1.0
    
    def _calculate_quality_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """Calculate model quality metrics"""
        
        return {
            'data_completeness': 1.0 - (data.isnull().sum().sum() / data.size),
            'sample_size': len(data),
            'variable_count': len(data.columns),
            'numeric_variable_ratio': len(data.select_dtypes(include=[np.number]).columns) / len(data.columns),
            'temporal_coverage': data['year'].nunique() if 'year' in data.columns else 1
        }
    
    def _select_causal_variables(self, data: pd.DataFrame) -> List[str]:
        """Select relevant variables for causal analysis"""
        
        # Prioritize AI adoption and productivity variables
        priority_terms = ['adoption', 'ai', 'revenue', 'efficiency', 'productivity', 'roi', 'investment', 'cost']
        
        selected_vars = []
        for col in data.columns:
            if any(term in col.lower() for term in priority_terms):
                selected_vars.append(col)
        
        # Add other numeric variables
        numeric_vars = data.select_dtypes(include=[np.number]).columns.tolist()
        for var in numeric_vars:
            if var not in selected_vars and len(selected_vars) < 15:  # Limit complexity
                selected_vars.append(var)
        
        return selected_vars[:15]  # Maximum 15 variables for computational efficiency
    
    def _create_fallback_analysis_result(self, analysis_id: str, sector: str) -> CausalAnalysisResult:
        """Create fallback analysis result when errors occur"""
        
        return CausalAnalysisResult(
            analysis_id=analysis_id,
            analysis_date=datetime.now(),
            data_sources=[f"Error in analysis for {sector}"],
            causal_relationships=[],
            productivity_impacts=[],
            intervention_recommendations=["Unable to complete causal analysis - check data quality"],
            confidence_score=0.0,
            model_quality_metrics={}
        )
    
    def _create_executive_summary(self, result: CausalAnalysisResult) -> str:
        """Create executive summary of causal analysis"""
        
        if not result.causal_relationships:
            return "Causal analysis could not identify significant relationships in the provided data."
        
        strong_relationships = [rel for rel in result.causal_relationships if rel.strength > 0.6]
        avg_productivity_improvement = np.mean([impact.improvement_percentage for impact in result.productivity_impacts]) if result.productivity_impacts else 0
        
        summary = f"""
        Causal Analysis Summary:
        • Identified {len(result.causal_relationships)} causal relationships ({len(strong_relationships)} high-confidence)
        • Average productivity improvement: {avg_productivity_improvement:.1f}%
        • Model confidence: {result.confidence_score:.1%}
        • Key insight: {result.intervention_recommendations[0] if result.intervention_recommendations else 'No specific insights available'}
        """
        
        return summary.strip()
    
    def _identify_key_drivers(self, result: CausalAnalysisResult) -> List[Dict[str, Any]]:
        """Identify key causal drivers from analysis"""
        
        drivers = []
        for rel in sorted(result.causal_relationships, key=lambda x: x.strength, reverse=True)[:5]:
            drivers.append({
                'driver': rel.cause,
                'impact_area': rel.effect,
                'strength': rel.strength,
                'direction': rel.impact_direction,
                'confidence': rel.confidence
            })
        
        return drivers
    
    def _rank_intervention_priorities(self, result: CausalAnalysisResult) -> List[Dict[str, Any]]:
        """Rank intervention priorities based on causal analysis"""
        
        priorities = []
        
        # Group relationships by cause to identify high-impact interventions
        cause_impacts = {}
        for rel in result.causal_relationships:
            if rel.cause not in cause_impacts:
                cause_impacts[rel.cause] = []
            cause_impacts[rel.cause].append(rel)
        
        # Calculate total impact score for each cause
        for cause, relationships in cause_impacts.items():
            total_impact = sum(rel.strength for rel in relationships if rel.impact_direction == "positive")
            avg_confidence = np.mean([rel.confidence for rel in relationships])
            
            priorities.append({
                'intervention': cause,
                'total_impact_score': total_impact,
                'confidence': avg_confidence,
                'affected_outcomes': [rel.effect for rel in relationships],
                'priority_rank': None  # Will be set after sorting
            })
        
        # Sort by impact score and assign ranks
        priorities.sort(key=lambda x: x['total_impact_score'], reverse=True)
        for i, priority in enumerate(priorities):
            priority['priority_rank'] = i + 1
        
        return priorities[:10]  # Top 10 priorities
    
    def _identify_productivity_opportunities(self, result: CausalAnalysisResult) -> List[Dict[str, Any]]:
        """Identify productivity improvement opportunities"""
        
        opportunities = []
        for impact in sorted(result.productivity_impacts, key=lambda x: x.improvement_percentage, reverse=True):
            opportunities.append({
                'metric': impact.metric.value,
                'current_improvement': f"{impact.improvement_percentage:.1f}%",
                'potential_additional_gain': f"{impact.improvement_percentage * 0.5:.1f}%",  # Estimated additional potential
                'confidence': impact.causal_confidence,
                'key_drivers': impact.contributing_factors
            })
        
        return opportunities
    
    def _assess_causal_risks(self, result: CausalAnalysisResult) -> Dict[str, Any]:
        """Assess risks based on causal analysis"""
        
        risks = {
            'model_uncertainty': 1.0 - result.confidence_score,
            'data_limitations': [],
            'causal_assumptions': [],
            'intervention_risks': []
        }
        
        # Identify potential risks
        if result.confidence_score < 0.7:
            risks['data_limitations'].append("Insufficient data for high-confidence causal inference")
        
        negative_relationships = [rel for rel in result.causal_relationships if rel.impact_direction == "negative"]
        if negative_relationships:
            risks['intervention_risks'].extend([
                f"Increasing {rel.cause} may negatively impact {rel.effect}" for rel in negative_relationships[:3]
            ])
        
        return risks
    
    def _analyze_competitive_implications(self, result: CausalAnalysisResult) -> Dict[str, Any]:
        """Analyze competitive implications of causal findings"""
        
        implications = {
            'competitive_advantages': [],
            'market_opportunities': [],
            'strategic_recommendations': []
        }
        
        # Identify competitive advantages from strong positive relationships
        strong_positive = [rel for rel in result.causal_relationships 
                          if rel.strength > 0.7 and rel.impact_direction == "positive"]
        
        for rel in strong_positive[:3]:
            implications['competitive_advantages'].append(
                f"Strong causal link: {rel.cause} → {rel.effect} (strength: {rel.strength:.2f})"
            )
        
        # Generate strategic recommendations
        if result.productivity_impacts:
            best_impact = max(result.productivity_impacts, key=lambda x: x.improvement_percentage)
            implications['strategic_recommendations'].append(
                f"Focus on {best_impact.metric.value} - showing {best_impact.improvement_percentage:.1f}% improvement potential"
            )
        
        return implications
    
    def _generate_executive_actions(self, result: CausalAnalysisResult, focus_areas: List[str]) -> List[str]:
        """Generate executive action items based on causal analysis"""
        
        actions = []
        
        # High-priority actions based on causal findings
        if result.intervention_recommendations:
            actions.extend(result.intervention_recommendations[:3])
        
        # Focus area specific actions
        if "roi_optimization" in focus_areas and result.productivity_impacts:
            best_roi_metric = max(result.productivity_impacts, key=lambda x: x.improvement_percentage)
            actions.append(f"Prioritize initiatives targeting {best_roi_metric.metric.value} for maximum ROI")
        
        if "risk_mitigation" in focus_areas:
            actions.append("Establish causal monitoring system to track intervention effectiveness")
        
        if "competitive_advantage" in focus_areas:
            actions.append("Leverage identified causal advantages for strategic differentiation")
        
        return actions[:8]  # Limit to 8 actionable items
    
    # Additional helper methods for scenario analysis and prediction
    def _predict_scenario_outcomes_causalnx(self, scenario: Dict[str, float]) -> Dict[str, float]:
        """Predict scenario outcomes using CausalNex"""
        # Implementation would use trained Bayesian networks
        # For now, return placeholder implementation
        return {
            'predicted_roi': scenario.get('adoption_rate', 50) * 0.8,
            'predicted_productivity_gain': scenario.get('investment_amount', 100000) * 0.0001,
            'predicted_risk_score': max(0, 100 - scenario.get('implementation_timeline', 12) * 5)
        }
    
    def _predict_scenario_outcomes_statistical(self, scenario: Dict[str, float]) -> Dict[str, float]:
        """Predict scenario outcomes using statistical methods"""
        return {
            'predicted_roi': scenario.get('adoption_rate', 50) * 0.6,  # Lower confidence
            'predicted_productivity_gain': scenario.get('investment_amount', 100000) * 0.00008,
            'predicted_risk_score': max(0, 80 - scenario.get('implementation_timeline', 12) * 4)
        }
    
    def _calculate_scenario_score(self, outcomes: Dict[str, float]) -> float:
        """Calculate overall score for a scenario"""
        roi_score = min(outcomes.get('predicted_roi', 0) / 100, 1.0)
        productivity_score = min(outcomes.get('predicted_productivity_gain', 0) / 50, 1.0)
        risk_penalty = outcomes.get('predicted_risk_score', 0) / 100
        
        return (roi_score * 0.4 + productivity_score * 0.4 - risk_penalty * 0.2) * 100
    
    def _assess_scenario_risk(self, scenario: Dict[str, float], outcomes: Dict[str, float]) -> str:
        """Assess risk level for a scenario"""
        risk_score = outcomes.get('predicted_risk_score', 50)
        
        if risk_score > 70:
            return "High Risk"
        elif risk_score > 40:
            return "Medium Risk"
        else:
            return "Low Risk"
    
    def _predict_intervention_statistical(
        self,
        intervention: Dict[str, float],
        target_metrics: List[ProductivityMetric],
        sector: str
    ) -> Dict[str, Any]:
        """Statistical fallback for intervention prediction"""
        
        predictions = {}
        for metric in target_metrics:
            # Simple statistical estimation based on intervention magnitude
            intervention_magnitude = sum(intervention.values()) / len(intervention) if intervention else 0
            base_improvement = intervention_magnitude * 0.01  # 1% improvement per unit intervention
            
            predictions[metric.value] = {
                'expected_improvement': f"{base_improvement:.1f}%",
                'confidence_interval': f"{base_improvement*0.5:.1f}% - {base_improvement*1.5:.1f}%",
                'time_to_impact': "6-12 months"
            }
        
        return predictions
    
    def _create_fallback_prediction(
        self,
        prediction_id: str,
        intervention: Dict[str, float],
        target_metrics: List[ProductivityMetric]
    ) -> Dict[str, Any]:
        """Create fallback prediction when errors occur"""
        
        return {
            'prediction_id': prediction_id,
            'intervention': intervention,
            'predicted_impacts': {"error": "Unable to predict intervention impact"},
            'confidence_level': 0.0,
            'prediction_date': datetime.now(),
            'methodology': 'Error - Analysis Failed'
        }
    
    def _interpret_prediction_result(self, result: Any) -> Dict[str, Any]:
        """Interpret CausalNex prediction results"""
        # This would interpret actual CausalNx results
        # For now, return placeholder
        return {
            'probability_distribution': "See detailed analysis",
            'expected_value': "Calculated from Bayesian inference",
            'confidence_interval': "Based on network uncertainty"
        }


# Global causal analysis engine instance
causal_engine = CausalAnalysisEngine()

# Export functions and classes
__all__ = [
    'CausalRelationType',
    'ProductivityMetric', 
    'CausalRelationship',
    'ProductivityImpact',
    'CausalAnalysisResult',
    'CausalAnalysisEngine',
    'causal_engine'
]