# Automated deployment using Jenkins

The default Jenkins pipeline only performs automated unit testing and code linting, which is useful for most projects. For team convenience, it is also possible to perform automatic deployment using Jenkins.
As this requires pipeline changes, it is not provided as the default pipeline and requires further configuration.

## Getting started

1. Copy `docs/examples/Jenkinsfile.autodeploy` to the project root as `Jenkinsfile`, overwriting the existing file.
2. If you modified the existing pipeline, please apply the same modifications into the new pipeline.
3. In `branchesConfig`, define the branches the project should deploy automatically and the inventory names of the servers where to deploy to.
4. At line 115 (stage "Deploy" -> `when`), add any additional branch that should trigger a deployment in case of successful test execution.
5. Authorize the Jenkins deploy key in the target environments. Ask the DevOps staff for more information.
6. Define the SSH host key into the respective inventory entries under the `host_ssh_key` key.
7. Commit and merge into the destination branch.

DO NOT modify the credentials ID unless you know what are you doing. It determines the key Jenkins will use to connect to the remote machine.

With proper configuration it is possible to have a continuous deployment pipeline, freeing team members of infrastructure management.

When done correctly, the project will become a 2-stage pipeline:

* Test
* Deployment

The **Test** stage will always be performed regardless of the branch being processed. **Deployment** is only done for branches matching the `when` condition defined in the Jenkinsfile configuration.
