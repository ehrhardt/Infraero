pipeline {
  agent any
  stages {
    stage('lint') {
      steps {
        sh '''#/usr/bin/bash

pylint Infraero.py'''
      }
    }
  }
}