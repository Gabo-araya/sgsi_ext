pipeline {
  agent any
  options {
    // Disable concurrent builds to avoid Docker from leaving dangling networks
    disableConcurrentBuilds()
  }
  environment {
    PROJECT_REPONAME = 'project-name-placeholder'
    SHORT_COMMIT = "${GIT_COMMIT[0..7]}"
    DOCKER_BUILDKIT = '1'
    COMPOSE_DOCKER_CLI_BUILD = '1'
    COMPOSE_FILE = 'docker/docker-compose.jenkins.yml'
    COMPOSE_PROJECT_NAME = "${PROJECT_REPONAME}-${env.SHORT_COMMIT}"
  }
  stages {
    stage('Build image') {
      steps {
        sh(script: 'docker-compose build', label: 'Build images')
        sh(script: 'docker-compose pull', label: 'Pull images')
      }
    }
    stage('Run code checks') {
      stages {
        stage('Check code formatting') {
          steps {
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
              sh '''docker-compose run app-test poetry run black --check .'''
            }
          }
        }
        stage('Check import sorting') {
          steps {
            catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
              sh 'docker-compose run app-test poetry run isort --check .'
            }
          }
        }
      }
    }
    stage('Run tests') {
      environment {
        COLLECTOR_CONTAINER_ID = """${sh(returnStdout: true, script:'docker-compose run -d --user root artifact-collector').trim()}"""
      }
      steps {
        sh 'docker-compose run app-test poetry run pytest --cov --cov-report=html:test-results/coverage --cov-report=xml:test-results/coverage.xml --cov-report=term'
        dir ('artifacts') {
          sh "docker cp \"${env.COLLECTOR_CONTAINER_ID}\":/artifacts/. ."
          sh "ls -l"
        }
      }
    }
  }
  post {
    always {
      sh 'docker-compose down -v'
      junit 'artifacts/pytest.xml'
      cobertura coberturaReportFile: 'artifacts/coverage.xml'
      archiveArtifacts allowEmptyArchive: true, artifacts: 'artifacts/*, artifacts/**', fingerprint: true
      cleanWs(
        deleteDirs: true,
        disableDeferredWipeout: true,
        notFailBuild: true,
      )
    }
  }
}
