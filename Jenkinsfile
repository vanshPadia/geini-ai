pipeline {
    agent any
    
    environment {        
        GIT_CREDENTIALS = 'git-vansh'   
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
        
        stage('Build docker') {
            steps {
                script {
                    sh '''
                        docker build -t genie-ai-image:latest . 
                    
                    '''
                    
                    }
                }
            }
        }
        
