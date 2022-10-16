# Implement JWT authorization and authentication between services with ISTIO

## Requirements

* Kubernetes Cluster 
* Istio 
* Python3
* kubectl

#### Before starting implement JWT we must create `PUBLIC` and `PRIVATE` key which will be used to forlumate PUBLIC key for validation JWT token and TOKEN itself. And deploy test `httpbin` application inside of the `foo` namespace. To full implementation of JWT we must write another service which will be responsible to create `JWT_TOKENS` with `PRIVATE` key. In our case we will use PYTHON code to do that, but for validation we will convert PUBLIC key to ISTIO CRD format which will be used by `RequestAuthentication` istio object. 

**Note:** `KUBECONFIG` must be present in terminal where we will execute all following commands

#### Execute the following script to create keys and `httpbin` objects inside of the `foo` namespace

```bash
$ ./create-keys-and-apply-httpbin.sh
```

#### The following `PYTHON` code, by using predefined `PUBLIC` and `PRIVATE` keys (these files created by `create-keys-and-apply-httpbin.sh` script) creates `JWT_TOKEN`, converted `PUBLIC key` to istio `RequestAuthentication` format and Kubernetes manifests and then applies them to `foo` namespace.

```python
./generate-validate-jwt-from-keys.py
```

#### To test flow we cat execute the following command

```bash
$ DOMAIN_NAME='httpbin.istio.domain.local'
$ export Token='JWT TOKEN OUTPUT FROM PYTHON CODE'
$ curl --header "Authorization: Bearer $Token" https://${DOMAIN_NAME}/headers -s -o /dev/null -w "%{http_code}\n"
```