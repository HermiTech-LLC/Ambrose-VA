#!/bin/bash

# Function to check if a command exists
command_exists () {
    type "$1" &> /dev/null ;
}

# Check for Python and Pip installation
echo "Checking for Python installation..."
if command_exists python3 && command_exists pip3; then
    echo "Python and Pip are installed."
else
    echo "Python or Pip is not installed. Please install Python 3 and Pip."
    exit 1
fi

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip3 install --upgrade pip
pip3 install setuptools wheel

# Check if setup.py exists
if [ -f setup.py ]; then
    echo "Found setup.py. Installing your package..."
    pip3 install .
    echo "Installation complete."
else
    echo "setup.py not found. Please ensure you are in the correct directory and try again."
    exit 1
fi

# Provide instructions for running the application
echo "To start the personal assistant, use the command: 'personal-assistant'"
echo "To deactivate the virtual environment, use the command: 'deactivate'"
