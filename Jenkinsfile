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
            docker.image('089058466443.dkr.ecr.eu-north-1.amazonaws.com/fabio-demo').push('test')}
          }

        }
      }
      stage('Smart Check scan') {
        steps {
            script {
                smartcheckScan([
                imageName: "089058466443.dkr.ecr.eu-north-1.amazonaws.com/fabio-demo/test",
                smartcheckHost: "a53bcb22c40af11eaacb70ae5ec6da6f-1483260547.us-east-1.elb.amazonaws.com",
                insecureSkipRegistryTLSVerify: true,
                smartcheckCredentialsId: "SC cred",
                
            ])
            }
        }
      }

}
