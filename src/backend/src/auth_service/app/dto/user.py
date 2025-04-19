from datetime import datetime
from typing import Annotated, List
from uuid import UUID
from fastapi import Query
from pydantic import BaseModel, ConfigDict, conint, constr, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from utils.enums import AuthTypeEnum, JWTScopeEnum

from utils.enums import RoleEnum

PhoneNumber.phone_format = 'E164' # чтобы не было в возврате приписки 'tel:'

class UserBaseDto(BaseModel):
  login: Annotated[str, constr(max_length=255)]
  lastname: Annotated[str, constr(max_length=255)]
  firstname: Annotated[str, constr(max_length=255)]
  email: EmailStr
  phone: PhoneNumber
  role: RoleEnum

class UserFilterDto(UserBaseDto):
  login: Annotated[str, Query(max_length=255)] | None = None
  lastname: Annotated[str, Query(max_length=255)] | None = None
  firstname: Annotated[str, Query(max_length=255)] | None = None
  email: Annotated[str, Query(max_length=255)] | None = None
  phone: Annotated[str, Query(max_length=64)] | None = None
  role: Annotated[RoleEnum, Query(max_length=50)] | None = None

class UserCreateDto(UserBaseDto):
  password: Annotated[str, constr(min_length=4)]

class UserUpdateDto(UserBaseDto):
  login: Annotated[str, constr(max_length=255)] | None = None
  lastname: Annotated[str, constr(max_length=255)] | None = None
  firstname: Annotated[str, constr(max_length=255)] | None = None
  password: str | None = None
  email: EmailStr | None = None
  phone: PhoneNumber | None = None
  role: RoleEnum | None = None

class UserDto(UserBaseDto):
  id: Annotated[int, conint(ge=1)]
  uuid: UUID
  password: str

class UserResponse(UserBaseDto):
  model_config = ConfigDict(from_attributes=True) # чинит какую-то ошибку
  uuid: UUID

class UserPaginationResponse(BaseModel):
  page: Annotated[int, conint(ge=1)]
  pageSize: Annotated[int, conint(ge=1)]
  totalElements: Annotated[int, conint(ge=0)]
  items: List[UserResponse]
  
# Auth
class UserLoginDto(BaseModel):
  login: Annotated[str, constr(max_length=255)]
  password: Annotated[str, constr(min_length=4)]
  scope: List[JWTScopeEnum] | None = None

class TokenInfo(BaseModel):
  access_token: str
  refresh_token: str | None = None
  auth_type: str = AuthTypeEnum.BEARER
  
class JWKResponse(BaseModel):
  kid: str
  kty: str
  alg: str
  use: str
  n: str
  e: str
  
class JWKSResponse(BaseModel):
  keys: List[JWKResponse]
  
class UserPayloadDto(BaseModel):
  sub: UUID # в контексте jwt - "sub" это идентификатор (uuid / id), у меня uuid
  login: str
  role: RoleEnum
  email: EmailStr | None = None
  phone: PhoneNumber | None = None
  lastname: str | None = None
  firstname: str | None = None
  type: str | None = None
  exp: datetime
  iat: datetime
  
class UserRefreshDto(BaseModel):
  refresh_token: str
  scope: List[JWTScopeEnum] | None = None
  
class UserRefreshPayloadDto(BaseModel):
  sub: UUID
  exp: datetime
  iat: datetime
  type: str | None = None
