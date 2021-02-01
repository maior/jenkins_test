pipeline {
    agent any
    triggers {
        pollSCM('*/1 * * * *')
    }
    stages {
        stage('Build') {
            steps {
                sh 'python app.py'
            }
        }
        stage('Test') {
            steps {
                sh 'python app.py'
            }
        }
        stage('Deploy') {
            steps {
                sh 'python --version'
            }
        }
    }
}
