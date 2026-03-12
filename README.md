# K8s Cluster

A repository which uses GitHub Workspaces to spin up a kind cluster.
We can then use this kind cluster to try out different k8s observability techniques.

## Branch Specific Goals

This branch is used to help demonstrate our cost allocation & security context capabilities by running three different versions of the same python script which emits metrics and logs.  Each container will emit a metric/log for `teamA`, `teamB` and `teamC`.

### Instructions

First, you need to build the docker image by running `docker build -t test-image:0.1 .`
Now that the docker image has been built, you need to load it into the Kind cluster which has been configured using `kind load docker-image test-image:0.1`
Now we can apply the kubernetes manifests to bring up the resources.  In order:

1. Update `./manifest/secret.yaml` which each of the team's DT OTel API Ingest Tokens
1. Execute `kubectl apply -f ./manifest/namespace.yaml`
1. Execute `kubectl apply -f ./manifest/secret.yaml`
1. Execute `kubectl apply -f ./manifest/otel-config.yaml`
1. Execute `kubectl apply -f ./manifest/app-deployment/deployment-team-a.yaml`
1. Execute `kubectl apply -f ./manifest/app-deployment/deployment-team-b.yaml`
1. Execute `kubectl apply -f ./manifest/app-deployment/deployment-team-c.yaml`

You should now be able to use `k9s` to validate functionality of the test applications.