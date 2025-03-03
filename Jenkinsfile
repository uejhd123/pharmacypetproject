pipeline {

    agent any

    stages {
        stage("run") {
            steps {
                sh 'docker compose down -d'
                sh 'docker compose up -d'
            }
        }
    }

}