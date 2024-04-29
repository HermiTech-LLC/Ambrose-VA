#!/bin/bash

# Function to check if a command exists
command_exists () {
    type "$1" &> /dev/null ;
}

echo "Starting setup for Ambrose-VA..."

# Check for Python and Pip installation
echo "Checking for Python and pip installation..."
if command_exists python3 && command_exists pip3; then
    echo "Python 3 and pip are installed."
else
    echo "Error: Python 3 or pip is not installed. Please install both before continuing."
    exit 1
fi

# Set up Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
if [ $? -eq 0 ]; then
    echo "Virtual environment created successfully."
else
    echo "Failed to create virtual environment. Please check your Python installation."
    exit 1
fi

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    echo "Virtual environment activated."
else
    echo "Failed to activate the virtual environment."
    exit 1
fi

# Install required packages
echo "Upgrading pip and installing required packages..."
pip3 install --upgrade pip && pip3 install setuptools wheel
if [ $? -eq 0 ]; then
    echo "Packages installed successfully."
else
    echo "Failed to install required packages."
    exit 1
fi

# Check if setup.py exists
echo "Checking for setup.py file..."
if [ -f setup.py ]; then
    echo "setup.py found. Installing your package..."
    pip3 install .
    if [ $? -eq 0 ]; then
        echo "Your package has been installed successfully."
    else
        echo "Failed to install your package. Please check setup.py for errors."
        exit 1
    fi
else
    echo "setup.py not found. Please ensure you are in the correct directory and try again."
    exit 1
fi

# Provide instructions for running the application
echo "Setup complete. To start the personal assistant, use the command: 'personal-assistant'"
echo "To deactivate the virtual environment, use the command: 'deactivate'"