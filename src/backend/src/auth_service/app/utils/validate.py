from typing import Dict, List
import bcrypt
from jwcrypto.jws import InvalidJWSSignature
from jwcrypto.jwt import JWTExpired

from utils.enums import BadRequestErrorTextEnum, LoginErrorTextEnum, PayloadEnum, TokenTypeEnum
from exceptions.http import BadRequestException, NotAuthorizedException
from model.user import UserModel
from utils.jwt import auth_jwt


# ДИСКЛЕЙМЕР: Вообще, не очень хорошо, что функции типа validate еще возвращают полезный
# результат, но я хочу так

'''
Функция проверяет, что в возвращенном массиве пользователей есть переданный логин.

Суть: Так как есть желание использовать базовый набор эндпоинтов, то получение юзера по логину
происходит из функции уровня репозитория GetAll(filters), которая возвращает список объектов
типа UserModel. Также эта функция производит сравнение по ILIKE, поэтому при логине "user", будут
получены все юзера следующего вида "%user%".

Происходит проверка, что строгий логин находится в списке полученных пользователей. Если нет, то
кастомная ошибка NotAuthorizedException. Если да, то возвращает этого юзера

* login: str - логин в строковом представлении
* users: List[UserModel] - список пользователей
'''
def validate_user_login_in_users(
  login: str,
  users: List[UserModel],
) -> UserModel:
  for user in users:
    if user.login == login:
      return user

  raise NotAuthorizedException(
    error_in=LoginErrorTextEnum.INVALID_LOGIN,
  )
    

'''
Функция проверяет совпадение переданного и реального паролей пользователя. Если пароли не
совпадают, то кастомная ошибка NotAuthorizedException.

* password: str - переданный для сравнения пароль
* hashed_password: bytes - реальный пароль пользователя в байтовом представлении
'''
def validate_password(
  password: str,
  hashed_password: bytes
) -> None:
  if not bcrypt.checkpw(
    password=password.encode(),
    hashed_password=hashed_password,
  ):
    raise NotAuthorizedException(
      error_in=LoginErrorTextEnum.INVALID_PASSWORD,
    )

'''
Фукнкция проверяет токен при декодировании. Если токен может быть декодирован, то
он возвращается из этой функции в типе Dict, иначе экспешн

* token: str | None - токен
'''
def validate_token_decode(
  token: str | None
) -> Dict:
  if token is None:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.NO_TOKEN)
  try:
    user_raw = auth_jwt.decode_jwt(token)
  except ValueError:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.INVALID_TOKEN_FORMAT)
  except InvalidJWSSignature:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.INVALID_PUBLIC_KEY)
  except JWTExpired:
    raise NotAuthorizedException(error_in=LoginErrorTextEnum.TOKEN_HAS_EXPIRED)
  
  return user_raw

'''
Функция проверяет тип токена из payload. Если типы токенов не совпадают, то экспешн

* payload: str - payload токена
* token_type: TokenTypeEnum - тип токена
'''
def validate_token_type(
  payload: Dict,
  token_type: TokenTypeEnum,
) -> None:
  try:
    if payload[PayloadEnum.TOKEN_TYPE] != token_type:
      raise BadRequestException(
        error_in=BadRequestErrorTextEnum.INVALID_TOKEN_TYPE,
        detail=TokenTypeEnum.REFRESH if token_type == TokenTypeEnum.ACCESS else TokenTypeEnum.ACCESS,
      )
  except KeyError as err:
    raise BadRequestException(
        error_in=BadRequestErrorTextEnum.INVALID_PAYLOAD_FIELD,
        detail=err,
      )
