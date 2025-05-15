#!/bin/bash
set -e

if [ "$1" = "api" ]; then
    echo "Starting Flask API..."
    python src/app.py
elif [ "$1" = "predict" ]; then
    echo "Running prediction CLI..."
    if [ "$#" -eq 1 ]; then
        echo "Error: Missing prediction arguments"
        echo "Usage: docker run <image> predict --strike-rate <value> --balls-faced <value> --matches <value> --wins <value> --losses <value>"
        exit 1
    fi
    shift
    python src/predict_cli.py "$@"
elif [ "$1" = "streamlit" ]; then
    echo "Starting Streamlit UI..."
    streamlit run app_streamlit.py --server.port=8501 --server.address=0.0.0.0
elif [ "$1" = "mlflow" ]; then
    echo "Starting MLflow UI..."
    mlflow ui --backend-store-uri $MLFLOW_TRACKING_URI
elif [ "$1" = "dvc" ]; then
    echo "Running DVC command..."
    shift
    bash run_dvc.sh "$@"
else
    echo "Unknown command. Options: predict, api, streamlit, mlflow, dvc"
    echo "For prediction usage: docker run <image> predict --strike-rate <value> --balls-faced <value> --matches <value> --wins <value> --losses <value>"
    exit 1
fi 