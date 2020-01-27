
pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/Fabio292/demo-jenkins.git'
      }
    }
    stage('Docker build') {
      steps {
        script {
          docker.build('fabio-demo')
        }
    
      }
    }
    stage('ECR push') {
      steps {
        script {
          docker.withRegistry('https://089058466443.dkr.ecr.eu-north-1.amazonaws.com', 'ecr:eu-north-1:AWS cred') {
            docker.image('089058466443.dkr.ecr.eu-north-1.amazonaws.com/fabio-demo').push('app-java')}
          }

        }
      }
    stage('Smartcheck') {
        steps {
          script {
            $FLAG = sh([ script: 'python /home/scAPI.py', returnStdout: true ]).trim()
            if ($FLAG != '1') {
              docker.withRegistry('https://089058466443.dkr.ecr.eu-north-1.amazonaws.com', 'ecr:eu-north-1:AWS cred') {
               docker.image('089058466443.dkr.ecr.eu-north-1.amazonaws.com/fabio-demo').push('app-java')} }
              }
                sh 'docker rmi $(docker images -q) -f 2> /dev/null'
              }

            }
          }
        }
     
    }
    
}
