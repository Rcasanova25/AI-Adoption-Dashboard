# Installation Guide for AI Adoption Dashboard

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## Checking Prerequisites

### 1. Check Python Version
```bash
python3 --version
# Should show Python 3.8.x or higher
```

### 2. Check pip
```bash
python3 -m pip --version
# Should show pip version
```

## Installing pip (if not available)

### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

### On macOS:
```bash
# If you have Homebrew:
brew install python3

# Or download get-pip.py:
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### On Windows (WSL):
```bash
sudo apt update
sudo apt install python3-pip python3-venv
```

### Alternative: Using get-pip.py
```bash
# Download the pip installer
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# Install pip
python3 get-pip.py --user

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

## Installing the Dashboard

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Adoption-Dashboard
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
# Upgrade pip first
python3 -m pip install --upgrade pip

# Install production dependencies
python3 -m pip install -r requirements.txt

# Install development dependencies (for testing)
python3 -m pip install -r requirements-dev.txt
```

### 4. Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use your preferred editor
```

### 5. Run the Application
```bash
streamlit run app.py
```

## Troubleshooting

### "No module named pip"
```bash
# On Ubuntu/Debian:
sudo apt install python3-pip

# Or use ensurepip:
python3 -m ensurepip --default-pip
```

### "Permission denied" errors
```bash
# Install packages for current user only:
python3 -m pip install --user -r requirements.txt

# Or use sudo (not recommended):
sudo python3 -m pip install -r requirements.txt
```

### SSL Certificate errors
```bash
# Temporary workaround (not recommended for production):
python3 -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Virtual environment issues
```bash
# Install venv package:
sudo apt install python3.x-venv  # Replace x with your Python version

# Or create without venv:
python3 -m pip install --user -r requirements.txt
```

## Verifying Installation

Run the verification script:
```bash
python3 verify_critical_fixes.py
```

All checks should pass. If not, review the error messages and ensure all dependencies are installed.

## Next Steps

1. Run tests: `python3 -m pytest tests/`
2. Check code quality: `python3 -m flake8`
3. Format code: `python3 -m black .`
4. Type check: `python3 -m mypy .`

See [TESTING.md](TESTING.md) for detailed testing instructions.