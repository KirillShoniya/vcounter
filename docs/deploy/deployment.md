## Local

**Requires GitLab account**

#### Minikube

1. Install [minikube](https://minikube.sigs.k8s.io/docs/start/)
2. Start: ```minikube start```
3. Enable ingress: ```minikube addons enable ingress```

#### Configure remote registry 

1. Export environment variables:
    * ENV_GITLAB_REGISTRY_TOKEN - registry access token
    * ENV_GITLAB_REGISTRY_USERNAME - username
    * ENV_GITLAB_PROJECT_GROUP_NAME - project group name. It will use in Docker image name

3. Login to remote registry. E.g. Gitlab Registry:
    * ```docker login registry.gitlab.com -u <USERNAME> -p <TOKEN>```
4. Create secret that contains docker registry credentials:
    * ```kubectl create secret generic gitlab-registry-credentials --from-file=.dockerconfigjson=/home/$USER/.docker/config.json --type=kubernetes.io/dockerconfigjson```
5. Create "vcounter" namespace: 
    * ```kubectl apply -f "$DeployDirectory/vcount/namespace.yml"```
6. Copy credential secret to new namespace:
    * ```kubectl get secret gitlab-registry-credentials -o yaml | sed 's/default/vcounter/g' | kubectl apply -f -```

#### Build and deploy

1. Build, Tag and push image using script: 
    * linux: [build.sh](../../deployment/k8s/local/build.sh)

#### DNS

1. Get minikube IP: ```minikube ip```
2. Add ip and hostname to /etc/hosts: ```<IP> vcounter.k8s.local```

_Note:_ ```vcounter.k8s.local``` domain name is used in k8s ingress configuration [file](/deployment/k8s/local/vcount/ingress.yml)
