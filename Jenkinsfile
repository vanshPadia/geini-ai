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
                            git clone --branch ${gitBranch:-master} ${repositoryUrl} . || (cd /home/aipoc/genie-app && git fetch && git checkout ${gitBranch:-master} && git pull)

                            # Build Docker Image
                            docker build -t genie-ai-image:latest .                           

                            # Run Docker Container
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
