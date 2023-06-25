import json
import requests
import re
import urllib.parse

HOST = "{{ host }}"
USERNAME = "{{ username }}"
PASSWORD = "{{ password }}"


def authenticate(
    session: requests.Session, username: str = None, password: str = None
) -> requests.Response:
    data = {"j_username": username, "j_password": password, "from": "/"}

    return session.post(f"{HOST}/j_spring_security_check", data=data)


def get_jenkins_crumb(session: requests.Session) -> str:
    response = session.get(f"{HOST}/view/all/newJob")
    pattern = r'data-crumb-value="([^"]+)"'
    match = re.search(pattern, response.text)

    if match is None:
        raise RuntimeError("Failed to parse Jenkins-Crumb value")

    return match.group(1)


def create_item(session: requests.Session, name: str) -> requests.Response:
    data = {
        "name": name,
        "mode": "org.jenkinsci.plugins.workflow.job.WorkflowJob",
        "Jenkins-Crumb": get_jenkins_crumb(session),
        "from": "",
    }

    data["json"] = json.dumps(data)

    return session.post(f"{HOST}/view/all/createItem", data=data)


def configure_item(
    session: requests.Session,
    name: str,
    repo_url: str,
    description: str = "",
) -> requests.Response:
    jenkins_crumb = get_jenkins_crumb(session)

    raw_request = (
        f"enable=true&description={urllib.parse.quote(description)}&"
        "stapler-class-bag=true&_.daysToKeepStr=&_.numToKeepStr=&_.artifactDaysToKeepStr=&_.artifactNumToKeepStr=&"
        "stapler-class=hudson.tasks.LogRotator&%24class=hudson.tasks.LogRotator&hint=MAX_SURVIVABILITY&_.buildCount=1&_.count=1&_.durationName=second&"
        "stapler-class-bag=true&_.upstreamProjects=&ReverseBuildTrigger.threshold=SUCCESS&_.spec=&hudson-triggers-SCMTrigger=on&_.scmpoll_spec=H%2F5+*+*+*+*&quiet_period=5&authToken=&_.displayNameOrNull=&oldScript=&_.script=&_.sandbox=on&"
        "stapler-class=org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition&%24class=org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition&"
        f"stapler-class=hudson.scm.NullSCM&%24class=hudson.scm.NullSCM&_.url={urllib.parse.quote(repo_url)}&includeUser=false&_.credentialsId=&_.name=&_.refspec=&_.name=*%2Fmain&"
        "stapler-class=hudson.plugins.git.browser.AssemblaWeb&%24class=hudson.plugins.git.browser.AssemblaWeb&"
        "stapler-class=hudson.plugins.git.browser.FisheyeGitRepositoryBrowser&%24class=hudson.plugins.git.browser.FisheyeGitRepositoryBrowser&"
        "stapler-class=hudson.plugins.git.browser.KilnGit&%24class=hudson.plugins.git.browser.KilnGit&"
        "stapler-class=hudson.plugins.git.browser.TFS2013GitRepositoryBrowser&%24class=hudson.plugins.git.browser.TFS2013GitRepositoryBrowser&"
        "stapler-class=hudson.plugins.git.browser.BitbucketServer&%24class=hudson.plugins.git.browser.BitbucketServer&"
        "stapler-class=hudson.plugins.git.browser.BitbucketWeb&%24class=hudson.plugins.git.browser.BitbucketWeb&"
        "stapler-class=hudson.plugins.git.browser.CGit&%24class=hudson.plugins.git.browser.CGit&"
        "stapler-class=hudson.plugins.git.browser.GitBlitRepositoryBrowser&%24class=hudson.plugins.git.browser.GitBlitRepositoryBrowser&"
        "stapler-class=hudson.plugins.git.browser.GithubWeb&%24class=hudson.plugins.git.browser.GithubWeb&"
        "stapler-class=hudson.plugins.git.browser.Gitiles&%24class=hudson.plugins.git.browser.Gitiles&"
        "stapler-class=hudson.plugins.git.browser.GitLab&%24class=hudson.plugins.git.browser.GitLab&"
        "stapler-class=hudson.plugins.git.browser.GitList&%24class=hudson.plugins.git.browser.GitList&"
        "stapler-class=hudson.plugins.git.browser.GitoriousWeb&%24class=hudson.plugins.git.browser.GitoriousWeb&"
        "stapler-class=hudson.plugins.git.browser.GitWeb&%24class=hudson.plugins.git.browser.GitWeb&"
        "stapler-class=hudson.plugins.git.browser.GogsGit&%24class=hudson.plugins.git.browser.GogsGit&"
        "stapler-class=hudson.plugins.git.browser.Phabricator&%24class=hudson.plugins.git.browser.Phabricator&"
        "stapler-class=hudson.plugins.git.browser.RedmineWeb&%24class=hudson.plugins.git.browser.RedmineWeb&"
        "stapler-class=hudson.plugins.git.browser.RhodeCode&%24class=hudson.plugins.git.browser.RhodeCode&"
        "stapler-class=hudson.plugins.git.browser.Stash&%24class=hudson.plugins.git.browser.Stash&"
        "stapler-class=hudson.plugins.git.browser.ViewGitWeb&%24class=hudson.plugins.git.browser.ViewGitWeb&"
        "stapler-class=hudson.plugins.git.GitSCM&%24class=hudson.plugins.git.GitSCM&_.scriptPath=Jenkinsfile&_.lightweight=on&"
        f"stapler-class=org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition&%24class=org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition&Submit=&core%3Aapply=&Jenkins-Crumb={jenkins_crumb}&json="
    )

    json_data = {
        "enable": True,
        "description": description,
        "properties": {
            "stapler-class-bag": "true",
            "jenkins-model-BuildDiscarderProperty": {
                "specified": False,
                "": "0",
                "strategy": {
                    "daysToKeepStr": "",
                    "numToKeepStr": "",
                    "artifactDaysToKeepStr": "",
                    "artifactNumToKeepStr": "",
                    "stapler-class": "hudson.tasks.LogRotator",
                    "$class": "hudson.tasks.LogRotator",
                },
            },
            "org-jenkinsci-plugins-workflow-job-properties-DisableConcurrentBuildsJobProperty": {
                "specified": False,
                "abortPrevious": False,
            },
            "org-jenkinsci-plugins-workflow-job-properties-DisableResumeJobProperty": {
                "specified": False
            },
            "org-jenkinsci-plugins-workflow-job-properties-DurabilityHintJobProperty": {
                "specified": False,
                "hint": "MAX_SURVIVABILITY",
            },
            "org-jenkinsci-plugins-pipeline-modeldefinition-properties-PreserveStashesJobProperty": {
                "specified": False,
                "buildCount": "1",
            },
            "hudson-model-ParametersDefinitionProperty": {"specified": False},
            "jenkins-branch-RateLimitBranchProperty$JobPropertyImpl": {},
            "org-jenkinsci-plugins-workflow-job-properties-PipelineTriggersJobProperty": {
                "triggers": {
                    "stapler-class-bag": "true",
                    "hudson-triggers-SCMTrigger": {
                        "scmpoll_spec": "H/5 * * * *",
                        "ignorePostCommitHooks": False,
                    },
                }
            },
        },
        "hasCustomQuietPeriod": False,
        "quiet_period": "5",
        "displayNameOrNull": "",
        "": "1",
        "definition": {
            "oldScript": "",
            "": "1",
            "scm": {
                "userRemoteConfigs": {
                    "url": repo_url,
                    "includeUser": "false",
                    "credentialsId": "",
                    "name": "",
                    "refspec": "",
                },
                "branches": {"name": "*/main"},
                "": "auto",
                "stapler-class": "hudson.plugins.git.GitSCM",
                "$class": "hudson.plugins.git.GitSCM",
            },
            "scriptPath": "Jenkinsfile",
            "lightweight": True,
            "stapler-class": "org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition",
            "$class": "org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition",
        },
        "Submit": "",
        "core:apply": "",
        "Jenkins-Crumb": jenkins_crumb,
    }

    raw_request += urllib.parse.quote(json.dumps(json_data))

    return session.post(
        f"{HOST}/job/{name}/configSubmit",
        data=raw_request,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def validate(response: requests.Response):
    if response.status_code >= 400:
        print(response.headers)
        print(response.text)
        raise RuntimeError(response.text)


def main():
    session = requests.Session()
    session.get(HOST)

    pipeline = "demo-app"

    validate(authenticate(session, username=USERNAME, password=PASSWORD))

    validate(create_item(session, name=pipeline))

    validate(
        configure_item(
            session,
            name=pipeline,
            repo_url="http://gitea-http.gitea.svc:3000/main/demo-app.git",
            description="Demo application pipeline",
        )
    )

    print("Done!")


if __name__ == "__main__":
    main()
