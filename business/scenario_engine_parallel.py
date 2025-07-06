"""Enhanced scenario analysis engine with parallel processing.

This module provides parallel processing capabilities for Monte Carlo
simulations and other computationally intensive scenario analyses.
"""

import logging
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Dict, List, Tuple, Optional, Callable
import numpy as np
from functools import partial

from .scenario_engine import (
    ScenarioVariable,
    monte_carlo_simulation as _monte_carlo_simulation,
    sensitivity_analysis as _sensitivity_analysis
)
from utils.cache_manager import cache_monte_carlo, calculation_cache

logger = logging.getLogger(__name__)


def _run_simulation_batch(
    args: Tuple[Dict, List[ScenarioVariable], Callable, int, int]
) -> List[float]:
    """Run a batch of Monte Carlo simulations.
    
    This function is designed to be run in parallel processes.
    
    Args:
        args: Tuple containing (base_case, variables, model_function, 
              start_seed, num_iterations)
        
    Returns:
        List of simulation results
    """
    base_case, variables, model_function, start_seed, num_iterations = args
    
    # Set random seed for reproducibility
    np.random.seed(start_seed)
    
    results = []
    
    for i in range(num_iterations):
        # Generate random values for each variable
        scenario = base_case.copy()
        
        for var in variables:
            if var.distribution == 'normal':
                std = var.std_dev or (var.max_value - var.min_value) / 4
                value = np.random.normal(var.base_value, std)
                value = np.clip(value, var.min_value, var.max_value)
                
            elif var.distribution == 'uniform':
                value = np.random.uniform(var.min_value, var.max_value)
                
            elif var.distribution == 'triangular':
                mode = var.mode or var.base_value
                value = np.random.triangular(var.min_value, mode, var.max_value)
                
            else:
                value = var.base_value
            
            scenario[var.name] = value
        
        # Run model with scenario parameters
        try:
            result = model_function(**scenario)
            results.append(result)
        except Exception as e:
            logger.warning(f"Simulation iteration failed: {e}")
            continue
    
    return results


@cache_monte_carlo
def monte_carlo_simulation_parallel(
    base_case: Dict[str, float],
    variables: List[ScenarioVariable],
    model_function: Callable,
    iterations: int = 10000,
    confidence_levels: List[float] = [0.05, 0.25, 0.50, 0.75, 0.95],
    n_processes: Optional[int] = None
) -> Dict:
    """Run Monte Carlo simulation with parallel processing.
    
    This version uses multiple CPU cores to speed up large simulations.
    
    Args:
        base_case: Base case values for all parameters
        variables: List of variables to vary in simulation
        model_function: Function that takes parameters and returns result
        iterations: Number of simulation iterations
        confidence_levels: Percentiles to calculate
        n_processes: Number of processes (None = number of CPUs)
        
    Returns:
        Dictionary with simulation results and statistics
    """
    # Check cache first
    cached_result = calculation_cache.get_monte_carlo(
        base_case, variables, iterations
    )
    if cached_result is not None:
        logger.info(f"Retrieved Monte Carlo results from cache")
        return cached_result
    
    # Determine number of processes
    if n_processes is None:
        n_processes = mp.cpu_count()
    
    # For small iterations, use single process
    if iterations < 1000 or n_processes == 1:
        logger.info(f"Running Monte Carlo with single process ({iterations} iterations)")
        result = _monte_carlo_simulation(
            base_case, variables, model_function, 
            iterations, confidence_levels
        )
        # Cache the result
        calculation_cache.cache_monte_carlo(
            base_case, variables, iterations, result
        )
        return result
    
    logger.info(f"Running parallel Monte Carlo with {n_processes} processes ({iterations} iterations)")
    
    # Split iterations across processes
    iterations_per_process = iterations // n_processes
    remainder = iterations % n_processes
    
    # Prepare arguments for each process
    process_args = []
    seed_offset = 0
    
    for i in range(n_processes):
        # Distribute remainder iterations
        process_iterations = iterations_per_process
        if i < remainder:
            process_iterations += 1
            
        # Create args tuple for this process
        args = (
            base_case,
            variables,
            model_function,
            seed_offset,  # Unique seed for each process
            process_iterations
        )
        process_args.append(args)
        seed_offset += process_iterations
    
    # Run simulations in parallel
    all_results = []
    
    with ProcessPoolExecutor(max_workers=n_processes) as executor:
        # Submit all tasks
        futures = [executor.submit(_run_simulation_batch, args) 
                  for args in process_args]
        
        # Collect results
        for future in futures:
            try:
                batch_results = future.result(timeout=300)  # 5 minute timeout
                all_results.extend(batch_results)
            except Exception as e:
                logger.error(f"Process failed: {e}")
                # Continue with other processes
    
    # If we didn't get enough results, fall back to single process
    if len(all_results) < iterations * 0.9:  # Allow 10% failure rate
        logger.warning(f"Parallel processing incomplete, falling back to single process")
        return _monte_carlo_simulation(
            base_case, variables, model_function, 
            iterations, confidence_levels
        )
    
    # Calculate statistics from combined results
    results_array = np.array(all_results)
    percentiles = np.percentile(results_array, [cl * 100 for cl in confidence_levels])
    
    # Calculate variable correlations (simplified for parallel version)
    result = {
        'iterations': len(all_results),
        'mean': np.mean(results_array),
        'std_dev': np.std(results_array),
        'min': np.min(results_array),
        'max': np.max(results_array),
        'percentiles': dict(zip([f'p{int(cl*100)}' for cl in confidence_levels], percentiles)),
        'confidence_interval_90': (percentiles[0], percentiles[-1]),
        'coefficient_of_variation': np.std(results_array) / np.mean(results_array) if np.mean(results_array) != 0 else np.inf,
        'correlations': {},  # Simplified for parallel version
        'histogram_data': {
            'values': all_results[:1000],  # Limit for UI performance
            'bins': np.histogram(results_array, bins=50)[1].tolist()
        }
    }
    
    # Cache the result
    calculation_cache.cache_monte_carlo(
        base_case, variables, iterations, result
    )
    
    logger.info(f"Parallel Monte Carlo completed: {len(all_results)} iterations")
    
    return result


def sensitivity_analysis_parallel(
    base_case: Dict[str, float],
    variables: List[str],
    model_function: Callable,
    variation_pct: float = 0.20,
    steps: int = 5,
    n_threads: int = 4
) -> Dict:
    """Perform sensitivity analysis with parallel execution.
    
    This version uses threading for I/O-bound sensitivity calculations.
    
    Args:
        base_case: Base case parameter values
        variables: List of variable names to analyze
        model_function: Function to evaluate
        variation_pct: Percentage to vary each parameter (±)
        steps: Number of steps in each direction
        n_threads: Number of threads to use
        
    Returns:
        Dictionary with sensitivity analysis results
    """
    def analyze_variable(var: str) -> Tuple[str, Dict]:
        """Analyze sensitivity for a single variable."""
        if var not in base_case:
            logger.warning(f"Variable {var} not in base case")
            return var, {'values': [], 'elasticity': 0, 'sensitivity_rank': 0}
            
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
                    'pct_change_output': 0  # Will be calculated later
                })
            except Exception as e:
                logger.warning(f"Sensitivity analysis failed for {var} at {multiplier}: {e}")
        
        # Calculate elasticity if we have results
        elasticity = 0
        if len(var_results) >= 2:
            # Simple elasticity calculation
            x_values = [r['pct_change_input'] for r in var_results]
            y_values = [r['result'] for r in var_results]
            
            if len(set(x_values)) > 1 and base_value != 0:
                # Calculate percentage changes in output
                base_result = model_function(**base_case)
                for r in var_results:
                    r['pct_change_output'] = ((r['result'] - base_result) / base_result * 100) if base_result != 0 else 0
                
                # Linear regression for elasticity
                y_pct_values = [r['pct_change_output'] for r in var_results]
                if max(x_values) - min(x_values) > 0:
                    elasticity = (max(y_pct_values) - min(y_pct_values)) / (max(x_values) - min(x_values))
        
        return var, {
            'values': var_results,
            'elasticity': elasticity,
            'sensitivity_rank': abs(elasticity)
        }
    
    # Get base result
    base_result = model_function(**base_case)
    results = {'base_result': base_result}
    
    # Use thread pool for parallel execution
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        # Submit all variables for analysis
        future_to_var = {executor.submit(analyze_variable, var): var 
                        for var in variables}
        
        # Collect results
        for future in future_to_var:
            var = future_to_var[future]
            try:
                var_name, var_result = future.result(timeout=60)
                results[var_name] = var_result
            except Exception as e:
                logger.error(f"Failed to analyze {var}: {e}")
                results[var] = {'values': [], 'elasticity': 0, 'sensitivity_rank': 0}
    
    # Rank variables by sensitivity
    sensitivity_ranking = sorted(
        [(var, data['sensitivity_rank']) for var, data in results.items() 
         if var != 'base_result'],
        key=lambda x: x[1],
        reverse=True
    )
    
    results['sensitivity_ranking'] = sensitivity_ranking
    
    return results


# Configuration functions
def get_optimal_process_count(iterations: int) -> int:
    """Determine optimal number of processes for Monte Carlo.
    
    Args:
        iterations: Number of Monte Carlo iterations
        
    Returns:
        Optimal number of processes
    """
    cpu_count = mp.cpu_count()
    
    # Rules for process count
    if iterations < 1000:
        return 1  # Not worth parallelizing
    elif iterations < 5000:
        return min(2, cpu_count)
    elif iterations < 20000:
        return min(4, cpu_count)
    else:
        # Use all CPUs for large simulations
        return cpu_count


def estimate_simulation_time(
    iterations: int,
    variables_count: int,
    model_complexity: str = "medium"
) -> float:
    """Estimate time for Monte Carlo simulation.
    
    Args:
        iterations: Number of iterations
        variables_count: Number of variables
        model_complexity: "simple", "medium", or "complex"
        
    Returns:
        Estimated time in seconds
    """
    # Base time per iteration (milliseconds)
    complexity_factors = {
        "simple": 0.1,
        "medium": 0.5,
        "complex": 2.0
    }
    
    base_time = complexity_factors.get(model_complexity, 0.5)
    
    # Adjust for number of variables
    variable_factor = 1 + (variables_count * 0.1)
    
    # Calculate total time
    total_ms = iterations * base_time * variable_factor
    
    # Account for parallel speedup
    n_processes = get_optimal_process_count(iterations)
    parallel_efficiency = 0.8  # Typical parallel efficiency
    
    if n_processes > 1:
        total_ms = total_ms / (n_processes * parallel_efficiency)
    
    return total_ms / 1000  # Convert to seconds


# Export enhanced versions
__all__ = [
    'monte_carlo_simulation_parallel',
    'sensitivity_analysis_parallel',
    'get_optimal_process_count',
    'estimate_simulation_time',
    'ScenarioVariable'  # Re-export from original module
]