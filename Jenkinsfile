pipeline {
    agent any

    environment {        
        GIT_CREDENTIALS = 'test'   
    }

    stages {
        stage('Execute All Steps on Remote Machine') {
            steps {
                script {
                    sshagent(['remote-ssh']) {
                        sh '''
                            ssh aipoc@172.30.20.35 '
                            # Checkout repository
                            mkdir -p /home/aipoc/genie-app
                            cd /home/aipoc/genie-app
                            git clone --branch ${gitBranch:-env.gitbranch} ${env.repositoryUrl} 
                            # Run Docker Container
                            docker rm -f genie-ai-container || true
                            docker compose up -d
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
