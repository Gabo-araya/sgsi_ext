pipeline {
  agent any
  environment {
    PROJECT_REPONAME = 'project-name-placeholder'
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
    stage('Run code checks') {
      stages {
        stage('Check code formatting') {
          steps {
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
              sh '''docker-compose -f docker/docker-compose.jenkins.yml run app-test poetry run black --check .'''
            }
          }
        }
        stage('Check import sorting') {
          steps {
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
              sh 'docker-compose -f docker/docker-compose.jenkins.yml run app-test poetry run isort --check .'
            }
          }
        }
      }
    }
    stage('Run tests') {
      environment {
        COLLECTOR_CONTAINER_ID = """${sh(returnStdout: true, script:'docker-compose -f docker/docker-compose.jenkins.yml run -d --user root artifact-collector').trim()}"""
      }
      steps {
        sh 'docker-compose -f docker/docker-compose.jenkins.yml run app-test poetry run pytest --cov --cov-report=html:test-results/coverage --cov-report=xml:test-results/coverage.xml --cov-report=term'
        dir ('artifacts') {
          sh "docker cp \"${env.COLLECTOR_CONTAINER_ID}\":/artifacts/. ."
          sh "ls -l"
        }
      }
    }
  }
  post {
    always {
      sh 'docker-compose -f docker/docker-compose.jenkins.yml down -v'
      junit 'artifacts/pytest.xml'
      cobertura coberturaReportFile: 'artifacts/coverage.xml'
      archiveArtifacts allowEmptyArchive: true, artifacts: 'artifacts/*, artifacts/**', fingerprint: true
    }
  }
}
