#!/usr/bin/env python3
"""
Setup script to initialize the project directory structure
"""

import os
from pathlib import Path

# Define the project directories
directories = [
    "data/raw",
    "data/processed",
    "models",
    "mlflow",
    "metrics",
    "tests",
    "src",
    "airflow/dags",
    "k8s",
    "docs",
    "logs",
    "monitoring",
    "monitoring/grafana-provisioning",
    ".github/workflows",
    "dvc_plots",
    "dvc_remote",
    ".dvc"
]

# Create the directories
for directory in directories:
    Path(directory).mkdir(parents=True, exist_ok=True)
    print(f"Created directory: {directory}")

# Create empty placeholder files to ensure git tracks empty directories
for directory in directories:
    placeholder_file = Path(directory) / ".gitkeep"
    if not placeholder_file.exists():
        with open(placeholder_file, "w") as f:
            f.write("# This file ensures git tracks this empty directory\n")
        print(f"Created placeholder file: {placeholder_file}")

print("\nProject directory structure initialized successfully!")
print("Next steps:")
print("1. Add your raw data to the data/raw directory")
print("2. Run the ETL pipeline with Airflow")
print("3. Train the model with src/train_model.py")
print("4. Deploy the model with Docker and Kubernetes") 