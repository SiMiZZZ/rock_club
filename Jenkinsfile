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
                    sh 'sudo docker compose up -d --build'
            }
        }
    }
}


