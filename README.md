# K8s Cluster

A repository which uses GitHub Workspaces to spin up a kind cluster.
We can then use this kind cluster to try out different k8s observability techniques.

## Dynatrace Installation

This repository also includes the resources required to install the Dynatrace Operator
*and* the Dynatrace Manfiest (Dynakube.yaml) as Helm install commands.

### /operator_helm

This folder contains an example `values.yaml` file that can be passed to the Operator
Helm install command like so:

```
helm install dynatrace-operator oci://public.ecr.aws/dynatrace/dynatrace-operator \
    --create-namespace \
    --namespace dynatrace \
    --atomic \
    -f ./operator_helm/values.yaml
```

### /dynakube

This is a Helm chart version of the `dynakube.yaml` manifest file.  The reason for turning this
into a Helm chart is to provide flexibility in the manifest configuration options.  Most attributes
of the manifest file have been turned into values that can be set programatically.  This
enables teams to maintain a single `dynakube.yaml` file but provide flexibility for the Dynatrace
tenant and Kubernetes Cluster they will be connecting to.