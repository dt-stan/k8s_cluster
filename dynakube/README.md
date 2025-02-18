# Dynakube Helm Chart

## Background

By default the Dynatrace deployment provides two instructions to instrument
a Kubernetes cluster.

1. Operator Deployment
1. Manifest Deployment (provided as `dynakube.yaml`)

In the event that there are multiple kubernetes clusters or Dynatrace tenants
you would like to connect to, you will need to duplicate and modify the `dynakube.yaml` manifest file appropriately.

You could update each attribute in the manifest and use a process like
[envsubst](https://linuxhandbook.com/envsubst-command/) to programmatically update the necessary variables.

Or you could leverage this Helm chart version of the `dynakube.yaml` manifest and either update/provide a `values.yaml` file or use `--set` commands as a part of your installation command.

## Example

In the following Helm install example, I have set the following Environment Variables and use `--set` commands to fill those values into the `dynakube.yaml` manifest for installation.

- `DT_API_TOKEN`: The Dynatrace Operator Token
- `DT_DATA_TOKEN`: The Dynatrace Data Ingest Token
- `DT_API_URL`: The Dynatrace Tenant API Ingest endpoint

```
helm install --set api_tokens.operator_token=$DT_API_TOKEN --set api_tokens.data_ingest_token=$DT_DATA_TOKEN --set api_url=$DT_API_URL --set cluster_name="k8s-poc" --set cluster_group="k8s-group" dynakube | more
```

## Helm Values

- `api_tokens.hashed`: [Default `false`] Determines the format of the API Tokens. If you're using a plain text API Token, this value should remain the default of `false`. If you're copying a hashed password directly from a generated manifest file, this value should be `true`
- `api_tokens.operator_token`: [**Required**] The [Dynatrace Operator Token](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/deployment/tokens-permissions#operatorToken)
- `api_tokens.data_ingest_token`: [**Required**] The [Dynatrace Data Ingest Token](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/deployment/tokens-permissions#dataIngestToken)
- `api_url`: [**Required**] The Dynatrace Tenant API.  This will be different for SaaS tenants vs Managed Environments.
    - \[SaaS\]: `https://{your-environment-id}.live.dynatrace.com/api`
    - \[Managed\]: `https://{your-activegate-domain}:{your-port}/e/{your-environment-id}/api`
- `cluster_group`: [*Optional*] This corresponds to the "Group" field in the Deploy OneAgent screen.  It will cover:
    - Network Zone
    - ActiveGate Group
    - Host Group
- `cluster_name`: [**Required**] This is a Dynatrace identifier for your cluster.  It will cover:
    - Kubernetes cluster display name
    - Secret name
    - DynaKube custom resource
    - ActiveGate and OneAgent pods
- `containers.oneagent.registry`: [*Optional*] This can be used to specify which OneAgent Container Image to deploy, specifically which registry to pull the image from.
    - Example: `docker.io/dynatrace`
- `containers.oneagent.image_name`: [*Optional*] This can be used to specify which OneAgent Container Image to deploy, specifically the container image name
    - Example: `dynatrace-oneagent`
- `containers.oneagent.image_tag`: [*Optional*] This can be used to specify which OneAgent Container Image to deploy, specifically the container tag/release.
    - Example: `1.303.70.202412110194654`
- `containers.codemodules.registry`: [*Optional*] This can be used to specify which Code Module Container Image to deploy, specifically which registry to pull the image from.
    - Example: `docker.io/dynatrace`
- `containers.codemodules.image_name`: [*Optional*] This can be used to specify which Code Module Container Image to deploy, specifically the container image name
    - Example: `dynatrace-codemodules`
- `containers.codemodules.image_tag`: [*Optional*] This can be used to specify which Code Module Container Image to deploy, specifically the container tag/release.
    - Example: `1.303.70.202412110194654`
- `containers.activegate.registry`: [*Optional*] This can be used to specify which ActiveGate Container Image to deploy, specifically which registry to pull the image from.
    - Example: `docker.io/dynatrace`
- `containers.activegate.image_name`: [*Optional*] This can be used to specify which ActiveGate Container Image to deploy, specifically the container image name
    - Example: `dynatrace-activegate`
- `containers.activegate.image_tag`: [*Optional*] This can be used to specify which ActiveGate Container Image to deploy, specifically the container tag/release.
    - Example: `1.303.41.20241206-221951`
- `namespace`: [Default `dynatrace`] Defines which namespace to deploy the resources to.

- `namespace_selector_label`: [*Optional*] Defines a Kubernetes label which [the Operator will respect as the only namespaces to instrument](https://docs.dynatrace.com/docs/ingest-from/setup-on-k8s/guides/operation/annotate#monitor-specific-namespaces).  Prevents the OneAgent from instrumenting all Pods in your cluster.

- `skip_cert_check`: [Default: `false`] A flag which will disable the certificate inspection for installer download and API communication.
- `oneagent.node_selector`: [*Optional*] Defines a [NodeSelector label](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) to control on which nodes the OneAgent will be deployed
- `oneagent.resources`: [*Optional*] Defines the requests and limits for Kubernetes resources for the OneAgent pods
- `oneagent.init_resources`: [*Optional*] Defines the requests and limits for Kubernetes resources for the init containers that bootstrap the OneAgent pods
- `activegate.node_selector`: [*Optional*] Defines a [NodeSelector label](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) to control on which nodes the ActiveGate will be deployed
- `activegate.resources`: [*Optional*] Defines the requests and limits for Kubernetes resources for the ActiveGate Pods
- `activegate.resources.replicas`: [*Optional*] Defines the number of ActiveGate Pods which will be spun up.  Defaults to a single pod but can be increased to help with cluster load.