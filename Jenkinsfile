pipeline {
    agent any
    
    environment {        
        GIT_CREDENTIALS = 'test'   
    }

    stages {
        stage('Checkout') {
            steps {
                script {                    
                    withFolderProperties {
                        checkout([
                            $class: 'GitSCM',
                            branches: [[name: env.gitBranch ?: 'master']],
                            userRemoteConfigs: [[
                                url: env.repositoryUrl,
                                credentialsId: GIT_CREDENTIALS  
                            ]]                          
                        ])
                    }
                }
            }
        }
        
        stage('Build Docker && save') {
            steps {
                script {                   
                    sh '''
                        docker build -t genie-ai-image:latest .
                        save -o genie-ai-image.tar genie-ai-image:latest
                    '''
                }
            }
        }
        stage('relode') {
            steps {
                script {                   
                    sh '''
                        docker load < genie-ai-image.tar
                    '''
                }
            }
        }
        stage('run docker') {
            steps {
                script {                   
                    sh '''
                        docker run -d --name genie-ai-container -p 8000:8000 genie-ai-image
                    '''
                }
            }
        }
    }
}
