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
          docker.withRegistry('<https://089058466443.dkr.ecr.eu-north-1.amazonaws.com', 'ecr:eu-north-1:<credential_id>') {
            docker.image('089058466443.dkr.ecr.eu-north-1.amazonaws.com/fabio-demo').push(test)}
          }

        }
      }

        }
        environment {
          IMAGETAG = 'tomcat'
          HIGH = '1'
          MEDIUM = '5'
          LOW = '5'
          NEGLIGIBLE = '5'
          UNKNOWN = '5'
          USER = administrator	
          PASSWORD = <smartcheck_password>
        }
      }