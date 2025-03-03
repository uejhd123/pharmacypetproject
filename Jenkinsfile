pipeline {
    agent any

    stages {
        stage("run") {
            agent {
                docker {
                    image "node:18-alpine"
                    reuseNode true
                }
            }
            steps {
                sh 'docker version'
            }
        }
    }
}