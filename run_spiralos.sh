#!/bin/bash

echo "🌀 Welcome to SpiralOS Setup & Launcher"
echo "Checking Python version..."
python3 --version

echo "Installing required Python packages..."
pip install --upgrade pip
pip install matplotlib networkx tk

echo "Which mode do you want to run?"
echo "1. CLI (console)"
echo "2. GUI (visual spiral)"

read -p "Enter 1 or 2: " mode

if [ "$mode" = "1" ]; then
  echo "Launching SpiralOS CLI..."
  python3 spiralos_runtime.py
elif [ "$mode" = "2" ]; then
  echo "Launching SpiralOS GUI..."
  python3 spiralos_gui.py
else
  echo "Invalid input. Exiting."
fi
