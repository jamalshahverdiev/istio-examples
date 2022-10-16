from jinja2 import Environment, FileSystemLoader
from python_jwt import generate_jwt, verify_jwt
from jwcrypto import jwk
from datetime import timedelta

PAYLOAD = {
    'iss': 'ISSUER',
    'sub': 'SUBJECT',
    'aud': 'AUDIENCE',
    'role': 'user',
    'permission': 'read'
}

PRIVATE_KEY="./keys/PRIVATE.pem"
PUBLIC_KEY="./keys/PUBLIC.pem"

with open(PUBLIC_KEY, "rb") as pemfile:
    PUBLIC = jwk.JWK.from_pem(pemfile.read())
    PUBLIC = PUBLIC.export()
    
with open(PRIVATE_KEY, "rb") as pemfile:
    PRIVATE_K = jwk.JWK.from_pem(pemfile.read())
    PRIVATE_K = PRIVATE_K.export()

JWT_TOKEN = generate_jwt(PAYLOAD, jwk.JWK.from_json(PRIVATE_K), 'RS256', timedelta(minutes=1000000))
HEADER, CLAIMS = verify_jwt(JWT_TOKEN, jwk.JWK.from_json(PUBLIC), ['RS256'])

GATEWAY_NAME = 'httpbin-gateway'
HTTPBIN_DOMAIN = 'httpbin.istio.domain.local'
HTTPBIN_VS_NAME = 'httpbin'
NAMESPACE = 'foo'
ISSUER = 'ISSUER'
CRD_NAME = 'jwt-httpbin'
AUTHZPOLICY_CRD_NAME = 'httpbin-authzpolicy'
ACTION = 'DENY'
RULE_MATCH_KEY_VALUE = 'app: httpbin'
ENVIRONMENT = Environment(loader=FileSystemLoader("templates/"))
REQUEST_AUTH_TEAMPLATE = ENVIRONMENT.get_template("RequestAuthentication.yaml")
AUTHZ_POLICY_TEAMPLATE = ENVIRONMENT.get_template("AuthorizationPolicy.yaml")
GATEWAY_TEMPLATE = ENVIRONMENT.get_template("Gateway.yaml")
VIRTUALSERVICE_TEMPLATE = ENVIRONMENT.get_template("Virtualservice.yaml")
REQUEST_AUTH_FILENAME = 'RequestAuthentication-Rendered.yaml'
AUTHZ_POLICY_FILENAME = 'AuthzPolicy-Rendered.yaml'
GATEWAY_FILENAME = 'Gateway-Rendered.yaml'
VIRTUALSERVICE_FILENAME = 'Virtualservice-Rendered.yaml'

REQUEST_AUTH_CONTENT = REQUEST_AUTH_TEAMPLATE.render(
    NAMESPACE=NAMESPACE,
    ISSUER=ISSUER,
    CRD_NAME=CRD_NAME,
    RULE_MATCH_KEY_VALUE=RULE_MATCH_KEY_VALUE,
    PUBLIC=PUBLIC
)

AUTHZ_POLICY_CONTENT = AUTHZ_POLICY_TEAMPLATE.render(
    NAMESPACE=NAMESPACE,
    ACTION=ACTION,
    AUTHZPOLICY_CRD_NAME=AUTHZPOLICY_CRD_NAME,
    RULE_MATCH_KEY_VALUE=RULE_MATCH_KEY_VALUE
)

GATEWAY_CONTENT = GATEWAY_TEMPLATE.render(
    GATEWAY_NAME=GATEWAY_NAME,
    NAMESPACE=NAMESPACE,
    HTTPBIN_DOMAIN=HTTPBIN_DOMAIN
)

VIRTUALSERVICE_CONTENT = VIRTUALSERVICE_TEMPLATE.render(
    HTTPBIN_VS_NAME=HTTPBIN_VS_NAME,
    NAMESPACE=NAMESPACE,
    HTTPBIN_DOMAIN=HTTPBIN_DOMAIN
)