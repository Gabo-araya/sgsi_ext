# Jenkins

Jenkins is an automation server that can be used to streamline testing and deployment on a project. DPT already has the configurations necessary to make Jenkins know how to handle this project thanks to the provided Jenkins file, so the only thing left is to set up the server.

## Setting up Jenkins.

First make sure that the necessary `Jenkinsfile` is already on the root folder of your repository, if you based your project on DPT it should already be there.

To set up automatic testing on your repository you have to follow these steps:

1. Log in to https://jenkins.do.magnet.cl/ using your magnet email.
2. On your dashboard click on **New Item** on the top left corner.
3. Enter a unique name for your Pipeline, a simple name would be following the structure `<organization>-<project>` e.g. `jenkins-test`

> Jenkins uses the name of the Pipeline to create directories on disk. Pipeline names which include spaces may uncover bugs in scripts which do not expect paths to contain spaces.

5. Select the **Multibranch Pipeline** option and click **OK**.
4. On the section **Display Name** of the configuration form enter a more readable name for your project. This name is how the project is going to appear on the Jenkins dashboard and GUI.
6. On the section **Branch Sources** click on **Add source** and select the option that fits your repository.
    - If you selected **Bitbucket** then fill the **Owner** space with the **Bitbucket Team** or **Bitbucket User Account** of your repository, in  the case of Magnet the owner would be `magnet-cl`. Then in **Credentials** select the option `magnet-cl@Bitbucket`. Lastly select your **Repository Name** in the dropdown list.
7. On the section **Properties** set the **Registry credentials** as `magnet-cl@Bitbucket`.
8. Press **Save** at the bottom of the page.

Now your repository should be running tests on each of your branches!
