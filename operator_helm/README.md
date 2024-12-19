This folder provides an example `values.yaml` file that can be used
with the Operator Helm chart.  The installation command then becomes:

```
helm install dynatrace-operator oci://public.ecr.aws/dynatrace/dynatrace-operator \
    --create-namespace \
    --namespace dynatrace \
    --atomic \
    -f ./operator_helm/values.yaml
```