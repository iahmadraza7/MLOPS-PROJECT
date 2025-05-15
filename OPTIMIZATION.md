# MLOps Project Optimization

## Project Redesign: From API to Direct Prediction

The project has been redesigned to use direct prediction instead of an API-based approach:

- **Before**: Flask API serving predictions via HTTP endpoints
- **After**: Direct command-line interface for predictions

This change provides several benefits:
1. **Simplified Architecture**: Removed HTTP layer complexity
2. **Lower Latency**: Direct model access without network overhead
3. **Easier Testing**: CLI tool can be tested without HTTP mocking
4. **Better Batch Processing**: Can be integrated into data pipelines

## Docker Optimization

The project has been optimized to use fewer Docker images and reduce complexity:

### 1. Container Consolidation

- **Before**: Separate containers for API, Streamlit, Grafana, Prometheus, cAdvisor, and Node-exporter
- **After**: Consolidated to just 4 main containers:
  - Prediction container (also serving Streamlit)
  - MLflow container
  - Postgres container (for Airflow)
  - Prometheus container (for monitoring)

### 2. Image Size Reduction

- Using multi-stage builds to reduce final image size
- Consolidating dependencies to avoid duplication
- Removing redundant Dockerfile.streamlit by enhancing the main Dockerfile

### 3. Airflow Simplification

- Consolidated Airflow services into a single container
- Combined webserver, scheduler, and initialization
- Improved resource utilization

### 4. Monitoring Stack Optimization

- Removed redundant monitoring containers
- Focused on essential metrics collection with Prometheus
- Eliminated cAdvisor and Node-exporter to reduce complexity

### 5. Kubernetes Configuration Updates

- Updated Kubernetes deployment to use CLI-based prediction
- Simplified service configuration
- Added volume mounts for model persistence
- Improved resource specifications

### 6. Requirements Optimization

- Removed duplicate dependencies in requirements.txt
- Created separate requirements-airflow.txt for Airflow-specific dependencies
- Fixed missing package references

## Performance Benefits

These optimizations provide the following benefits:

1. **Reduced Resource Usage**: Fewer containers means less memory and CPU overhead
2. **Faster Startup Time**: Simplified stack reduces startup dependencies
3. **Improved Maintainability**: Fewer components to manage and troubleshoot
4. **Better Developer Experience**: Simplified Docker commands and configuration
5. **Smaller Storage Footprint**: Optimized images consume less disk space

## Running the Optimized Stack

Use the following commands to run the optimized stack:

```bash
# Run the main stack
docker-compose up -d

# Make predictions using the CLI
docker-compose run prediction predict --strike-rate 90 --balls-faced 10000 --matches 200 --wins 120 --losses 80

# Run Airflow stack separately if needed
docker-compose -f docker-compose-airflow.yml up -d
``` 