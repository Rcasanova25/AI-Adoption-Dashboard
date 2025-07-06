"""Advanced scenario analysis engine for AI adoption planning.

This module provides Monte Carlo simulation, sensitivity analysis,
and S-curve adoption modeling for sophisticated scenario planning.
"""

import logging
from typing import Dict, List, Tuple, Optional, Callable
import numpy as np
import pandas as pd
from scipy import stats
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ScenarioVariable:
    """Definition of a variable for scenario analysis."""
    name: str
    base_value: float
    min_value: float
    max_value: float
    distribution: str = 'normal'  # 'normal', 'uniform', 'triangular'
    std_dev: Optional[float] = None  # For normal distribution
    mode: Optional[float] = None  # For triangular distribution


def monte_carlo_simulation(
    base_case: Dict[str, float],
    variables: List[ScenarioVariable],
    model_function: Callable,
    iterations: int = 10000,
    confidence_levels: List[float] = [0.05, 0.25, 0.50, 0.75, 0.95]
) -> Dict:
    """
    Run Monte Carlo simulation for scenario analysis.
    
    Args:
        base_case: Base case values for all parameters
        variables: List of variables to vary in simulation
        model_function: Function that takes parameters and returns result
        iterations: Number of simulation iterations
        confidence_levels: Percentiles to calculate
        
    Returns:
        Dictionary with simulation results and statistics
    """
    results = []
    variable_samples = {var.name: [] for var in variables}
    
    for i in range(iterations):
        # Generate random values for each variable
        scenario = base_case.copy()
        
        for var in variables:
            if var.distribution == 'normal':
                # Use std_dev if provided, otherwise use range/4 as approximation
                std = var.std_dev or (var.max_value - var.min_value) / 4
                value = np.random.normal(var.base_value, std)
                # Clip to bounds
                value = np.clip(value, var.min_value, var.max_value)
                
            elif var.distribution == 'uniform':
                value = np.random.uniform(var.min_value, var.max_value)
                
            elif var.distribution == 'triangular':
                mode = var.mode or var.base_value
                value = np.random.triangular(var.min_value, mode, var.max_value)
                
            else:
                value = var.base_value
            
            scenario[var.name] = value
            variable_samples[var.name].append(value)
        
        # Run model with scenario parameters
        try:
            result = model_function(**scenario)
            results.append(result)
        except Exception as e:
            logger.warning(f"Simulation iteration {i} failed: {e}")
            continue
    
    # Calculate statistics
    results_array = np.array(results)
    percentiles = np.percentile(results_array, [cl * 100 for cl in confidence_levels])
    
    # Calculate correlations between inputs and output
    correlations = {}
    for var in variables:
        if len(variable_samples[var.name]) == len(results):
            correlation, p_value = stats.pearsonr(variable_samples[var.name], results)
            correlations[var.name] = {
                'correlation': correlation,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
    
    return {
        'iterations': len(results),
        'mean': np.mean(results_array),
        'std_dev': np.std(results_array),
        'min': np.min(results_array),
        'max': np.max(results_array),
        'percentiles': dict(zip([f'p{int(cl*100)}' for cl in confidence_levels], percentiles)),
        'confidence_interval_90': (percentiles[0], percentiles[-1]),
        'coefficient_of_variation': np.std(results_array) / np.mean(results_array) if np.mean(results_array) != 0 else np.inf,
        'correlations': correlations,
        'histogram_data': {
            'values': results,
            'bins': np.histogram(results_array, bins=50)[1].tolist()
        }
    }


def sensitivity_analysis(
    base_case: Dict[str, float],
    variables: List[str],
    model_function: Callable,
    variation_pct: float = 0.20,
    steps: int = 5
) -> Dict:
    """
    Perform sensitivity analysis on model parameters.
    
    Args:
        base_case: Base case parameter values
        variables: List of variable names to analyze
        model_function: Function to evaluate
        variation_pct: Percentage to vary each parameter (±)
        steps: Number of steps in each direction
        
    Returns:
        Dictionary with sensitivity analysis results
    """
    base_result = model_function(**base_case)
    results = {'base_result': base_result}
    
    for var in variables:
        if var not in base_case:
            logger.warning(f"Variable {var} not in base case")
            continue
            
        base_value = base_case[var]
        var_results = []
        
        # Create range of values
        multipliers = np.linspace(1 - variation_pct, 1 + variation_pct, steps * 2 + 1)
        
        for multiplier in multipliers:
            scenario = base_case.copy()
            scenario[var] = base_value * multiplier
            
            try:
                result = model_function(**scenario)
                var_results.append({
                    'value': scenario[var],
                    'multiplier': multiplier,
                    'result': result,
                    'pct_change_input': (multiplier - 1) * 100,
                    'pct_change_output': ((result - base_result) / base_result * 100) if base_result != 0 else 0
                })
            except Exception as e:
                logger.warning(f"Sensitivity analysis failed for {var} at {multiplier}: {e}")
                
        # Calculate sensitivity metric (elasticity)
        if len(var_results) >= 2:
            # Use linear regression to estimate sensitivity
            x_values = [r['pct_change_input'] for r in var_results]
            y_values = [r['pct_change_output'] for r in var_results]
            
            if len(set(x_values)) > 1:  # Ensure we have variation
                slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
                elasticity = slope
            else:
                elasticity = 0
        else:
            elasticity = 0
            
        results[var] = {
            'values': var_results,
            'elasticity': elasticity,  # % change in output per % change in input
            'sensitivity_rank': abs(elasticity)
        }
    
    # Rank variables by sensitivity
    sensitivity_ranking = sorted(
        [(var, data['sensitivity_rank']) for var, data in results.items() if var != 'base_result'],
        key=lambda x: x[1],
        reverse=True
    )
    
    results['sensitivity_ranking'] = sensitivity_ranking
    
    return results


def adoption_s_curve(
    time_periods: int,
    max_adoption: float = 100.0,
    inflection_point: int = None,
    steepness: float = 0.5
) -> List[float]:
    """
    Generate S-curve adoption pattern using logistic function.
    
    Args:
        time_periods: Number of time periods to model
        max_adoption: Maximum adoption percentage
        inflection_point: Period where adoption rate is highest (default: middle)
        steepness: Steepness of the curve (0.1 = gradual, 1.0 = steep)
        
    Returns:
        List of adoption percentages for each time period
    """
    if inflection_point is None:
        inflection_point = time_periods // 2
        
    t = np.arange(time_periods)
    
    # Logistic function: L / (1 + e^(-k(t-t0)))
    # L = max value, k = steepness, t0 = inflection point
    adoption = max_adoption / (1 + np.exp(-steepness * (t - inflection_point)))
    
    return adoption.tolist()


def technology_correlation_matrix(
    technologies: List[str],
    correlation_type: str = 'complementary'
) -> np.ndarray:
    """
    Generate correlation matrix for technology adoption.
    
    Args:
        technologies: List of technology names
        correlation_type: 'complementary', 'competitive', or 'mixed'
        
    Returns:
        Correlation matrix as numpy array
    """
    n = len(technologies)
    
    if correlation_type == 'complementary':
        # Technologies reinforce each other
        base_correlation = 0.3
        noise_level = 0.1
    elif correlation_type == 'competitive':
        # Technologies compete with each other
        base_correlation = -0.2
        noise_level = 0.1
    else:  # mixed
        base_correlation = 0.0
        noise_level = 0.3
        
    # Create correlation matrix
    corr_matrix = np.eye(n)  # Start with identity matrix
    
    for i in range(n):
        for j in range(i + 1, n):
            # Add base correlation with some random noise
            correlation = base_correlation + np.random.uniform(-noise_level, noise_level)
            # Ensure correlation is in valid range
            correlation = np.clip(correlation, -0.9, 0.9)
            corr_matrix[i, j] = correlation
            corr_matrix[j, i] = correlation  # Symmetric
            
    return corr_matrix


def scenario_comparison(
    scenarios: Dict[str, Dict[str, float]],
    model_function: Callable,
    metrics_to_compare: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Compare multiple scenarios side by side.
    
    Args:
        scenarios: Dictionary of scenario names to parameter sets
        model_function: Function to evaluate each scenario
        metrics_to_compare: Optional list of specific metrics to extract
        
    Returns:
        DataFrame with scenario comparison
    """
    results = []
    
    for scenario_name, parameters in scenarios.items():
        try:
            result = model_function(**parameters)
            
            # Handle different result types
            if isinstance(result, dict):
                row = {'scenario': scenario_name}
                row.update(result)
            elif isinstance(result, (int, float)):
                row = {'scenario': scenario_name, 'result': result}
            else:
                row = {'scenario': scenario_name, 'result': str(result)}
                
            results.append(row)
            
        except Exception as e:
            logger.error(f"Failed to evaluate scenario {scenario_name}: {e}")
            results.append({'scenario': scenario_name, 'error': str(e)})
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Filter columns if requested
    if metrics_to_compare:
        columns = ['scenario'] + [col for col in metrics_to_compare if col in df.columns]
        df = df[columns]
    
    return df


def create_scenario_tornado_chart(
    sensitivity_results: Dict,
    variable_names: Optional[Dict[str, str]] = None
) -> Dict:
    """
    Create data for tornado chart visualization from sensitivity analysis.
    
    Args:
        sensitivity_results: Results from sensitivity_analysis function
        variable_names: Optional mapping of variable codes to display names
        
    Returns:
        Dictionary with tornado chart data
    """
    base_result = sensitivity_results['base_result']
    tornado_data = []
    
    for var, data in sensitivity_results.items():
        if var in ['base_result', 'sensitivity_ranking']:
            continue
            
        values = data['values']
        if not values:
            continue
            
        # Get min and max impacts
        impacts = [v['result'] for v in values]
        min_impact = min(impacts)
        max_impact = max(impacts)
        
        # Calculate deviations from base
        min_deviation = min_impact - base_result
        max_deviation = max_impact - base_result
        
        display_name = variable_names.get(var, var) if variable_names else var
        
        tornado_data.append({
            'variable': display_name,
            'min_impact': min_impact,
            'max_impact': max_impact,
            'min_deviation': min_deviation,
            'max_deviation': max_deviation,
            'range': max_impact - min_impact,
            'elasticity': data['elasticity']
        })
    
    # Sort by impact range
    tornado_data.sort(key=lambda x: x['range'], reverse=True)
    
    return {
        'base_result': base_result,
        'data': tornado_data
    }