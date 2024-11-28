pipeline {
    agent any

    environment {
        GIT_CREDENTIALS = 'test'  // Jenkins credential ID for Git
        SSH_CREDENTIALS = 'remote-ssh' // Jenkins credential ID for SSH
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

        stage('Build Docker && Save') {
            steps {
                script {                   
                    sh '''
                        docker build -t genie-ai-image:latest .
                        docker save -o genie-ai-image.tar genie-ai-image:latest
                    '''
                }
            }
        }

        stage('Copy Image Tar to Remote Machine') {
            steps {
                sshPublisher(publishers: [
                    sshPublisherDesc(
                        configName: SSH_CREDENTIALS,
                        transfers: [
                            sshTransfer(
                                sourceFiles: 'genie-ai-image.tar',
                                remoteDirectory: '/home/aipoc/genie-app/container-registry'
                            )
                        ]
                    )
                ])
            }
        }

        stage('Reload Docker Image') {
            steps {
                sshCommand remote: [
                    name: 'remote-ssh',
                    host: '172.30.20.35',
                    user: 'aipoc',
                    credentialsId: SSH_CREDENTIALS
                ], command: '''
                    docker load < /home/aipoc/genie-app/container-registry/genie-ai-image.tar
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                sshCommand remote: [
                    name: 'remote-ssh',
                    host: '172.30.20.35',
                    user: 'aipoc',
                    credentialsId: SSH_CREDENTIALS
                ], command: '''
                    docker rm -f genie-ai-container || true
                    docker run -d --name genie-ai-container -p 8000:8000 genie-ai-image
                '''
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
