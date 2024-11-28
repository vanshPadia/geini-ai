pipeline {
    agent any

    environment {        
        GIT_CREDENTIALS = 'test'         
    }

    stages {
        stage('Checkout') {
            steps {
                script {                    
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: env.gitBranch]],
                        userRemoteConfigs: [[
                            url: env.repositoryUrl,
                            credentialsId: GIT_CREDENTIALS  
                        ]]
                    ])
                }
            }
        }

        stage('Build Docker and Save') {
            steps {
                script {
                    sh '''
                        docker build -t genie-ai-image:latest .
                        docker save -o genie-ai-image.tar genie-ai-image:latest
                    '''
                }
            }
        }

        stage('Reload Docker Image') {
            steps {
                script {
                    sh '''
                        docker load < genie-ai-image.tar
                    '''
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh '''
                        docker rm -f genie-ai-container || true
                        docker run -d --name genie-ai-container -p 8000:8000 genie-ai-image
                    '''
                }
            }
        }
    }
}
