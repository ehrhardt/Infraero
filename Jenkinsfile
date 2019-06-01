pipeline {
  agent {
    node {
      label 'jenkins-slave'
    }
    
  }
  stages {
    stage('lint') {
      steps {
        sh 'dpkg -l pylint || ( apt update && apt install -y python pylint )'
        sh 'pylint Infraero.py'
      }
    }
  }
}
