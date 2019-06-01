pipeline {
  agent {
    node {
      label 'jenkins-slave'
    }

  }
  stages {
    stage('Lint') {
      steps {
        sh 'dpkg -l pylint || ( apt update && apt install -y python pylint python-pip && pip install --upgrade pylint && pip install pylint_junit )'
        sh 'pylint --output-format=pylint_junit.JUnitReporter Infraero.py | tee Infraero.pylint.xml'
        junit(testResults: 'Infraero.pylint.xml', allowEmptyResults: true)
      }
    }
  }
}