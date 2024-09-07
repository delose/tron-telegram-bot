#!/bin/bash

# Check if the virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is NOT activated."
    echo "Please activate it using: source venv/bin/activate"
else
    echo "Virtual environment is activated."
    echo "Current virtual environment: $VIRTUAL_ENV"
fi


