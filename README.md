# MLOps Project for Innovate Analytics Inc.

## Project Overview
This repository contains the end-to-end MLOps pipeline for Innovate Analytics Inc.'s cricket performance prediction system. The system processes cricket data to predict player performance using machine learning models.

## Architecture
- **Data Engineering**: Automated ETL pipeline using Apache Airflow
- **Data Versioning**: DVC for dataset version control
- **Model Training**: Scikit-learn models with MLflow tracking
- **CI/CD**: GitHub Actions for dev branch (linting, testing) and test branch (build, push)
- **Deployment**: Jenkins pipeline for Docker image creation and Kubernetes deployment
- **Monitoring**: Prometheus for real-time monitoring and metrics visualization

## Docker Optimization
The project has been optimized for efficient containerization:
- Multi-stage builds to reduce image size
- Consolidated containers to minimize resource usage
- Single Docker image for both prediction CLI and Streamlit UI
- Simplified Airflow setup with fewer containers
- Optimized monitoring stack

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker
- Docker Compose
- Kubernetes (Minikube for local development)
- Jenkins
- Apache Airflow

### Installation
1. Clone the repository
```bash
git clone https://github.com/iahmadraza7/Mlops-Project.git
cd Mlops-Project
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize project structure
```bash
python setup.py
```

5. Set up DVC
```bash
dvc init
dvc add data/raw/ODI_Cricket_Data.csv
```

### Running the Pipeline

#### Data Processing with DVC
```bash
# Run the full DVC pipeline
dvc repro

# Run specific stages
dvc repro extract
dvc repro preprocess
dvc repro train_model

# View metrics
dvc metrics show
```

#### Making Predictions
```bash
# Using the CLI directly
python src/predict_cli.py --strike-rate 90 --balls-faced 10000 --matches 200 --wins 120 --losses 80

# Using Docker
docker run -v $(pwd)/models:/app/models [image-name] predict --strike-rate 90 --balls-faced 10000 --matches 200 --wins 120 --losses 80

# Using Docker Compose
docker-compose run prediction predict --strike-rate 90 --balls-faced 10000 --matches 200 --wins 120 --losses 80
```

#### Running with Airflow
```bash
# Start Airflow standalone server
export AIRFLOW_HOME=$(pwd)/airflow
airflow standalone

# Access Airflow UI at http://localhost:8080
# Username: admin, Password: shown in terminal output

# Trigger DAG manually from the UI or CLI
airflow dags trigger cricket_etl
```

#### MLflow Tracking
```bash
# Start MLflow UI
mlflow ui --backend-store-uri ./mlflow

# Access MLflow UI at http://localhost:5000
```

#### Docker Setup

##### Using Docker Compose
```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down
```

##### Using Helper Script
```bash
# Make the script executable
chmod +x docker_ops.py

# Build the image
./docker_ops.py build

# Run the container
./docker_ops.py run

# Start with Docker Compose
./docker_ops.py compose-up -d
```

### Development Workflow
1. Create feature branch from `dev`
2. Make changes and commit
3. Create PR to merge into `dev` branch
4. Automated linting and testing via GitHub Actions
5. After approval, merge to `dev`
6. For releases, create PR from `dev` to `test`
7. After approval and testing, merge to `main` for production

### Project Organization
- Sprint planning managed through GitHub Issues (see `.github/workflows/sprint_planning.md`)
- Branch protection rules defined in `.github/BRANCH_PROTECTION.md`
- Comprehensive documentation in the `docs/` directory

## Deployment

### Local Kubernetes Deployment

The project includes comprehensive Kubernetes manifests for deployment on Minikube:

```bash
# Start Minikube
minikube start

# Deploy to local Kubernetes cluster
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Check deployment status
kubectl get deployments
kubectl get services
kubectl get pods

# Access the Streamlit UI
minikube service mlops-prediction-service

# Run prediction CLI within a pod
kubectl exec -it $(kubectl get pods -l app=mlops-prediction -o name | head -n1) -- /app/entrypoint.sh predict --strike-rate 90 --balls-faced 10000 --matches 200 --wins 120 --losses 80
```

#### Windows Users

For Windows users with PowerShell:

```powershell
# Start Minikube
minikube start --driver=docker

# Deploy to local Kubernetes cluster
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Access the Streamlit UI
minikube service mlops-prediction-service
```

### CI/CD Pipeline
The project uses Jenkins for CI/CD:
1. Code is pushed to the repository
2. Jenkins pipeline triggers automatically
3. Code is linted and tested
4. Docker image is built and scanned for vulnerabilities
5. Image is pushed to Docker Hub
6. Kubernetes manifests are applied for deployment

## Testing
```bash
# Run all tests
pytest

# Run specific test files
pytest tests/test_data_processing.py
pytest tests/test_model.py
pytest tests/test_integration.py

# Run Docker container tests
python tests/test_docker.py
```

## Monitoring
The project includes a monitoring stack:

- **Prometheus**: Metrics collection (http://localhost:9090)
- **Streamlit Dashboard**: Interactive visualization (http://localhost:8501)

## Security
The project includes several security measures:

- Regular dependency scanning with Safety
- Static code analysis with Bandit
- Container image scanning with Trivy
- Secret detection with Gitleaks
- All implemented in CI/CD pipeline

## Project Structure
- `src/`: Source code for model training and prediction
  - `preprocess.py`: Data preprocessing script
  - `train_model.py`: Model training script
  - `predict_cli.py`: Command-line prediction tool
- `data/`: Raw and processed datasets (managed by DVC)
- `models/`: Trained model artifacts
- `airflow/`: Airflow DAGs for data pipelines
- `k8s/`: Kubernetes deployment configurations
- `mlflow/`: MLflow experiment tracking
- `.github/`: CI/CD workflows and templates
- `monitoring/`: Prometheus configuration
- `tests/`: Unit and integration tests
- `docs/`: Project documentation
- `docker-compose.yml`: Multi-service Docker setup