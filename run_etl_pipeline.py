#!/usr/bin/env python
"""
Standalone ETL Pipeline Runner
This script performs the same functions as the Airflow DAG but can run without Airflow.
"""
import os
import sys
import pandas as pd
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_PATH = BASE_DIR / 'data' / 'raw' / 'ODI_Cricket_Data.csv'
PROCESSED_DIR = BASE_DIR / 'data' / 'processed'
PREPROCESS_SCRIPT = BASE_DIR / 'src' / 'preprocess.py'
TRAIN_SCRIPT = BASE_DIR / 'src' / 'train_model.py'

# Ensure directories exist
os.makedirs(PROCESSED_DIR, exist_ok=True)

def extract():
    """Extract data from source and save to intermediate location"""
    logger.info(f"Extracting data from {RAW_DATA_PATH}")
    
    # Check if the raw data file exists
    if not RAW_DATA_PATH.exists():
        logger.error(f"Raw data file not found: {RAW_DATA_PATH}")
        sys.exit(1)
    
    # Define output path
    raw_csv_path = PROCESSED_DIR / 'raw.csv'
    
    # Read and save data
    df = pd.read_csv(RAW_DATA_PATH)
    df.to_csv(raw_csv_path, index=False)
    logger.info(f"✅ Data extracted from {RAW_DATA_PATH} to {raw_csv_path}")
    return str(raw_csv_path)

def preprocess(raw_csv_path):
    """Run the preprocessing script"""
    logger.info(f"Preprocessing data from {raw_csv_path}")
    
    # Define output path
    cleaned_data_path = str(PROCESSED_DIR / 'cleaned_data.csv')
    
    # Run the preprocessing script
    cmd = [
        sys.executable,
        str(PREPROCESS_SCRIPT),
        '--input', raw_csv_path,
        '--output', cleaned_data_path
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(result.stdout)
        
        if result.stderr:
            logger.warning(f"STDERR: {result.stderr}")
        
        logger.info(f"✅ Data preprocessed and saved to {cleaned_data_path}")
        return cleaned_data_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Preprocessing failed: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        sys.exit(1)

def train_model(cleaned_data_path):
    """Run the model training script"""
    logger.info(f"Training model with data from {cleaned_data_path}")
    
    # Run the training script
    cmd = [sys.executable, str(TRAIN_SCRIPT)]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(result.stdout)
        
        if result.stderr:
            logger.warning(f"STDERR: {result.stderr}")
        
        logger.info("✅ Model trained successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Model training failed: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        sys.exit(1)

def main():
    """Run the full ETL pipeline"""
    logger.info("Starting ETL pipeline")
    
    # Extract
    raw_csv_path = extract()
    
    # Preprocess
    cleaned_data_path = preprocess(raw_csv_path)
    
    # Train model
    train_model(cleaned_data_path)
    
    logger.info("✅ ETL pipeline completed successfully")

if __name__ == "__main__":
    main() 