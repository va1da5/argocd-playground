# ArgoCD Playground Using Minikube

The purpose of this project is to set up a GitOps playground in Minikube using ArgoCD and Gitea. This allows users to easily test various scenarios. The deployment automation is achieved through the use of an Ansible playbook and custom Kubernetes jobs, which facilitate seamless integration between services.

## Prerequisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://minikube.sigs.k8s.io/docs/handbook/kubectl/)
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)
- [HELM](https://helm.sh/docs/intro/install/)

## Ansible

```bash
# install dependencies
pip install -r requirements.txt

# deploy ArgoCD + Gitea
ansible-playbook install.yml

# remove deployment
ansible-playbook destroy.yml
```

## References

- [ArgoCD Getting Started](https://argo-cd.readthedocs.io/en/stable/getting_started/)
- [ArgoCD Series: How to Install ArgoCD on a Single Node Minikube Cluster](https://mycloudjourney.medium.com/argocd-series-how-to-install-argocd-on-a-single-node-minikube-cluster-1d3a46aaad20)
- [Install and Configure Gitea Git Service on Kubernetes / OpenShift](https://computingforgeeks.com/install-gitea-git-service-on-kubernetes-openshift/)
- [Gitea Helm Chart](https://gitea.com/gitea/helm-chart/)
