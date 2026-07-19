pipeline {
    agent any

    environment {
        IMAGE_NAME = "nilesh/flask-devops-demo"
        IMAGE_TAG = "${BUILD_NUMBER}"
        RELEASE_NAME = "flask-app"
        HELM_PATH = "./helm/flask-devops-demo"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/your-username/flask-devops-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Deploy using Helm') {
            steps {
                sh """
                helm upgrade --install ${RELEASE_NAME} ${HELM_PATH} \
                --set image.repository=${IMAGE_NAME} \
                --set image.tag=${IMAGE_TAG}
                """
            }
        }

        stage('Verify Deployment') {
            steps {
                sh "kubectl rollout status deployment/${RELEASE_NAME}"
            }
        }
    }
}
