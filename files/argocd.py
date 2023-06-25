from urllib.parse import urljoin
import requests


HOST = "https://argocd-server.argocd.svc:443"
USERNAME = "admin"
PASSWORD = "{{ password }}"


class ArgoCD:
    host: str

    def __init__(self, host: str, **kwargs):
        self.session = requests.Session(**kwargs)
        self.session.verify = False
        self.session.get(host)
        self.host = host
        self._kwargs = kwargs

    def get_url(self, path: str) -> str:
        return urljoin(self.host, path)

    def auth(self, username: str, password: str) -> requests.Response:
        data = {"username": username, "password": password}
        return self.session.post(
            self.get_url("/api/v1/session"), json=data, **self._kwargs
        )

    def create_application(
        self, name: str, namespace: str, repo_url: str, repo_path: str = "."
    ) -> requests.Response:
        data = {
            "apiVersion": "argoproj.io/v1alpha1",
            "kind": "Application",
            "metadata": {"name": name},
            "spec": {
                "destination": {
                    "name": "",
                    "namespace": namespace,
                    "server": "https://kubernetes.default.svc",
                },
                "source": {
                    "path": repo_path,
                    "repoURL": repo_url,
                    "targetRevision": "HEAD",
                },
                "sources": [],
                "project": "default",
                "syncPolicy": {"automated": {"prune": True, "selfHeal": True}},
            },
        }

        return self.session.post(
            self.get_url("/api/v1/applications"), json=data, **self._kwargs
        )


def validate(response: requests.Response):
    if response.status_code > 200:
        print(response.headers)
        print(response.text)
        raise RuntimeError(response.text)


def main():
    argo = ArgoCD(HOST)

    validate(argo.auth(USERNAME, PASSWORD))
    argo.create_application(
        "demo", "demo-app", "http://gitea-http.gitea.svc:3000/main/gitops.git"
    )

    print("Done!")


if __name__ == "__main__":
    main()
