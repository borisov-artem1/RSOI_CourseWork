from typing import List
from pydantic import ValidationError
from sqlalchemy.orm import Session
from uuid import UUID
from jwcrypto.jws import InvalidJWSSignature
from jwcrypto.jwt import JWTExpired

from utils.addons import get_pydantic_validation_error_text, get_refresh_token_payload
from utils.enums import BadRequestErrorTextEnum, LoginErrorTextEnum, PayloadEnum, RoleEnum, TokenTypeEnum
from utils.jwks import auth_jwk
from utils.jwt import auth_jwt
from model.user import UserModel
from exceptions.http import BadRequestException, NotAuthorizedException, NotFoundException, ConflictException
from dto.user import JWKSResponse, TokenInfo, UserCreateDto, UserFilterDto, UserLoginDto, UserPaginationResponse, UserRefreshPayloadDto, UserResponse, UserUpdateDto
from repository.user import UserRepository
from utils.validate import validate_user_login_in_users, validate_password


class UserService():
  def __init__(self, userRepository: UserRepository, db: Session):
    self._userRepository: UserRepository = userRepository(db)

  async def auth_user(
    self,
    login_dto: UserLoginDto,
  ) -> TokenInfo:
    users, _ = await self._userRepository.get_all(
      filter=UserFilterDto(
        login=login_dto.login,
      )
    )
    
    user = validate_user_login_in_users(login_dto.login, users)
    validate_password(login_dto.password, user.password)
    
    return TokenInfo(
      access_token=auth_jwt.get_access_token(user, scope=login_dto.scope),
      refresh_token=auth_jwt.get_refresh_token(user)
    )
    
  async def register_user(
    self,
    user_create: UserCreateDto,
  ) -> TokenInfo:
    user = await self._userRepository.create(
      UserModel(**user_create.model_dump())
    )
    if user is None:
      raise ConflictException(prefix="register user")
    
    token = TokenInfo(
      access_token=auth_jwt.get_access_token(user),
      refresh_token=auth_jwt.get_refresh_token(user),
    )
    
    return token
  
  async def refresh_user_token(
    self,
    refresh_token: str | None,
    scope: List[RoleEnum] | None = None,
  ) -> TokenInfo:
    user_refresh_payload = get_refresh_token_payload(refresh_token)
      
    user = await self._userRepository.get_by_uuid(
      uuid=user_refresh_payload.sub,
    )
    if user is None:
      raise NotFoundException(prefix="get user")
    
    token = TokenInfo(
      access_token=auth_jwt.get_access_token(user, scope=scope),
      refresh_token=refresh_token,
    )
    
    return token

  async def get_jwks(self) -> JWKSResponse:
    return auth_jwk.get_jwks_from_file()

  async def get_all(
      self,
      filter: UserFilterDto,
      page: int = 1,
      size: int = 100
  ) -> UserPaginationResponse:
    users, totalItems = await self._userRepository.get_all(
      filter=filter,
      offset=(page - 1) * size,
      limit=size,
    )
    
    usersResponse = [UserResponse.model_validate(user, from_attributes=True) for user in users]
  
    return UserPaginationResponse(
      page=page,
      pageSize=size,
      totalElements=totalItems,
      items=usersResponse
    )
  
  async def get_by_uuid(
      self,
      uuid: UUID
  ) -> UserResponse:
    user = await self._userRepository.get_by_uuid(uuid)
    if user is None:
      raise NotFoundException(prefix="get user")
    
    return UserResponse.model_validate(user, from_attributes=True)
  
  async def create(
      self,
      user_create: UserCreateDto,
  ) -> UserResponse:
    user = await self._userRepository.create(
      UserModel(**user_create.model_dump())
    )
    if user is None:
      raise ConflictException(prefix="create user")
    
    return user
  
  async def patch(
      self,
      uuid: UUID,
      user_patch: UserUpdateDto
  ) -> UserResponse:
    user = await self._userRepository.get_by_uuid(uuid)
    if user is None:
      raise NotFoundException(prefix="patch user")
    
    user = await self._userRepository.update(user, user_patch)
    if user is None:
      raise ConflictException(prefix="patch user")
    
    return user
  
  async def delete(
      self,
      uuid: UUID
  ) -> UserResponse:
    user = await self._userRepository.get_by_uuid(uuid)
    if user is None:
      raise NotFoundException(prefix="delete user")
    
    return await self._userRepository.delete(user)
