#!/usr/bin/env python3
from subprocess import run
from src.variables import (
    AUTHZ_POLICY_CONTENT,
    CLAIMS,
    GATEWAY_CONTENT,
    HEADER,
    JWT_TOKEN,
    PRIVATE_K,
    PUBLIC,
    REQUEST_AUTH_CONTENT,
    REQUEST_AUTH_FILENAME,
    AUTHZ_POLICY_FILENAME,
    GATEWAY_FILENAME,
    VIRTUALSERVICE_CONTENT,
    VIRTUALSERVICE_FILENAME
)

print("\n*****************  PUBLIC KEY CONTENT  *****************\n")
print(PUBLIC)
print("\n*****************  PRIVATE KEY CONTENT  *****************\n")
print(PRIVATE_K)
print("\n*****************  JWT TOKEN TO AUTHENTICATE  *****************\n")
print(JWT_TOKEN)

print("\n*********************  JWT TOKEN INFO  *********************\n")
print(HEADER)
print(CLAIMS)

with open(REQUEST_AUTH_FILENAME, mode="w", encoding="utf-8") as message:
    message.write(REQUEST_AUTH_CONTENT)

with open(AUTHZ_POLICY_FILENAME, mode="w", encoding="utf-8") as message:
    message.write(AUTHZ_POLICY_CONTENT)

with open(GATEWAY_FILENAME, mode="w", encoding="utf-8") as message:
    message.write(GATEWAY_CONTENT)
    
with open(VIRTUALSERVICE_FILENAME, mode="w", encoding="utf-8") as message:
    message.write(VIRTUALSERVICE_CONTENT)

print("\n*****************  Applying manifests to Kubernetes *****************\n")
for filename in REQUEST_AUTH_FILENAME, AUTHZ_POLICY_FILENAME, GATEWAY_FILENAME, VIRTUALSERVICE_FILENAME:
    run(["kubectl", "apply", "-f", filename])
    run(["rm", "-rf", filename])