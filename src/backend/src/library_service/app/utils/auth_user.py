from typing import Annotated, Dict, List
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from utils.validate import validate_token_decode, validate_token_type
from enums.enums import BadRequestErrorTextEnum, LoginErrorTextEnum, RoleEnum, TokenTypeEnum
from exceptions.http import BadRequestException, ForbiddenException, NotAuthorizedException
from schemas.user import UserPayloadDto
from utils.addons import get_pydantic_validation_error_text

http_bearer = HTTPBearer(auto_error=False)


def __get_raw_payload(
  token: str | None,
) -> Dict:
  raw = validate_token_decode(token)
  return raw

def __transform_payload_to_user_dto(
  raw_payload: Dict,
) -> UserPayloadDto:
  validate_token_type(raw_payload, token_type=TokenTypeEnum.ACCESS)
  try:
    payload: UserPayloadDto = UserPayloadDto.model_validate(raw_payload)
  except ValidationError as err:
    raise BadRequestException(
      error_in=BadRequestErrorTextEnum.INVALID_PAYLOAD_FIELD,
      detail=get_pydantic_validation_error_text(err),
    )
    
  return payload

def get_current_user(
  token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> UserPayloadDto:
  if token is None:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.NO_TOKEN)
  raw_payload = __get_raw_payload(token=token.credentials)
  
  return __transform_payload_to_user_dto(raw_payload=raw_payload)

class RoleChecker:
  def __init__(self, allowed_roles: List[RoleEnum]):
    self.allowed_roles: List[RoleEnum] = allowed_roles
  
  def __call__(self, user: Annotated[UserPayloadDto, Depends(get_current_user)]) -> bool:
    if user.role == RoleEnum.ADMIN \
      or user.role in self.allowed_roles:
      return True
    
    raise ForbiddenException()