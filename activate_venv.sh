#!/bin/bash

# Run below using source command

source venv/bin/activate

# Check if the activation was successful
if [ "$VIRTUAL_ENV" != "" ]; then
    echo "Virtual environment activated successfully."
else
    echo "Failed to activate the virtual environment."
    exit 1  # Exit the script with an error status
fi
