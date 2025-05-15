.PHONY: setup clean test lint format docker-build docker-run dvc-run mlflow airflow k8s-deploy

# Default environment variables
PYTHON := python
PIP := pip
DOCKER_REPO := iahmadraza7
IMAGE_NAME := mlops-app
TAG := latest
PORT := 5000

# Setup targets
setup:
	$(PYTHON) setup.py
	$(PIP) install -r requirements.txt
	dvc init

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm -rf build dist *.egg-info

# Testing and linting
test:
	pytest tests/

lint:
	flake8 src/ tests/

format:
	black src/ tests/

# Data processing
preprocess:
	$(PYTHON) src/preprocess.py

train:
	$(PYTHON) src/train_model.py

predict:
	$(PYTHON) src/predict_cli.py --strike-rate 90 --balls-faced 10000 --matches 200 --wins 120 --losses 80

dvc-run:
	dvc repro

# Docker operations
docker-build:
	docker build -t $(DOCKER_REPO)/$(IMAGE_NAME):$(TAG) .

docker-run:
	docker run -p $(PORT):5000 $(DOCKER_REPO)/$(IMAGE_NAME):$(TAG)

docker-push:
	docker push $(DOCKER_REPO)/$(IMAGE_NAME):$(TAG)

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

# MLflow
mlflow:
	mlflow ui --backend-store-uri ./mlflow

# Airflow
airflow-init:
	export AIRFLOW_HOME=$(PWD)/airflow && airflow db init

airflow-start:
	export AIRFLOW_HOME=$(PWD)/airflow && airflow standalone

# Kubernetes
k8s-deploy:
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml

k8s-delete:
	kubectl delete -f k8s/service.yaml
	kubectl delete -f k8s/deployment.yaml

# Run full pipeline
run-pipeline: preprocess train mlflow

# Run Docker test
docker-test:
	$(PYTHON) tests/test_docker.py

# Help
help:
	@echo "Available targets:"
	@echo "  setup         - Initialize project and install dependencies"
	@echo "  clean         - Remove cache and temporary files"
	@echo "  test          - Run tests"
	@echo "  lint          - Run linter"
	@echo "  format        - Format code"
	@echo "  preprocess    - Run data preprocessing"
	@echo "  train         - Train the model"
	@echo "  predict       - Make a prediction with sample data"
	@echo "  dvc-run       - Run DVC pipeline"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-run    - Run Docker container"
	@echo "  docker-push   - Push Docker image to registry"
	@echo "  docker-compose-up   - Start services with Docker Compose"
	@echo "  docker-compose-down - Stop services with Docker Compose"
	@echo "  mlflow        - Start MLflow UI"
	@echo "  airflow-init  - Initialize Airflow"
	@echo "  airflow-start - Start Airflow standalone server"
	@echo "  k8s-deploy    - Deploy to Kubernetes"
	@echo "  k8s-delete    - Delete from Kubernetes"
	@echo "  run-pipeline  - Run the full pipeline"
	@echo "  docker-test   - Run Docker container tests" 