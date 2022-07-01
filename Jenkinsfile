pipeline {
  agent { 
    dockerfile {
      additionalBuildArgs '--target test'
    }
  }
  stages {
    stage('Test') {
      steps {
        echo 'Agent built'
      }
    }
  }
}
