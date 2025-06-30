import json
import os
import subprocess
import sys
from datetime import datetime

def run_performance_benchmark():
    """Run performance benchmark and return results"""
    result = subprocess.run([
        'pytest', 'tests/performance/', 
        '-m', 'performance and not slow',
        '--benchmark-json=benchmark.json',
        '-q'
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Performance tests failed: {result.stderr}")
        return None
    
    try:
        with open('benchmark.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Benchmark results not found")
        return None

def load_baseline():
    """Load baseline performance metrics"""
    baseline_file = 'performance_baseline.json'
    if os.path.exists(baseline_file):
        with open(baseline_file, 'r') as f:
            return json.load(f)
    return None

def save_baseline(results):
    """Save current results as new baseline"""
    with open('performance_baseline.json', 'w') as f:
        json.dump(results, f, indent=2)

def check_regression(current, baseline, threshold=0.2):
    """Check for performance regression"""
    if not baseline:
        print("No baseline found, saving current results as baseline")
        save_baseline(current)
        return True
    
    regressions = []
    
    # Compare key metrics
    for test_name, current_metrics in current.get('benchmarks', {}).items():
        if test_name in baseline.get('benchmarks', {}):
            baseline_metrics = baseline['benchmarks'][test_name]
            
            # Check execution time regression
            current_time = current_metrics.get('mean', 0)
            baseline_time = baseline_metrics.get('mean', 0)
            
            if baseline_time > 0:
                regression_ratio = (current_time - baseline_time) / baseline_time
                
                if regression_ratio > threshold:
                    regressions.append({
                        'test': test_name,
                        'current_time': current_time,
                        'baseline_time': baseline_time,
                        'regression_percent': regression_ratio * 100
                    })
    
    if regressions:
        print("Performance regressions detected:")
        for reg in regressions:
            print(f"  {reg['test']}: {reg['regression_percent']:.1f}% slower")
            print(f"    Current: {reg['current_time']:.4f}s")
            print(f"    Baseline: {reg['baseline_time']:.4f}s")
        return False
    else:
        print("No performance regressions detected")
        save_baseline(current)
        return True

if __name__ == "__main__":
    current_results = run_performance_benchmark()
    if current_results is None:
        sys.exit(1)
    
    baseline_results = load_baseline()
    
    if not check_regression(current_results, baseline_results):
        sys.exit(1) 