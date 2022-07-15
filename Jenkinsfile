pipeline {
  agent any
  environment {
    PROJECT_REPONAME = 'django3-project-template'
    DOCKER_BUILDKIT = '1'
    COMPOSE_DOCKER_CLI_BUILD = '1'
  }
  stages {
    stage('Build test and production images') {
      steps {
        sh "docker build --progress=plain --target test -t \"${env.PROJECT_REPONAME}-test:${env.BUILD_NUMBER}\" ."
        sh "docker tag \"${env.PROJECT_REPONAME}-test:${env.BUILD_NUMBER}\" \"${env.PROJECT_REPONAME}-test:latest\""
      }
    }
    stage('Test') {
      steps {
        sh """
        CONTAINER_ID=\$(docker-compose -f docker/docker-compose.jenkins.yml run -d --user root artifact-collector)
        export COLLECTOR_CONTAINER_ID=\$CONTAINER_ID
        """
        sh '''docker-compose -f docker/docker-compose.jenkins.yml run app-test poetry run black --check --exclude \\""^.*\\b(migrations)\\b.*$"\\" .'''
        sh 'docker-compose -f docker/docker-compose.jenkins.yml run app-test poetry run isort --check .'
        sh 'docker-compose -f docker/docker-compose.jenkins.yml run app-test poetry run pytest'
      }
    }
  }
  post {
    always {
      sh 'docker-compose -f docker/docker-compose.jenkins.yml down -v'
    }
  }
}
