from pathlib import Path
from pydantic import BaseModel
from yaml import safe_load
from utils.consts import *

BASE_DIR = Path(__file__).parent.parent
CERTS_DIR_NAME = "certs"
CONFIG_PATH = "config.yaml"


class ServiceSettings(BaseModel):
  host: str = None
  port: int = None
  log_level: str = None
  reload: bool = None


class DatabaseSettings(BaseModel):
  user: str = None
  password: str = None
  host: str = None
  port: int = None
  db_name: str = None
  
  
class AuthJWTSettings(BaseModel):
  typ: str = "JWT"
  algorithm: str = "RS256" # так как ключи Private и Public / иначе HS256
  access_token_expire_minutes: int = 15
  refresh_token_expire_minutes: int = 60
  
class JWKSSettings(BaseModel):
  jwks_path: Path = BASE_DIR / CERTS_DIR_NAME / "jwks.json"
  keys_to_generate: int = 1
  kty: str = "RSA"
  size: int = 2048
  alg: str = "RSA256"
  use: str = "sig"
  kid: str = None # из глобальных настроек, чтобы также менять во всех сервисах
  
  
class SettingOptions(BaseModel):
  service: ServiceSettings = ServiceSettings()
  database: DatabaseSettings = DatabaseSettings()
  auth_jwt: AuthJWTSettings = AuthJWTSettings()
  jwks: JWKSSettings = JWKSSettings()


class Settings():
  options: SettingOptions = SettingOptions()

  def __init__(self, config_name: str=CONFIG_PATH):
    with open(config_name, 'r') as f:
      data = safe_load(f)

    try:
      currentServiceData = data[SERVICES][AUTH]
      Settings.options.service.host = currentServiceData[HOST]
      Settings.options.service.port = currentServiceData[PORT]
      Settings.options.service.log_level = currentServiceData[LOG_LEVEL]
      Settings.options.service.reload = currentServiceData[RELOAD]

      currentDatabaseData = data[DATABASES][AUTH+DB_SUFFIX]
      Settings.options.database.user = currentDatabaseData[USER]
      Settings.options.database.password = currentDatabaseData[PASSWORD]
      Settings.options.database.host = currentDatabaseData[HOST]
      Settings.options.database.port = currentDatabaseData[PORT]
      Settings.options.database.db_name = currentDatabaseData[DB_NAME]
      
      authServiceData = data[SERVICES][AUTH]
      Settings.options.jwks.kid = authServiceData[JWKS_KID]
    except KeyError as e:
      print(f"SETTINGS: no argument {e}")
    else:
      Settings.__log()
      
  def __log():
    print(f"\n{Settings.options.model_dump_json(indent=2)}\n")
    
    
settings = Settings() # TODO: 2 раза при первом запуске
