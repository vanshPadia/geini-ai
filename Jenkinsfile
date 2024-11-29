pipeline {
    agent any

    environment {        
        GIT_CREDENTIALS = 'test'
        repositoryUrl = 'https://github.com/vanshPadia/geini-ai.git' 
    }

    stages {
        stage('Deploy to Remote Server') {
            steps {
                script {
                    sshagent(['remote-ssh']) {  
                        sh '''
                            ssh aipoc@172.30.20.35 '
                            mkdir -p /home/aipoc/genie-app
                            cd /home/aipoc/genie-app
                            git clone --branch master ${repositoryUrl} .
                            
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
    }
}
