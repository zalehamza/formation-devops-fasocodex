pipeline {
    agent any

    environment {
        IMAGE   = 'zalehamza/finance-service-portal'
        VERSION = '1.0.0'
    }

    stages {
        stage('Hello') {
            steps {
                echo 'Hello FasoCodex 👋'
            }
        }

        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -q pytest ruff
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '. venv/bin/activate && ruff check .'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest -v'
            }
        }

        stage('Build image') {
            steps {
                sh '''
                    docker build -t $IMAGE:$VERSION .
                '''
            }
        }

        stage('Push Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh '''
                        echo "$PASS" | docker login -u "$USER" --password-stdin
                        docker push $IMAGE:$VERSION
                        docker push $IMAGE:latest
                    '''
                }
            }
        }
    }

    post {
        success { echo "✅ Pipeline OK — $IMAGE:$VERSION" }
        failure { echo '❌ Pipeline KO' }
        always  {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}
