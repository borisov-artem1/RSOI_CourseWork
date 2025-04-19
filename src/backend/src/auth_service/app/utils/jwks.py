import json
from typing import Dict, List
from pathlib import Path
from jwcrypto.jwk import JWK, JWKSet, InvalidJWKValue

from utils.settings import settings

'''
Класс для работы с методами, связанными с JWK
'''
class AuthJWK:
  '''
  Функция получения набора ключей JWKSet из файла
  
  Вход:
    * private_keys: bool - выдавать ли данные приватных ключей или только публичные
    * jwks_file_path: Path - путь до файла с jwks
  Выход:
    * набор ключей JWK в словаре dict ({"keys": [...]})
  '''
  @staticmethod
  def get_jwks_from_file(
    private_keys: bool = False,
    jwks_file_path: Path = settings.options.jwks.jwks_path,
  ) -> Dict | str | None:
    try:
      with open(jwks_file_path, "r") as jwks_file:
        jwks = JWKSet.from_json(jwks_file.read())
        
      return jwks.export(private_keys=private_keys, as_dict=True)
    except FileNotFoundError:
      return None
    except InvalidJWKValue:
      return None
  
  '''
  Функция перевода набора ключей JWK из словаря dict в тип JWKSet 
  
  Вход:
    * jwks_dict: Dict - набора ключей JWK
  Выход:
    * набор ключей JWK типа JWKSet
  '''
  @staticmethod
  def transform_dict_to_jwks(jwks_dict: Dict) -> JWKSet:
    return JWKSet.from_json(keyset=json.dumps(jwks_dict, sort_keys=True))

  '''
  Функция генерации JWK ключей. Ключи записываются в файл jwks.json
  
  Вход:
    * number_of_keys: int - количество ключей для генерации
    * force: bool - если передан флаг и есть уже сгенерированные
    ключи, записанные в файл jwks.json, то они сгенерируются заново
  Выход:
    * None
  '''
  @staticmethod
  def generate_jwks(
    number_of_keys: int = settings.options.jwks.keys_to_generate,
    force: bool = False,
  ) -> None:
    jwks = AuthJWK.get_jwks_from_file()
    
    if jwks and force is False:
      return
    else:
      keys: List[JWK] = []
      for kid in range(1, number_of_keys+1):
        key = JWK.generate(
          kty=settings.options.jwks.kty,
          size=settings.options.jwks.size,
          alg=settings.options.jwks.alg,
          use=settings.options.jwks.use,
          kid=str(kid),
        )
        keys.append(key)
        
      AuthJWK.export_to_file(keys)

  '''
  Функция, которая записывает в файл jwks.json набор ключей JWK
  
  Вход:
    * jwks: List[JWK] - список ключей JWK
  Выход:
    * None
  '''
  @staticmethod
  def export_to_file(jwks: List[JWK]) -> None:
    with open(settings.options.jwks.jwks_path, "w") as jwks_file:
      keys = []
      
      for jwk in jwks:
        keys.append(jwk.export(private_key=True, as_dict=True))
        
      if keys is not None:
        json.dump({"keys": keys}, jwks_file, indent=2)
        
  @staticmethod
  def get_by_kid(jwks: JWKSet, kid: str) -> JWK:
    return jwks.get_key(kid=kid)
    
  
auth_jwk = AuthJWK()
