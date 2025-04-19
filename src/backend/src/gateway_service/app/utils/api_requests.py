import inspect
import requests
from requests import Response
from fastapi import status

from exceptions.http import InvalidRequestException, ServiceUnavailableException
from utils.consts import AUTH
from utils.addons import get_service_name

def __check_status_code(
  status_code: int,
  service_name: str
) -> None:
  method = inspect.stack()[1][3]
  method = " ".join(method.split('_')).title()
  
  if status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
    raise ServiceUnavailableException(
      message=f"{service_name} unavailable: cannot decode jwt token"
    )
  elif status_code >= 400:
    raise InvalidRequestException(
      prefix=method,
      status_code=status_code
    )


def get_request(
  url: str,
  params: str = None,
) -> Response:
  try:
    response: Response = requests.get(
      url=url,
      params=params,
    )
  except:
    response = Response()
    response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    
  __check_status_code(response.status_code, get_service_name(domain_name=AUTH))
  return response
