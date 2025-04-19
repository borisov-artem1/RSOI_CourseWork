from pathlib import Path
from pydantic import BaseModel
from yaml import safe_load
from utils.consts import *

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = "config.yaml"


class ServiceSettings(BaseModel):
  host: str = None
  port: int = None
  log_level: str = None
  reload: bool = None


class GatewayServiceSettings(ServiceSettings):
  max_num_of_fails: int = None
  timeout: int = None
  library_host: str = None
  rating_host: str = None
  reservation_host: str = None

  
class JWKSSettings(BaseModel):
  host: str = None
  port: int = None
  kid: str = None
  
class StatisticsSettings(BaseModel):
  host: str = None
  port: int = None

class SettingOptions(BaseModel):
  gateway_service: GatewayServiceSettings = GatewayServiceSettings()
  library_service: ServiceSettings = ServiceSettings()
  rating_service: ServiceSettings = ServiceSettings()
  reservation_service: ServiceSettings = ServiceSettings()
  jwks: JWKSSettings = JWKSSettings()
  statistics: StatisticsSettings = StatisticsSettings()

class Settings():
  options: SettingOptions = SettingOptions()

  def __init__(self, config_name: str=CONFIG_PATH):
    with open(config_name, 'r') as f:
      data = safe_load(f)

    try:
      gateway_service_data = data[SERVICE+S_SUFFIX][GATEWAY]
      Settings.options.gateway_service.host = gateway_service_data[HOST]
      Settings.options.gateway_service.port = gateway_service_data[PORT]
      Settings.options.gateway_service.log_level = gateway_service_data[LOG_LEVEL]
      Settings.options.gateway_service.reload = gateway_service_data[RELOAD]
      Settings.options.gateway_service.max_num_of_fails = gateway_service_data[MAX_NUM_OF_FAILS]
      Settings.options.gateway_service.timeout = gateway_service_data[TIMEOUT]
      Settings.options.gateway_service.library_host = gateway_service_data[LIBRARY+UNDERSCORE+HOST]
      Settings.options.gateway_service.rating_host = gateway_service_data[RATING+UNDERSCORE+HOST]
      Settings.options.gateway_service.reservation_host = gateway_service_data[RESERVATION+UNDERSCORE+HOST]

      library_service_data = data[SERVICE+S_SUFFIX][LIBRARY]
      Settings.options.library_service.host = library_service_data[HOST]
      Settings.options.library_service.port = library_service_data[PORT]
      Settings.options.library_service.log_level = library_service_data[LOG_LEVEL]
      Settings.options.library_service.reload = library_service_data[RELOAD]

      rating_service_data = data[SERVICE+S_SUFFIX][RATING]
      Settings.options.rating_service.host = rating_service_data[HOST]
      Settings.options.rating_service.port = rating_service_data[PORT]
      Settings.options.rating_service.log_level = rating_service_data[LOG_LEVEL]
      Settings.options.rating_service.reload = rating_service_data[RELOAD]

      reservation_service_data = data[SERVICE+S_SUFFIX][RESERVATION]
      Settings.options.reservation_service.host = reservation_service_data[HOST]
      Settings.options.reservation_service.port = reservation_service_data[PORT]
      Settings.options.reservation_service.log_level = reservation_service_data[LOG_LEVEL]
      Settings.options.reservation_service.reload = reservation_service_data[RELOAD]

      authServiceData = data[SERVICE+S_SUFFIX][AUTH]
      Settings.options.jwks.host = authServiceData[NETWORK_HOST]
      Settings.options.jwks.port = authServiceData[PORT]
      Settings.options.jwks.kid = authServiceData[JWKS_KID]
      
      statisticsServiceData = data[SERVICE+S_SUFFIX][STATISTICS]
      Settings.options.statistics.host = statisticsServiceData[NETWORK_HOST]
      Settings.options.statistics.port = statisticsServiceData[PORT]
    except KeyError as e:
      print(f"SETTINGS: no argument {e}")
    else:
      Settings.__log()
      
  def __log():
    print(f"\n{Settings.options.model_dump_json(indent=2)}\n")
    

settings = Settings() # TODO: 2 раза при первом запуске
