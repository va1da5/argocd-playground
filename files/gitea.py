import requests

HOST = "http://gitea-http.gitea.svc:3000"
USERNAME = "gitea_admin"
PASSWORD = "Passw0rd!"


def authenticate(
    session: requests.Session, username: str = None, password: str = None
) -> requests.Response:
    params = {
        "_csrf": session.cookies.get("_csrf"),
        "user_name": username,
        "password": password,
    }

    return session.post(f"{HOST}/user/login", data=params)


def create_org(session: requests.Session, name: str) -> requests.Response:
    params = {
        "_csrf": session.cookies.get("_csrf"),
        "org_name": name,
        "visibility": 0,
        "repo_admin_change_team_access": "on",
    }

    return session.post(f"{HOST}/org/create", data=params)


def create_repo(session: requests.Session, name: str) -> requests.Response:
    params = {
        "_csrf": session.cookies.get("_csrf"),
        "uid": 2,
        "repo_name": name,
        "description": "",
        "repo_template": "",
        "issue_labels": "",
        "gitignores": "",
        "license": "",
        "readme": "Default",
        "default_branch": "main",
        "trust_model": "default",
    }

    return session.post(f"{HOST}/repo/create", data=params)


def validate(response: requests.Response):
    if response.status_code > 400:
        print(response.headers)
        print(response.text)
        raise RuntimeError(response.text)


def main():
    session = requests.Session()
    session.get(HOST)

    validate(authenticate(session, USERNAME, PASSWORD))
    validate(create_org(session, "main"))
    validate(create_repo(session, "gitops"))

    print("Done!")


if __name__ == "__main__":
    main()
