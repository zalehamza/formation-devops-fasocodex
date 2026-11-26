pipeline {
    agent any

    environment {
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
                    docker build -t fasocodex/finance-service-portal:$VERSION \
                                 -t fasocodex/finance-service-portal:latest .
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
                        docker push zalehamza/finance-service-portal:$VERSION
                        docker push zalehamza/finance-service-portal:latest
                    '''
                }
            }
        }
    }

    post {
        success { echo "✅ Pipeline OK — version $VERSION" }
        failure { echo '❌ Pipeline KO' }
        always  {
            sh 'docker logout || true'
            cleanWs()
        }
    }
}
