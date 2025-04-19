from datetime import timedelta, datetime, timezone
from typing import Dict, List
from jwcrypto.jwt import JWT
import json

from utils.jwks import auth_jwk
from model.user import UserModel
from utils.enums import HeaderEnum, JWTScopeEnum, TokenTypeEnum, PayloadEnum
from utils.settings import settings
from utils.consts import JWKS_KID

'''
Класс для работы с методами, связанными с JWT
'''
class AuthJWT:
  '''
  Функция, которая выдает jwt access токен
  
  Вход:
    * user: UserModel - модель пользователя для загрузки нужных данных в payload
    * scope: List[str] - массив элементов типа JWTScopeEnum, в зависимости от которых
    загружается та или иная информация из user
  Выход:
    * jwt токен в виде строки str
  '''
  @staticmethod
  def get_access_token(
    user: UserModel,
    scope: List[str] | None = None,
  ) -> str:
    jwt_header = AuthJWT.__create_header()
    jwt_payload = AuthJWT.__create_payload(user, TokenTypeEnum.ACCESS, scope)
    
    return AuthJWT.encode_jwt(
      header = jwt_header,
      payload=jwt_payload,
    )
  
  '''
  Функция, которая выдает jwt refresh токен
  
  Вход:
    * user: UserModel - модель пользователя для загрузки нужных данных в payload
  Выход:
    * jwt токен в виде строки str
  '''
  @staticmethod
  def get_refresh_token(
    user: UserModel,
  ) -> str:
    jwt_header = AuthJWT.__create_header()
    jwt_payload = AuthJWT.__create_payload(
      user,
      TokenTypeEnum.REFRESH,
      expire_minutes=settings.options.auth_jwt.refresh_token_expire_minutes,
    )

    return AuthJWT.encode_jwt(
      header=jwt_header,
      payload=jwt_payload,
    )
  
  '''
  Вспомогательная функция, которая записывает в payload сервисную информацию, которая не
  зависит от пользовтеля:
    * token_type: TokenTypeEnum - тип токена
    * iat: int - дата создания токена в POSIX формате
    * exp: int - дата окончания токена в POSIX формате
    
  Вход:
    * token_type: TokenTypeEnum - тип токена
    * expire_minutes: int - время жизни токена в минутах
    * expire_timedelta: timedelta - продолжительность жизни токена в виде timedelta
  Выход:
    * payload с сервисными данными типа Dict
  '''
  @staticmethod
  def __create_service_payload(
    token_type: TokenTypeEnum,
    expire_minutes: int = settings.options.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
  ) -> Dict:
    now = datetime.now(timezone.utc)
    if expire_timedelta:
      expire = now + expire_timedelta
    else:
      expire = now + timedelta(minutes=expire_minutes)

    jwt_service_payload = {
      PayloadEnum.TOKEN_TYPE: token_type,
      PayloadEnum.IAT: int(now.timestamp()),
      PayloadEnum.EXP: int(expire.timestamp()),
    }
    
    return jwt_service_payload
  
  '''
  Вспомогательная функция, которая создает payload токена, заполняя его сервисными
  данными (см функцию __create_service_payload) и полезными данными UserModel конкретного
  пользователя в зависимости от scope:
    * openid: sub, login, role
    * email: openid + email
    * profile: email + lastname, firstname, phone
    
  Вход:
    * user: UserModel - модель данных пользователя
    * token_type: TokenTypeEnum - тип токена
    * scope: List[str] - типы scope
    * expire_minutes: int - время жизни токена в минутах
    * expire_timedelta: timedelta - продолжительность жизни токена в виде timedelta
  Выход:
    * payload с данными типа Dict
  '''
  @staticmethod
  def __create_payload(
    user: UserModel,
    token_type: TokenTypeEnum,
    scope: List[str] | None = None,
    expire_minutes: int = settings.options.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
  ) -> Dict:
    jwt_payload = AuthJWT.__create_service_payload(
      token_type=token_type,
      expire_minutes=expire_minutes,
      expire_timedelta=expire_timedelta,
    )
    
    jwt_payload.update({
      PayloadEnum.SUB: str(user.uuid),
    })
    
    if token_type == TokenTypeEnum.REFRESH:
      return jwt_payload
    elif token_type == TokenTypeEnum.ACCESS:
      jwt_payload.update({
        PayloadEnum.LOGIN: user.login,
        PayloadEnum.ROLE: user.role,
      })
      
      if scope is None:
        return jwt_payload
      else:
        for data in scope:
          if data == JWTScopeEnum.OPENID:
            continue # базовый payload access
          elif data == JWTScopeEnum.EMAIL:
            jwt_payload.update({
              PayloadEnum.EMAIL: user.email
            })
          elif data == JWTScopeEnum.PROFILE:
            jwt_payload.update({
              PayloadEnum.LASTNAME: user.lastname,
              PayloadEnum.FIRSTNAME: user.firstname,
              PayloadEnum.PHONE: user.phone,
            })
      
    return jwt_payload
  
  '''
  Вспомогательная функция, которая создает header токена, заполняя его сервисными
  данными:
    * alg: str - алгоритм, который был использован для подписи
    * typ: str - тип токена (JWT)
    * kid: str - идентификатор ключа подписи JWKS
    
  Вход:
    * alg: str - алгоритм, который был использован для подписи
    * typ: str - тип токена (JWT)
    * kid: str - идентификатор ключа подписи JWKS
  Выход:
    * header с данными типа Dict
  '''
  @staticmethod
  def __create_header(
    algorithm: str = settings.options.auth_jwt.algorithm,
    typ: str = settings.options.auth_jwt.typ,
    kid: str = settings.options.jwks.kid,
  ):
    jwt_header = {
      HeaderEnum.ALG: algorithm,
      HeaderEnum.TYP: typ,
      HeaderEnum.KID: kid,
    }
    
    return jwt_header
  
  '''
  Функция, которая создает (кодирует) и подписывает токен
  ключом, который получен из связки ключей типа JWKSet
  по айди ключа jwk_kid:
    
  Вход:
    * header: dict - header jwt токена
    * payload: dict - payload jwt токена
    * jwk_kid: str - идентификатор ключа набора ключей jwks
  Выход:
    * jwt токен в виде строки str
  '''
  @staticmethod
  def encode_jwt(
    header: dict,
    payload: dict,
    jwk_kid: str = settings.options.jwks.kid,
  ):
    token = JWT(
      header=header,
      claims=payload,
    )
    
    jwks_dict = auth_jwk.get_jwks_from_file(private_keys=True)
    jwks = auth_jwk.transform_dict_to_jwks(jwks_dict)
    key = auth_jwk.get_by_kid(jwks, jwk_kid)
    
    token.make_signed_token(
      key=key,
    )
    
    return token.serialize()
  
  '''
  Функция, которая декодирует токен token и проверяет его подпись 
  ключом, который получен из связки ключей типа JWKSet
  по айди ключа jwk_kid
    
  Вход:
    * token: str - jwt токен
  Выход:
    * jwt токен в виде строки str
  '''
  @staticmethod
  def decode_jwt(
    token: str | bytes,
  ) -> JWT:
    jwks_dict = auth_jwk.get_jwks_from_file()
    jwks = auth_jwk.transform_dict_to_jwks(jwks_dict)
    
    jwt = JWT()
    jwt.deserialize(jwt=token, key=jwks)
    
    return json.loads(jwt.claims)


auth_jwt = AuthJWT()
