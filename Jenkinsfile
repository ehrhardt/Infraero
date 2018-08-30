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
        sh 'python --version'
        sh '''pylint Infraero.py
'''
      }
    }
  }
}