#!/bin/bash
# FOR LINUX
VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment found."
fi

source "$VENV_DIR/bin/activate"

if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping package installation."
fi

echo "Running main.py..."
python main.py

deactivate
