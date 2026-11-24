pipeline {
    agent any

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
    }

    post {
        success { echo '✅ Pipeline OK' }
        failure { echo '❌ Pipeline KO' }
        always  { cleanWs() }
    }
}
