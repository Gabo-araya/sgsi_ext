import groovy.transform.Field

// Deployment definitions
@Field
def branchesConfig = [
  'release/0004': [
    inventory_name: 'staging',
    credentials_id: '910dbf9b-3658-41a2-83df-fa5fd5f7da4c'
  ],
  main: [
    inventory_name: 'production',
    credentials_id: '910dbf9b-3658-41a2-83df-fa5fd5f7da4c'
  ],
  fallback: [
    inventory_name: 'localhost',
    credentials_id: '910dbf9b-3658-41a2-83df-fa5fd5f7da4c'
  ]
]

def getConfigFromBranch(branch) {
  if (branchesConfig.containsKey(branch)) {
    return branchesConfig.get(branch)
  } else {
    return branchesConfig.get('fallback')
  }
}

pipeline {
  agent none
  options {
    // Disable concurrent builds to avoid Docker from leaving dangling networks
    disableConcurrentBuilds()
  }
  stages {
    stage('Build and test') {
      agent { label 'linux-docker' }
      environment {
        PROJECT_REPONAME = 'magnet-sgsi'
        SHORT_COMMIT = "${GIT_COMMIT[0..7]}"
        DOCKER_BUILDKIT = '1'
        COMPOSE_DOCKER_CLI_BUILD = '1'
        COMPOSE_FILE = "${WORKSPACE}/docker/docker-compose.jenkins.yml"
        COMPOSE_PROJECT_NAME = "${PROJECT_REPONAME}-${env.SHORT_COMMIT}-${env.CHANGE_ID ?: 0}-${env.BUILD_NUMBER}"
        HOST_GID = sh(script: "id -g", returnStdout: true).trim()
        HOST_UID = sh(script: "id -u", returnStdout: true).trim()
        WHO = 'magnet'
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
            sh(script: 'mkdir test-results', label: 'Create test results directory')
            warnError('Some code checks have failed') {
              sh(script: 'docker compose run --rm app-test poetry run pre-commit run --all-files', label: 'Run pre-commit hooks')
              sh(script: 'docker compose run --rm app-test poetry run ./manage.py makemigrations --check --dry-run', label: 'Check migrations')
              sh(script: 'docker compose run --rm app-test poetry run ./manage.py collectstatic --noinput', label: 'Collect static files')
              sh(script: 'docker compose run --rm app-test poetry run ./manage.py migrate', label: 'Apply migrations')
              sh(script: 'docker compose run --rm app-test poetry run ./manage.py updategroups --sync', label: 'Update groups')
              sh(script: 'docker compose run --rm app-test poetry run django-admin compilemessages', label: 'Check translations')
              sh(script: 'docker compose run --rm app-test npm run lint', label: 'Run node linters')
            }
          }
        }
        stage('Run tests') {
          steps {
            sh(
              script: 'docker compose run --rm app-test ' +
                'poetry run pytest ' +
                '--cov ' +
                '--cov-report=html:test-results/coverage ' +
                '--cov-report=xml:test-results/coverage.xml ' +
                '--cov-report=term',
              label: 'Run pytest'
            )
          }
          post {
            always {
              dir ('test-results') {
                sh(script: '[ -d "coverage" ] && tar czf coverage.tar.gz coverage/*; exit 0', label: 'Compress coverage results (if exists)')
                junit(testResults: 'pytest.xml', allowEmptyResults: true)
                // patch file to remove container paths
                sh(script: "sed -i 's/<source>\\/usr\\/src\\/app<\\/source>/<source>.<\\/source>/' coverage.xml", label: 'Patch coverage results')
                recordCoverage(sourceDirectories: [[path: '..']], tools: [[parser: 'COBERTURA', pattern: 'coverage.xml']])
                archiveArtifacts(
                  allowEmptyArchive: true,
                  artifacts: '*, **',
                  fingerprint: true
                )
              }
            }
          }
        }
      }
      post {
        always {
          sh(
            script: 'docker compose down -v',
            label: 'Tear down docker-compose environment'
          )
          cleanWs(
            deleteDirs: true,
            disableDeferredWipeout: true,
            notFailBuild: true,
          )
          dir("${env.WORKSPACE}@tmp") {
            deleteDir()
          }
          dir("${env.WORKSPACE}@script") {
            deleteDir()
          }
        }
      }
    }
    stage('Deploy') {
      when { anyOf { branch 'release/0004'; branch 'main' } }
      agent {
        docker {
          image 'python:3.10-bullseye'
          args '-u 0:0'
        }
      }
      environment {
        TARGET_HOST = getConfigFromBranch(env.BRANCH_NAME).get('inventory_name')
        ANSIBLE_SSH_ARGS = '-C -o ControlMaster=auto -o ControlPersist=60s -o BatchMode=yes'
        RUNNING_IN_CONTAINER = '1'
      }
      stages {
        stage('Prepare environment') {
          steps {
            sh(script: 'apt-get update && apt-get install -y jq', label: 'Install jq')
            sh(script: 'pip3 install "ansible-core==2.15.5" "yq==2.14.0" "jmespath==1.0.1"', label: 'Install Ansible, yq & jmespath')
            sh(
              script: 'ansible-galaxy install -r requirements.yml',
              label: 'Install required Ansible collections'
            )
            withCredentials(
              [
                sshUserPrivateKey(
                  credentialsId: getConfigFromBranch(env.BRANCH_NAME).get('credentials_id'),
                  keyFileVariable: 'deployKey',
                  usernameVariable: 'deployUser'
                )
              ]
            ) {
              sh(
                script: 'mkdir -p ~/.ssh && cp $deployKey ~/.ssh/id_rsa',
                label: 'Store deploy key'
              )
            }
            sh(
                script: './.jenkins/copy_ssh_host_keys.sh',
                label: 'Load remote host keys'
            )
          }
        }
        stage('Run deployment') {
          environment {
            ANSIBLE_INVENTORY = 'inventory.yml'
          }
          steps {
            sh(
              script: "./ansible/update.sh ${env.TARGET_HOST}",
              label: 'Run deploy tasks'
            )
          }
        }
      }
      post {
        always {
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
  }
}
