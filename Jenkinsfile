pipeline {
  agent any
  stages {
    stage('lint') {
      steps {
        sh 'pylint Infraero.py'
      }
    }
  }
}