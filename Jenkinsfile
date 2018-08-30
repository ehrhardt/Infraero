pipeline {
  agent {
    node {
      label 'jenkins-slave'
    }
    
  }
  stages {
    stage('lint') {
      steps {
        sh 'python --version'
        sh 'cat /etc/*-release'
      }
    }
  }
}