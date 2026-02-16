#!/bin/bash
# ============================================================================
# AUTOMATED SETUP SCRIPT
# ============================================================================
# This script installs everything needed for the log monitoring system
# It creates a virtual environment and installs all dependencies

# ----------------------------------------------------------------------------
# PRINT HEADER
# ----------------------------------------------------------------------------
echo "============================================"
echo "Log Monitoring System - Automated Setup"
echo "============================================"
echo ""

# ----------------------------------------------------------------------------
# CHECK PYTHON INSTALLATION
# ----------------------------------------------------------------------------
# First, verify Python 3 is installed on this system
if ! command -v python3 &> /dev/null; then
    # If python3 command doesn't exist, show error and exit
    echo "❌ ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "  • Windows: https://www.python.org/downloads/"
    echo "  • Mac: brew install python3"
    echo "  • Linux: sudo apt-get install python3"
    exit 1  # Exit with error code
fi

# Python is installed - show version
echo "✓ Python 3 found: $(python3 --version)"
echo ""

# ----------------------------------------------------------------------------
# CREATE VIRTUAL ENVIRONMENT
# ----------------------------------------------------------------------------
# What is a virtual environment?
# - Isolated Python environment for this project only
# - Prevents conflicts with other Python projects
# - Example: Project A needs pandas v1.0, Project B needs pandas v2.0
#            Virtual environments let both coexist

echo "Creating virtual environment..."
python3 -m venv venv  # Creates a folder called 'venv' with isolated Python

# Check if virtual environment was created successfully
if [ ! -d "venv" ]; then
    echo "❌ ERROR: Failed to create virtual environment"
    exit 1
fi

echo "✓ Virtual environment created"
echo ""

# ----------------------------------------------------------------------------
# ACTIVATE VIRTUAL ENVIRONMENT
# ----------------------------------------------------------------------------
# Activation tells terminal to use the isolated Python instead of system Python

echo "Activating virtual environment..."
source venv/bin/activate  # On Windows Git Bash, this works
                          # On Windows CMD, use: venv\Scripts\activate.bat
                          # On Mac/Linux, use: source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# ----------------------------------------------------------------------------
# UPGRADE PIP
# ----------------------------------------------------------------------------
# pip is the Python package installer
# We upgrade it to get the latest features and bug fixes

echo "Upgrading pip (Python package installer)..."
pip install --upgrade pip --quiet  # --quiet means don't show all the details

echo "✓ pip upgraded to latest version"
echo ""

# ----------------------------------------------------------------------------
# INSTALL DEPENDENCIES
# ----------------------------------------------------------------------------
# Now install all the libraries listed in requirements.txt

echo "Installing dependencies..."
echo "(This may take 2-5 minutes depending on internet speed)"
echo ""

# Install each package
echo "  → Installing Dask (parallel processing)..."
pip install dask[complete]==2024.1.1 --quiet

echo "  → Installing Ray (distributed monitoring)..."
pip install ray[default]==2.9.0 --quiet

echo "  → Installing PyYAML (YAML parsing)..."
pip install pyyaml==6.0.1 --quiet

echo "  → Installing Pandas (data manipulation)..."
pip install pandas==2.1.4 --quiet

echo "  → Installing Bokeh (visualization)..."
pip install bokeh==3.3.2 --quiet

echo "  → Installing Distributed (Dask scheduler)..."
pip install distributed==2024.1.1 --quiet

echo "  → Installing Pytest (testing)..."
pip install pytest==7.4.3 --quiet

echo "  → Installing Pytest-cov (test coverage)..."
pip install pytest-cov==4.1.0 --quiet

echo ""
echo "✓ All dependencies installed"
echo ""

# ----------------------------------------------------------------------------
# CREATE NECESSARY DIRECTORIES
# ----------------------------------------------------------------------------
# Make sure all required folders exist

echo "Creating necessary directories..."
mkdir -p logs         # Where log files will be stored
mkdir -p screenshots  # Where dashboard screenshots go
mkdir -p tests        # Where test files go

echo "✓ Directories created"
echo ""

# ----------------------------------------------------------------------------
# VERIFY INSTALLATION
# ----------------------------------------------------------------------------
# Check that key packages were installed correctly

echo "Verifying installation..."
python3 << EOF
try:
    import dask
    import ray
    import yaml
    import pandas
    print("✓ All core packages verified")
except ImportError as e:
    print(f"❌ Import error: {e}")
    exit(1)
EOF

echo ""

# ----------------------------------------------------------------------------
# PRINT SUCCESS MESSAGE
# ----------------------------------------------------------------------------
echo "============================================"
echo "✓ SETUP COMPLETE!"
echo "============================================"
echo ""
echo "Your log monitoring system is ready!"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run tests to verify:"
echo "     python tests/test_environment.py"
echo ""
echo "  3. Start Dask dashboard:"
echo "     python -c \"from dask.distributed import Client; client = Client(); input('Press Enter to stop...')\""
echo "     Open: http://localhost:8787"
echo ""
echo "  4. Start Ray dashboard:"
echo "     ray start --head --dashboard-host=0.0.0.0"
echo "     Open: http://localhost:8265"
echo ""
echo "============================================"