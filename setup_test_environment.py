#!/usr/bin/env python3
"""
Setup script for AI-Adoption-Dashboard test environment
This script sets up a virtual environment and installs all dependencies
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description="", check=True):
    """Run a command and handle errors"""
    print(f"Running: {description or command}")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def setup_virtual_environment():
    """Set up Python virtual environment"""
    project_dir = Path(__file__).parent
    venv_dir = project_dir / "venv"
    
    print("Setting up virtual environment...")
    
    # Create virtual environment
    if not venv_dir.exists():
        if not run_command(f"python3 -m venv {venv_dir}", "Creating virtual environment"):
            print("Failed to create virtual environment")
            return False
    
    # Determine activation script path
    if platform.system() == "Windows":
        activate_script = venv_dir / "Scripts" / "activate"
        pip_path = venv_dir / "Scripts" / "pip"
    else:
        activate_script = venv_dir / "bin" / "activate"
        pip_path = venv_dir / "bin" / "pip"
    
    print(f"Virtual environment created at: {venv_dir}")
    print(f"To activate manually: source {activate_script}")
    
    return str(pip_path)

def install_dependencies(pip_path):
    """Install project dependencies"""
    project_dir = Path(__file__).parent
    
    # Install main dependencies
    requirements_files = [
        project_dir / "requirements.txt",
        project_dir / "requirements-test.txt"
    ]
    
    for req_file in requirements_files:
        if req_file.exists():
            print(f"Installing from {req_file.name}...")
            if not run_command(f"{pip_path} install -r {req_file}", 
                             f"Installing {req_file.name}"):
                print(f"Warning: Failed to install some packages from {req_file}")
        else:
            print(f"Warning: {req_file} not found")
    
    # Install additional packages that might be missing
    additional_packages = [
        "streamlit",
        "pandas", 
        "plotly",
        "numpy",
        "pydantic",
        "psutil",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "hypothesis",
        "memory-profiler"
    ]
    
    print("Installing additional packages...")
    for package in additional_packages:
        run_command(f"{pip_path} install {package}", 
                   f"Installing {package}", check=False)

def run_tests(pip_path):
    """Run the test suite"""
    project_dir = Path(__file__).parent
    venv_dir = project_dir / "venv"
    
    if platform.system() == "Windows":
        python_path = venv_dir / "Scripts" / "python"
        pytest_path = venv_dir / "Scripts" / "pytest"
    else:
        python_path = venv_dir / "bin" / "python"
        pytest_path = venv_dir / "bin" / "pytest"
    
    # Set PYTHONPATH to include project directory
    env = os.environ.copy()
    env['PYTHONPATH'] = str(project_dir)
    
    print("Running test suite...")
    
    # Run different test categories
    test_commands = [
        (f"{pytest_path} tests/unit/ -v", "Unit tests"),
        (f"{pytest_path} tests/integration/ -v", "Integration tests"),
        (f"{pytest_path} tests/performance/ -v", "Performance tests"),
        (f"{pytest_path} --cov=. --cov-report=term-missing", "Coverage report")
    ]
    
    results = {}
    for command, description in test_commands:
        print(f"\n{'='*50}")
        print(f"Running: {description}")
        print('='*50)
        
        try:
            result = subprocess.run(command, shell=True, cwd=project_dir,
                                  env=env, timeout=300)
            results[description] = result.returncode == 0
        except subprocess.TimeoutExpired:
            print(f"Test timeout: {description}")
            results[description] = False
        except Exception as e:
            print(f"Test error: {description} - {e}")
            results[description] = False
    
    return results

def main():
    """Main setup function"""
    print("AI-Adoption-Dashboard Test Environment Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    
    # Setup virtual environment
    pip_path = setup_virtual_environment()
    if not pip_path:
        print("Failed to setup virtual environment")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies(pip_path)
    
    # Run tests
    print("\n" + "="*50)
    print("Running test suite...")
    print("="*50)
    
    test_results = run_tests(pip_path)
    
    # Print summary
    print("\n" + "="*50)
    print("SETUP SUMMARY")
    print("="*50)
    
    print("✅ Virtual environment: Created")
    print("✅ Dependencies: Installed")
    
    print("\nTest Results:")
    for test_name, passed in test_results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    print(f"\nOverall: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Environment is ready.")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test suite(s) failed. Check logs above.")
    
    print(f"\nTo activate virtual environment:")
    project_dir = Path(__file__).parent
    venv_dir = project_dir / "venv"
    if platform.system() == "Windows":
        print(f"  {venv_dir}\\Scripts\\activate")
    else:
        print(f"  source {venv_dir}/bin/activate")

if __name__ == "__main__":
    main()