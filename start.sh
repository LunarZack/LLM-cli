#!/bin/bash

# Check if already in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    # If not in a virtual environment, check if .venv exists
    if [ -d ".venv" ]; then
        echo "Activating virtual environment..."
        source .venv/bin/activate
    else
        echo "No virtual environment found. Running without it."
    fi
else
    echo "Already inside a virtual environment. Skipping activation."
fi

# Run the script
python3 llm-cli.py
