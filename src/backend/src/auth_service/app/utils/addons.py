from typing import Annotated, Dict, List
import bcrypt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError

from utils.validate import validate_token_decode, validate_token_type
from dto.user import UserPayloadDto, UserRefreshPayloadDto
from exceptions.http import BadRequestException, ForbiddenException, NotAuthorizedException
from utils.enums import BadRequestErrorTextEnum, LoginErrorTextEnum, PayloadEnum, RoleEnum, TokenTypeEnum
from utils.jwt import auth_jwt

http_bearer = HTTPBearer(auto_error=False)

'''
Функция, экранирующая службные символы в PostgreSQL

Вход:
  * text - входная строка
Выход:
  * строка с экранированными символами
'''
def escape_like(text: str) -> str:
  return text.replace("%", "\\%").replace("\\", "\\\\").replace("_", "\\_")

'''
Функция, добавляющая "%" для ilike поиска в PostgreSQL

Вход:
  * text - входная строка
Выход:
  * строка с символами "%"
'''
def ilike_search(text: str) -> str:
  return "%" + text + "%";

'''
Функция, удаляющая из строки text символы symbols

Вход:
  * text - входная строка
  * symbols - символы для удаления
Выход:
  * строка с удаленными символами
'''
def remove_extra_symbols(text: str, symbols: str) -> str:
  translate_table = str.maketrans(symbols, "^"*len(symbols))
  return text.translate(translate_table).replace("^", "")

def get_pydantic_validation_error_text(err: ValidationError) -> str:
  errors = err.errors()
  text = remove_extra_symbols(
    text="; ".join(f"{e['loc']}: {e['msg']}" for e in errors),
    symbols="()[],",
  )
  
  return text

'''
Функция, для хеширования паролей

Вход:
  * password - пароль типа str
Выход:
  * хешированный пароль типа bytes
'''
def hash_password(
  password: str,
) -> bytes:
  salt = bcrypt.gensalt()
  pwd_bytes: bytes = password.encode()
  return bcrypt.hashpw(password=pwd_bytes, salt=salt)

'''
Вспомогательная функция, которая достает из jwt-токена пользователя его payload
в виде словаря Dict 

Вход:
  * token - входной токен
Выход:
  * словарь dict с полями payload-а
'''
def __get_raw_payload(
  token: str | None,
) -> Dict:
  raw = validate_token_decode(token)
  return raw

'''
Вспомогательная функция, которая переводит payload из типа Dict
в вид UserPayloadDto

Вход:
  * raw_payload - payload в виде Dict
Выход:
  * payload пользователя UserPayloadDto
'''
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

'''
Функция для получения аутентифицированного пользователя из его jwt access токена

Вход:
  * token - входной токен
Выход:
  * payload пользователя в виде UserPayloadDto
'''
def get_current_user(
  token: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> UserPayloadDto:
  if token is None:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.NO_TOKEN)
  raw_payload = __get_raw_payload(token=token.credentials)
  
  return __transform_payload_to_user_dto(raw_payload=raw_payload)

'''
Вспомогательная функция, которая переводит payload из типа Dict
в вид UserRefreshPayloadDto

Вход:
  * raw_payload - payload в виде Dict
Выход:
  * payload пользователя UserRefreshPayloadDto
'''
def __transform_payload_to_refresh_dto(
  raw_payload: Dict,
) -> UserRefreshPayloadDto:
  validate_token_type(raw_payload, token_type=TokenTypeEnum.REFRESH)
  try:
    payload: UserRefreshPayloadDto = UserRefreshPayloadDto.model_validate(raw_payload)
  except ValidationError as err:
    raise BadRequestException(
      error_in=BadRequestErrorTextEnum.INVALID_PAYLOAD_FIELD,
      detail=get_pydantic_validation_error_text(err),
    )

  return payload

'''
Функция для получения payload refresh токена

Вход:
  * token - входной токен
Выход:
  * payload пользователя в виде UserRefreshPayloadDto
'''
def get_refresh_token_payload(
  token: str | None = None,
) -> UserRefreshPayloadDto:
  raw_payload = __get_raw_payload(token=token)
  return __transform_payload_to_refresh_dto(raw_payload=raw_payload)

'''
Класс проверки ролей пользователей (ролевой авторизации)
'''
class RoleChecker:
  '''
  Функция инициализации объекта класса
  
  Вход:
    * allowed_roles: List[RoleEnum] - список ролей RoleEnum, с которыми разрешено (!)
    выполнить метод, где данный класс используется
  Выход:
    * Объект класса
  '''
  def __init__(self, allowed_roles: List[RoleEnum]):
    self.allowed_roles: List[RoleEnum] = allowed_roles
  
  '''
  Функция, которая позволяет вызвать объект класса как функцию. Выполнится логика, которая прописана в
  ней. Соответственно, данная функция получает текущего аутентифицированного пользователя и проверяет его роль
  на совпадение с одной из разрешенных. При этом пользователь с ролью "ADMIN" автоматически получает авторизацию
  '''
  def __call__(self, user: Annotated[UserPayloadDto, Depends(get_current_user)]) -> bool:
    if user.role == RoleEnum.ADMIN \
      or user.role in self.allowed_roles:
      return True
    
    raise ForbiddenException()
