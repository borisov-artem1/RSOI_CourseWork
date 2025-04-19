from typing import Dict
from fastapi.security import HTTPAuthorizationCredentials
from jwcrypto.jws import InvalidJWSSignature
from jwcrypto.jwt import JWTExpired

from enums.enums import PayloadEnum, BadRequestErrorTextEnum, LoginErrorTextEnum, TokenTypeEnum
from utils.jwt import decode_jwt
from exceptions.http import BadRequestAuthException, NotAuthorizedException

def validate_token_exists(
  token: HTTPAuthorizationCredentials | None,
):
  if token is None:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.NO_TOKEN)

def validate_token_decode(
  token: str | None
) -> Dict:
  if token is None:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.NO_TOKEN)
  try:
    user_raw = decode_jwt(token)
  except ValueError:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.INVALID_TOKEN_FORMAT)
  except InvalidJWSSignature:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.INVALID_PUBLIC_KEY)
  except JWTExpired:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.TOKEN_HAS_EXPIRED)
  
  return user_raw

def validate_token_type(
  payload: Dict,
  token_type: TokenTypeEnum,
) -> None:
  try:
    if payload[PayloadEnum.TOKEN_TYPE] != token_type:
      raise BadRequestAuthException(
        error_in=BadRequestErrorTextEnum.INVALID_TOKEN_TYPE,
        detail=TokenTypeEnum.REFRESH if token_type == TokenTypeEnum.ACCESS else TokenTypeEnum.ACCESS,
      )
  except KeyError as err:
    raise BadRequestAuthException(
        error_in=BadRequestErrorTextEnum.INVALID_PAYLOAD_FIELD,
        detail=err,
      )
