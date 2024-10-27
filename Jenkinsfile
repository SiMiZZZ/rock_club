pipeline {
    agent any
    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/SiMiZZZ/rock_club.git'
            }
        }
        stage('Deploy') {
            steps {
                    sh 'docker compose up -d --build'
            }
        }
    }
}


