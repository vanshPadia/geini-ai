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

        stage('Build Docker & Save Image') {
            steps {
                script {
                    sh '''
                        docker build -t genie-ai-image:latest .
                        docker save -o genie-ai-image.tar genie-ai-image:latest
                    '''
                }
            }
        }

        stage('Copy Image Tar to AIPOC Machine') {
            steps {
                script {
                    sshagent(['remote-ssh']) {                 
                        sh '''
                            scp genie-ai-image.tar aipoc@172.30.20.35:/home/aipoc/genie-app/container-registry/
                        '''
                    }
                }
            }
        }

        stage('Load Docker Image on AIPOC Machine') {
            steps {
                script {
                    sshagent(['remote-ssh']) {
                        sh '''
                            ssh aipoc@172.30.20.35 'docker load < /home/aipoc/genie-app/container-registry/genie-ai-image.tar'
                        '''
                    }
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sshagent(['remote-ssh']) {
                        sh '''
                            ssh aipoc@172.30.20.35 '
                            docker rm -f genie-ai-container || true
                            docker run -d --name genie-ai-container -p 8000:8000 genie-ai-image
                            '
                        '''
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution complete.'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed. Please check logs for more details.'
        }
    }
}
