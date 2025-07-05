#!/usr/bin/env python3
"""Check if all required dependencies can be installed."""

import subprocess
import sys
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python 3.8 or higher is required")
        return False

def check_pip():
    """Check if pip is available."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ pip is available: {result.stdout.strip()}")
            return True
        else:
            print("❌ pip is not available")
            print("\nTo install pip:")
            if platform.system() == "Linux":
                print("  sudo apt install python3-pip")
            elif platform.system() == "Darwin":
                print("  brew install python3")
            else:
                print("  python3 -m ensurepip --default-pip")
            return False
    except Exception as e:
        print(f"❌ Error checking pip: {e}")
        return False

def check_venv():
    """Check if venv module is available."""
    try:
        import venv
        print("✅ venv module is available")
        return True
    except ImportError:
        print("❌ venv module is not available")
        print("\nTo install venv:")
        print(f"  sudo apt install python{sys.version_info.major}.{sys.version_info.minor}-venv")
        return False

def check_requirements_files():
    """Check if requirements files exist."""
    req_files = ["requirements.txt", "requirements-dev.txt"]
    all_exist = True
    
    for req_file in req_files:
        if Path(req_file).exists():
            print(f"✅ {req_file} exists")
        else:
            print(f"❌ {req_file} is missing")
            all_exist = False
    
    return all_exist

def check_env_file():
    """Check if .env.example exists."""
    if Path(".env.example").exists():
        print("✅ .env.example exists")
        if not Path(".env").exists():
            print("ℹ️  .env not found - you'll need to copy .env.example to .env")
        return True
    else:
        print("❌ .env.example is missing")
        return False

def test_imports():
    """Test if critical modules can be imported (without external deps)."""
    print("\nTesting local imports...")
    
    test_modules = [
        ("utils.error_handler", "ErrorHandler"),
        ("utils.types", "DashboardData"),
        ("views.base", "ViewRegistry"),
        ("config.settings", "Settings"),
    ]
    
    # Save current path
    original_path = sys.path.copy()
    
    # Add current directory to path
    sys.path.insert(0, str(Path.cwd()))
    
    all_good = True
    for module, item in test_modules:
        try:
            exec(f"from {module} import {item}")
            print(f"✅ Can import {item} from {module}")
        except ImportError as e:
            # Check if it's due to external dependencies
            if "streamlit" in str(e) or "pandas" in str(e):
                print(f"⚠️  {module} requires external dependencies (expected)")
            else:
                print(f"❌ Cannot import {item} from {module}: {e}")
                all_good = False
        except Exception as e:
            print(f"❌ Error importing {item} from {module}: {e}")
            all_good = False
    
    # Restore path
    sys.path = original_path
    
    return all_good

def suggest_next_steps():
    """Suggest next steps for installation."""
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("\n1. Create a virtual environment:")
    print("   python3 -m venv .venv")
    print("   source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate")
    print("\n2. Install dependencies:")
    print("   python3 -m pip install --upgrade pip")
    print("   python3 -m pip install -r requirements.txt")
    print("   python3 -m pip install -r requirements-dev.txt")
    print("\n3. Configure environment:")
    print("   cp .env.example .env")
    print("   # Edit .env with your settings")
    print("\n4. Run the application:")
    print("   streamlit run app.py")

def main():
    """Run all checks."""
    print("🔍 Checking dependencies for AI Adoption Dashboard\n")
    
    checks = [
        ("Python Version", check_python_version()),
        ("pip Available", check_pip()),
        ("venv Module", check_venv()),
        ("Requirements Files", check_requirements_files()),
        ("Environment Config", check_env_file()),
        ("Local Imports", test_imports()),
    ]
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print("\n" + "="*60)
    print(f"Summary: {passed}/{total} checks passed")
    print("="*60)
    
    if passed == total:
        print("\n✅ All dependency checks passed!")
        suggest_next_steps()
    else:
        print("\n⚠️  Some checks failed. Please address the issues above.")
        if checks[1][1]:  # If pip is available
            suggest_next_steps()
        else:
            print("\n❗ Install pip first before proceeding.")

if __name__ == "__main__":
    main()