pipeline {
  agent any
  
  environment {
    DOCKER_CREDS = credentials('dockerhub')
    IMAGE_NAME = "mlops-app"
    IMAGE_TAG = "${env.BUILD_NUMBER}"
    DOCKER_REPO = "iahmadraza7"
  }
  
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    
    stage('Lint & Test') {
      steps {
        sh 'pip install flake8 pytest'
        sh 'flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics'
        sh 'pytest tests/'
      }
    }
    
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t $DOCKER_REPO/$IMAGE_NAME:$IMAGE_TAG -t $DOCKER_REPO/$IMAGE_NAME:latest .'
      }
    }
    
    stage('Security Scan') {
      steps {
        sh 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image $DOCKER_REPO/$IMAGE_NAME:$IMAGE_TAG'
      }
    }
    
    stage('Push to Registry') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
          sh 'echo $PASS | docker login -u $USER --password-stdin'
          sh 'docker push $DOCKER_REPO/$IMAGE_NAME:$IMAGE_TAG'
          sh 'docker push $DOCKER_REPO/$IMAGE_NAME:latest'
        }
      }
    }
    
    stage('Deploy to Kubernetes') {
      steps {
        sh '''
          # Update Kubernetes deployment with new image
          sed -i "s|\\${DOCKER_USERNAME}/mlops-app:latest|$DOCKER_REPO/$IMAGE_NAME:$IMAGE_TAG|g" k8s/deployment.yaml
          
          # Apply Kubernetes manifests
          kubectl apply -f k8s/deployment.yaml
          kubectl apply -f k8s/service.yaml
          
          # Wait for deployment to complete
          kubectl rollout status deployment/mlops-app
        '''
      }
    }
  }
  
  post {
    always {
      // Clean up local Docker images
      sh 'docker rmi $DOCKER_REPO/$IMAGE_NAME:$IMAGE_TAG $DOCKER_REPO/$IMAGE_NAME:latest || true'
      cleanWs()
    }
    success {
      echo 'Build, test, and deployment completed successfully!'
    }
    failure {
      echo 'Pipeline failed! Check the logs for details.'
    }
  }
}