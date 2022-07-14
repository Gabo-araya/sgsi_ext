pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh 'docker-compose -f docker/docker-compose.jenkins.yml run django poetry run pytest'
      }
    }
  }
  post {
    always {
      sh 'docker-compose -f docker/docker-compose.jenkins.yml down -v'
    }
  }
}
