pipeline {
  agent { label 'linux-docker' }
  options {
    // Disable concurrent builds to avoid Docker from leaving dangling networks
    disableConcurrentBuilds()
  }
  environment {
    PROJECT_REPONAME = 'project-name-placeholder'
    SHORT_COMMIT = "${GIT_COMMIT[0..7]}"
    DOCKER_BUILDKIT = '1'
    COMPOSE_DOCKER_CLI_BUILD = '1'
    COMPOSE_FILE = "${WORKSPACE}/docker/docker-compose.jenkins.yml"
    COMPOSE_PROJECT_NAME = "${PROJECT_REPONAME}-${env.SHORT_COMMIT}-${env.CHANGE_ID ?: 0}-${env.BUILD_NUMBER}"
  }
  stages {
    stage('Build image') {
      steps {
        sh(script: 'docker compose build', label: 'Build images')
        sh(script: 'docker compose pull', label: 'Pull images')
      }
    }
    stage('Run code checks') {
      steps {
        warnError('Some code checks have failed') {
          sh(script: 'docker compose run app-test poetry run black --check .', label: 'Check code formatting')
          sh(script: 'docker compose run app-test poetry run ruff .', label: 'Check linting')
        }
      }
    }
    stage('Run tests') {
      steps {
        sh(
          script: 'docker compose up -d artifact-collector',
          label: 'Start artifact collector'
        )
        sh(
          script: 'docker compose ' +
            'run app-test poetry run pytest ' +
            '--cov ' +
            '--cov-report=html:test-results/coverage ' +
            '--cov-report=xml:test-results/coverage.xml ' +
            '--cov-report=term',
          label: 'Run pytest'
        )
      }
      post {
        always {
          dir ('artifacts') {
            sh(script: 'docker compose cp artifact-collector:/artifacts/. .', label: 'Copy test results')
            sh(script: 'ls -l', label: 'List copied files')
            sh(
              script: 'tar czf coverage.tar.gz coverage/*',
              label: 'Compress coverage results'
            )
          }
          junit(testResults: 'artifacts/pytest.xml', allowEmptyResults: true)
          cobertura coberturaReportFile: 'artifacts/coverage.xml'
          archiveArtifacts(
            allowEmptyArchive: true,
            artifacts: 'artifacts/*, artifacts/**',
            fingerprint: true
          )
        }
      }
    }
  }
  post {
    always {
      sh 'docker compose down -v'
      cleanWs(
        deleteDirs: true,
        disableDeferredWipeout: true,
        notFailBuild: true,
      )
      // Delete @tmp and @script directories
      dir("${env.WORKSPACE}@tmp") {
        deleteDir()
      }
      dir("${env.WORKSPACE}@script") {
        deleteDir()
      }
    }
  }
}
