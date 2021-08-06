DeployDirectory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ProjectRootDirectory="$DeployDirectory/../../../."
DockerFileDirectory=$ProjectRootDirectory
NowTimestamp=$(date +"%H-%M")

Registry="registry.gitlab.com"
RegistryToken="$ENV_GITLAB_REGISTRY_TOKEN"
RegistryUsername="$ENV_GITLAB_REGISTRY_USERNAME"
DockerConfigPath=".dockerconfigjson=/home/$USER/.docker/config.json"
ImageName="$ENV_GITLAB_PROJECT_GROUP_NAME/vcounter"
ImageVersion="$USER-$NowTimestamp"
ImageTag="$Registry/$ImageName:$ImageVersion"

echo "Image tag: $ImageTag"

poetry export --output "$ProjectRootDirectory/requirements.txt"
poetry build --format wheel

docker login $Registry -u $RegistryUsername -p $RegistryToken
docker build --progress plain --force-rm -t "$ImageTag" "$DockerFileDirectory"
docker push "$ImageTag"

echo "Image pushed to $Registry. Image tag: $ImageTag"

# create deployment file from sample
ESCAPED_REPLACE=$(printf '%s\n' "$ImageTag" | sed -e 's/[\/&]/\\&/g')
sed "s/IMAGE_NAME/$ESCAPED_REPLACE/g" $DeployDirectory/vcount/deployment.sample.yml > $DeployDirectory/vcount/deployment.yml

kubectl create secret generic gitlab-registry-credentials --from-file=$DockerConfigPath --type=kubernetes.io/dockerconfigjson
kubectl get secret gitlab-registry-credentials -o yaml | sed 's/default/vcounter/g' | kubectl apply -f -

kubectl apply -f "$DeployDirectory/vcount/namespace.yml"
kubectl apply -f "$DeployDirectory/vcount/service.yml"
kubectl apply -f "$DeployDirectory/vcount/deployment.yml"
kubectl apply -f "$DeployDirectory/vcount/ingress.yml"

kubectl apply -f "$DeployDirectory/redis/service.yml"
kubectl apply -f "$DeployDirectory/redis/deployment.yml"
