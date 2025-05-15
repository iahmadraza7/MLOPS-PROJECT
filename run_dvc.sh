#!/bin/bash
set -e

# Ensure we're in the project directory
cd /app

# Initialize DVC if not already initialized
if [ ! -d ".dvc" ]; then
  echo "Initializing DVC"
  dvc init
fi

# Run the specified command or 'repro' by default
if [ $# -eq 0 ]; then
  echo "Running 'dvc repro'"
  dvc repro
else
  echo "Running 'dvc $@'"
  dvc "$@"
fi 