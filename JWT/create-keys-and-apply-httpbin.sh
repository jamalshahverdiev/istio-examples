#!/usr/bin/env bash
ISTIO_FOLDER='istio'
ISTIO_VERSION='1.15.0'
KEY_FOLDER='keys'
NAMESPACE='foo'
PRIVATE_KEYFILE='private-key.pem'
PUBLIC_KEYFILE='public-key.pem'

if [ ! -d ${KEY_FOLDER} ]; then 
    mkdir ${KEY_FOLDER} && cd ${KEY_FOLDER}
    openssl genrsa -out ${PRIVATE_KEYFILE} 2048
    openssl rsa -in ${PRIVATE_KEYFILE} -pubout -out ${PUBLIC_KEYFILE}
fi 

if [ ! -d ${ISTIO_FOLDER}-${ISTIO_VERSION} ]; then 
    curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -
fi

kubectl create ns ${NAMESPACE}
kubectl apply -f <(istioctl kube-inject -f ${ISTIO_FOLDER}-${ISTIO_VERSION}/samples/httpbin/httpbin.yaml) -n ${NAMESPACE}