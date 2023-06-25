import requests

HOST = "{{ host }}"
USERNAME = "{{ username }}"
PASSWORD = "{{ password }}"


def authenticate(
    session: requests.Session, username: str = None, password: str = None
) -> requests.Response:
    data = {
        "_csrf": session.cookies.get("_csrf"),
        "user_name": username,
        "password": password,
    }

    return session.post(f"{HOST}/user/login", data=data)


def create_org(session: requests.Session, name: str) -> requests.Response:
    data = {
        "_csrf": session.cookies.get("_csrf"),
        "org_name": name,
        "visibility": 0,
        "repo_admin_change_team_access": "on",
    }

    return session.post(f"{HOST}/org/create", data=data)


def add_member(session: requests.Session, org: str, username: str) -> requests.Response:
    data = {"_csrf": session.cookies.get("_csrf"), "uid": 1, "uname": username}
    return session.post(f"{HOST}/org/{org}/teams/owners/action/add", data=data)


def create_user(
    session: requests.Session, username: str, password: str
) -> requests.Response:
    data = {
        "_csrf": session.cookies.get("_csrf"),
        "login_type": "0-0",
        "visibility": 0,
        "login_name": "",
        "user_name": username,
        "email": f"{username}@gitea.local",
        "password": password,
    }

    return session.post(f"{HOST}/admin/users/new", data=data)


def create_repo(session: requests.Session, name: str) -> requests.Response:
    data = {
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

    return session.post(f"{HOST}/repo/create", data=data)


def validate(response: requests.Response):
    if response.status_code >= 400:
        print(response.headers)
        print(response.text)
        raise RuntimeError(response.text)


def main():
    session = requests.Session()
    session.get(HOST)

    validate(authenticate(session, username=USERNAME, password=PASSWORD))
    validate(create_org(session, name="main"))

    validate(create_repo(session, "gitops"))
    validate(create_repo(session, "demo-app"))

    validate(create_user(session, username="gitops", password="gitops"))
    validate(add_member(session, org="main", username="gitops"))

    print("Done!")


if __name__ == "__main__":
    main()
