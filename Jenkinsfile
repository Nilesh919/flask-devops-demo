pipeline {
    agent any

    environment {
        IMAGE_NAME = "9137102267/flask-devops-demo"
        IMAGE_TAG = "${BUILD_NUMBER}"
        RELEASE_NAME = "flask-app"
        HELM_PATH = "./helm/flask-devops-demo"
    }

    stages {

       stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                  credentialsId: 'dockerhub-creds',
                  usernameVariable: 'DOCKER_USER',
                  passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
        }
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
