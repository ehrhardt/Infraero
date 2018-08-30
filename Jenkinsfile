pipeline {
  agent {
    node {
      label 'jenkins-slave'
    }
    
  }
  stages {
    stage('lint') {
      steps {
        sh 'apt update && apt install -y python pylint'
        sh 'pylint Infraero.py'
      }
    }
  }
}
