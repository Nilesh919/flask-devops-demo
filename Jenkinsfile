pipeline {
    agent any

    environment {
        IMAGE_NAME   = "9137102267/flask-devops-demo"
        IMAGE_TAG    = "${BUILD_NUMBER}"
        RELEASE_NAME = "flask-app"
        HELM_PATH    = "./helm/flask-devops-demo"
    }

    stages {
        stage('Run Unit Tests') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip setuptools
                    pip install "Flask>=2.0.0" pytest
                    pytest
                '''
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('Helm Lint & Deploy') {
            steps {
                sh "helm lint ${HELM_PATH}"
                sh """
                helm upgrade --install ${RELEASE_NAME} ${HELM_PATH} \
                  --set image.repository=${IMAGE_NAME} \
                  --set image.tag=${IMAGE_TAG}
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                // Uses helm status to verify deployment rollout dynamically
                sh "kubectl rollout status deployment/${RELEASE_NAME}-flask-devops-demo || kubectl rollout status deployment/${RELEASE_NAME}"
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
            sh 'rm -rf venv'
        }
    }
}
