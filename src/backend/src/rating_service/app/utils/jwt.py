import json
from typing import Dict
from jwcrypto.jwt import JWT

from jwcrypto.jwk import JWKSet, JWK

from utils.api_requests import get_request
from utils.settings import settings


def decode_jwt(
    token: str | bytes,
  ) -> Dict:
    jwks = __get_jwks()
    
    jwt = JWT()
    jwt.deserialize(jwt=token, key=jwks)
    
    return json.loads(jwt.claims)

def __transform_dict_to_jwks(jwks_dict: Dict) -> JWKSet:
  return JWKSet.from_json(keyset=json.dumps(jwks_dict, sort_keys=True))

def __construct_jwks_auth_url(
  host=settings.options.jwks.host,
  port=settings.options.jwks.port,
) -> str:
  return f"http://{host}:{port}/api/v1/user/.well-known/jwks.json"

def __get_jwks() -> JWKSet:
  url = __construct_jwks_auth_url()
  response = get_request(
    url=url,
  )
  
  return __transform_dict_to_jwks(response.json())
